import os

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import tensorflow as tf
import numpy as np
from glob import glob
from itertools import cycle
import malaya_speech
import malaya_speech.train
from malaya_speech.train.model import univnet_nonorm as univnet
from malaya_speech.train.model import universal_melgan as melgan
from malaya_speech.train.model import melgan as melgan_loss
from malaya_speech.train.model import stft
import malaya_speech.config
from malaya_speech.train.loss import calculate_2d_loss, calculate_3d_loss
import random


def generate(batch_max_steps=8192, hop_size=256):
    while True:
        npys = glob('universal-audio/*.npy')
        random.shuffle(npys)
        for f in npys:
            audio = np.load(f)
            mel = np.load(f.replace('-audio', '-mel'))

            batch_max_frames = batch_max_steps // hop_size
            if len(audio) < len(mel) * hop_size:
                audio = np.pad(audio, [[0, len(mel) * hop_size - len(audio)]])

            if len(mel) > batch_max_frames:
                interval_start = 0
                interval_end = len(mel) - batch_max_frames
                start_frame = random.randint(interval_start, interval_end)
                start_step = start_frame * hop_size
                audio = audio[start_step: start_step + batch_max_steps]
                mel = mel[start_frame: start_frame + batch_max_frames, :]
            else:
                audio = np.pad(audio, [[0, batch_max_steps - len(audio)]])
                mel = np.pad(mel, [[0, batch_max_frames - len(mel)], [0, 0]])

            yield {'mel': mel, 'audio': audio}


dataset = tf.data.Dataset.from_generator(
    generate,
    {'mel': tf.float32, 'audio': tf.float32},
    output_shapes={
        'mel': tf.TensorShape([None, 80]),
        'audio': tf.TensorShape([None]),
    },
)
dataset = dataset.shuffle(32)
dataset = dataset.padded_batch(
    32,
    padded_shapes={
        'audio': tf.TensorShape([None]),
        'mel': tf.TensorShape([None, 80]),
    },
    padding_values={
        'audio': tf.constant(0, dtype=tf.float32),
        'mel': tf.constant(0, dtype=tf.float32),
    },
)

features = dataset.make_one_shot_iterator().get_next()

gen_config = univnet.GeneratorConfig()
melgan_config = malaya_speech.config.universal_melgan_config

generator = univnet.Generator(gen_config, name='universalunivnet-generator')
discriminator = melgan.MultiScaleDiscriminator(
    melgan.WaveFormDiscriminatorConfig(
        **melgan_config['melgan_waveform_discriminator_params']
    ),
    melgan.STFTDiscriminatorConfig(
        **melgan_config['melgan_stft_discriminator_params']
    ),
    name='universalmelgan-discriminator',
)

stft_loss_params = {
    'fft_lengths': [1024, 2048, 512],
    'frame_steps': [120, 240, 50],
    'frame_lengths': [600, 1200, 240],
}
stft_loss = stft.loss.MultiResolutionSTFT(**stft_loss_params)
mels_loss = melgan_loss.loss.TFMelSpectrogram()
mse_loss = tf.keras.losses.MeanSquaredError()
mae_loss = tf.keras.losses.MeanAbsoluteError()


def compute_per_example_generator_losses(features):
    y_hat = generator(features['mel'], training=True)
    audios = features['audio']

    sc_loss, mag_loss = calculate_2d_loss(
        audios, tf.squeeze(y_hat, -1), stft_loss
    )

    sc_loss = tf.where(sc_loss >= 10.0, tf.zeros_like(sc_loss), sc_loss)
    mag_loss = tf.where(mag_loss >= 10.0, tf.zeros_like(mag_loss), mag_loss)

    generator_loss = 0.5 * (sc_loss + mag_loss)

    p_hat = discriminator(y_hat)
    p = discriminator(tf.expand_dims(audios, 2))

    adv_loss = 0.0
    for i in range(len(p_hat)):
        adv_loss += mse_loss(tf.ones_like(p_hat[i][-1]), p_hat[i][-1])
    adv_loss /= i + 1

    fm_loss = 0.0
    for i in range(len(p_hat)):
        for j in range(len(p_hat[i]) - 1):
            fm_loss += mae_loss(p[i][j], p_hat[i][j])
    fm_loss /= (i + 1) * (j + 1)
    adv_loss += 10 * fm_loss

    generator_loss += 4.0 * adv_loss

    per_example_losses = generator_loss

    a = calculate_2d_loss(audios, tf.squeeze(y_hat, -1), loss_fn=mels_loss)

    dict_metrics_losses = {
        'adversarial_loss': adv_loss,
        'fm_loss': fm_loss,
        'gen_loss': tf.reduce_mean(generator_loss),
        'mels_spectrogram_loss': tf.reduce_mean(a),
    }

    return per_example_losses, dict_metrics_losses


def compute_per_example_discriminator_losses(features):
    y_hat = generator(features['mel'], training=True)
    audios = features['audio']
    y = tf.expand_dims(audios, 2)
    p = discriminator(y)
    p_hat = discriminator(y_hat)

    real_loss = 0.0
    fake_loss = 0.0
    for i in range(len(p)):
        real_loss += mse_loss(tf.ones_like(p[i][-1]), p[i][-1])
        fake_loss += mse_loss(tf.zeros_like(p_hat[i][-1]), p_hat[i][-1])

    real_loss /= i + 1
    fake_loss /= i + 1
    dis_loss = real_loss + fake_loss

    per_example_losses = dis_loss

    dict_metrics_losses = {
        'real_loss': real_loss,
        'fake_loss': fake_loss,
        'dis_loss': dis_loss,
    }

    return per_example_losses, dict_metrics_losses


per_example_losses, generator_losses = compute_per_example_generator_losses(
    features
)
generator_loss = tf.reduce_mean(per_example_losses)

per_example_losses, discriminator_losses = compute_per_example_discriminator_losses(
    features
)
discriminator_loss = tf.reduce_mean(per_example_losses)

for k, v in generator_losses.items():
    tf.summary.scalar(k, v)

for k, v in discriminator_losses.items():
    tf.summary.scalar(k, v)

summaries = tf.summary.merge_all()

t_vars = tf.trainable_variables()
d_vars = [
    var
    for var in t_vars
    if var.name.startswith('universalmelgan-discriminator')
]
g_vars = [
    var for var in t_vars if var.name.startswith('universalunivnet-generator')
]

global_step_generator = tf.Variable(
    100000, trainable=False, name='global_step_generator'
)
global_step_discriminator = tf.Variable(
    100000, trainable=False, name='global_step_discriminator'
)

d_optimizer = tf.train.AdamOptimizer(0.00001, beta1=0.5, beta2=0.9).minimize(
    discriminator_loss, var_list=d_vars, global_step=global_step_discriminator
)
g_optimizer = tf.train.AdamOptimizer(0.0001, beta1=0.5, beta2=0.9).minimize(
    generator_loss, var_list=g_vars, global_step=global_step_generator
)

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

saver = tf.train.Saver(var_list=g_vars)
saver.restore(sess, tf.train.latest_checkpoint('universal-univnet-32-generator'))

saver = tf.train.Saver()

checkpoint = 10000
write_tensorboard = 100
epoch = 4_000_000
path = 'universal-univnet-32-combined'

writer = tf.summary.FileWriter(f'./{path}')

ckpt_path = tf.train.latest_checkpoint(path)
if ckpt_path:
    saver.restore(sess, ckpt_path)
    print(f'restoring checkpoint from {ckpt_path}')

global_step = sess.run(global_step_generator)
for i in range(global_step, epoch):
    g_loss, _, g_losses = sess.run([generator_loss, g_optimizer, generator_losses])
    d_loss, _ = sess.run([discriminator_loss, d_optimizer])
    i = sess.run(global_step_generator)

    if i % write_tensorboard == 0:
        s = sess.run(summaries)
        writer.add_summary(s, i)

    if i % checkpoint == 0:
        saver.save(sess, f'{path}/model.ckpt', global_step=i)

    print(i, g_loss, d_loss, g_losses)

saver.save(sess, f'{path}/model.ckpt', global_step=epoch)
