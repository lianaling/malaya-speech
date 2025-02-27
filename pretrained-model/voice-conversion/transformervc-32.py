import os

os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import numpy as np
from glob import glob
import random
import tensorflow as tf
import pandas as pd
from malaya_speech.train.model import fastspeech, transformervc
from math import ceil
from malaya_speech.train.loss import calculate_2d_loss, calculate_3d_loss
import malaya_speech.train as train
import malaya_speech
from collections import defaultdict
import sklearn

speaker_model = malaya_speech.speaker_vector.deep_model('vggvox-v2')

vctk = glob('vtck/**/*.flac', recursive=True)

vctk_speakers = defaultdict(list)
for f in vctk:
    s = f.split('/')[-1].split('_')[0]
    vctk_speakers[s].append(f)

files = glob('/home/husein/speech-bahasa/ST-CMDS-20170001_1-OS/*.wav')
speakers_mandarin = defaultdict(list)
for f in files:
    speakers_mandarin[f[:-9]].append(f)

df_nepali = pd.read_csv(
    '/home/husein/speech-bahasa/nepali_0/asr_nepali/utt_spk_text.tsv',
    sep='\t',
    header=None,
)
asr_nepali = glob('/home/husein/speech-bahasa/*/asr_nepali/data/*/*.flac')
asr_nepali_replaced = {
    f.split('/')[-1].replace('.flac', ''): f for f in asr_nepali
}
df_nepali = df_nepali[df_nepali[0].isin(asr_nepali_replaced.keys())]

speakers_nepali = defaultdict(list)
for i in range(len(df_nepali)):
    speakers_nepali[df_nepali.iloc[i, 1]].append(
        asr_nepali_replaced[df_nepali.iloc[i, 0]]
    )

speakers = []
for s in vctk_speakers.keys():
    speakers.extend(
        random.sample(vctk_speakers[s], min(500, len(vctk_speakers[s])))
    )

for s in speakers_mandarin.keys():
    speakers.extend(
        random.sample(speakers_mandarin[s], min(200, len(speakers_mandarin[s])))
    )

for s in speakers_nepali.keys():
    speakers.extend(
        random.sample(speakers_nepali[s], min(200, len(speakers_nepali[s])))
    )

salina = glob('/home/husein/speech-bahasa/salina/output-wav-salina/*.wav')
salina = random.sample(salina, 5000)
male = glob('/home/husein/speech-bahasa/turki/output-wav-turki/*.wav')
male.extend(
    glob(
        '/home/husein/speech-bahasa/dari-pasentran-ke-istana/output-wav-dari-pasentran-ke-istana/*.wav'
    )
)
male = random.sample(male, 5000)
haqkiem = glob('/home/husein/speech-bahasa/haqkiem/*.wav')
khalil = glob('/home/husein/speech-bahasa/tolong-sebut/*.wav')
mas = glob('/home/husein/speech-bahasa/sebut-perkataan-woman/*.wav')
husein = glob('/home/husein/speech-bahasa/audio-wattpad/*.wav')
husein.extend(glob('/home/husein/speech-bahasa/audio-iium/*.wav'))
husein.extend(glob('/home/husein/speech-bahasa/audio/*.wav'))
husein.extend(glob('/home/husein/speech-bahasa/sebut-perkataan-man/*.wav'))

files = salina + male + haqkiem + khalil + mas + husein + speakers
sr = 22050


def generate(hop_size=256):
    while True:
        shuffled = sklearn.utils.shuffle(files)
        for f in shuffled:
            audio, _ = malaya_speech.load(f, sr=sr)
            mel = malaya_speech.featurization.universal_mel(audio)
            batch_max_steps = random.randint(16384, 110250)
            batch_max_frames = batch_max_steps // hop_size

            if len(mel) > batch_max_frames:
                interval_start = 0
                interval_end = len(mel) - batch_max_frames
                start_frame = random.randint(interval_start, interval_end)
                start_step = start_frame * hop_size
                mel = mel[start_frame: start_frame + batch_max_frames, :]
                audio = audio[start_step: start_step + batch_max_steps]

            audio_16k = malaya_speech.resample(audio, sr, 16000)
            v = speaker_model([audio_16k])

            yield {
                'mel': mel,
                'mel_length': [len(mel)],
                'audio': audio,
                'v': v[0],
            }


def get_dataset(batch_size=8):
    def get():
        dataset = tf.data.Dataset.from_generator(
            generate,
            {
                'mel': tf.float32,
                'mel_length': tf.int32,
                'audio': tf.float32,
                'v': tf.float32,
            },
            output_shapes={
                'mel': tf.TensorShape([None, 80]),
                'mel_length': tf.TensorShape([None]),
                'audio': tf.TensorShape([None]),
                'v': tf.TensorShape([512]),
            },
        )
        dataset = dataset.shuffle(batch_size)
        dataset = dataset.padded_batch(
            batch_size,
            padded_shapes={
                'audio': tf.TensorShape([None]),
                'mel': tf.TensorShape([None, 80]),
                'mel_length': tf.TensorShape([None]),
                'v': tf.TensorShape([512]),
            },
            padding_values={
                'audio': tf.constant(0, dtype=tf.float32),
                'mel': tf.constant(0, dtype=tf.float32),
                'mel_length': tf.constant(0, dtype=tf.int32),
                'v': tf.constant(0, dtype=tf.float32),
            },
        )
        return dataset

    return get


total_steps = 500000


def model_fn(features, labels, mode, params):
    vectors = features['v'] * 30 - 3.5
    mels = features['mel']
    mels_len = features['mel_length'][:, 0]
    dim_neck = 32
    dim_speaker = 512
    dim_input = 80
    encoder_config = malaya_speech.config.transformer_config.copy()
    decoder_config = malaya_speech.config.transformer_config.copy()
    encoder_config['hidden_size'] = dim_speaker + dim_input
    decoder_config['hidden_size'] = dim_speaker + dim_neck
    encoder_config['activation'] = 'mish'
    decoder_config['activation'] = 'mish'
    config = malaya_speech.config.fastspeech_config
    config = fastspeech.Config(vocab_size=1, **config)
    model = transformervc.Model(
        dim_neck,
        encoder_config,
        decoder_config,
        config,
        dim_input=dim_input,
        dim_speaker=dim_speaker,
        skip=6,
    )
    encoder_outputs, mel_before, mel_after, codes = model(
        mels, vectors, vectors, mels_len
    )
    codes_ = model.call_second(mel_after, vectors, mels_len)
    loss_f = tf.losses.absolute_difference
    max_length = tf.cast(tf.reduce_max(mels_len), tf.int32)
    mask = tf.sequence_mask(
        lengths=mels_len, maxlen=max_length, dtype=tf.float32
    )
    mask = tf.expand_dims(mask, axis=-1)
    mel_loss_before = loss_f(
        labels=mels, predictions=mel_before, weights=mask
    )
    mel_loss_after = loss_f(
        labels=mels, predictions=mel_after, weights=mask
    )
    g_loss_cd = tf.losses.absolute_difference(codes, codes_)
    loss = mel_loss_before + mel_loss_after + g_loss_cd

    tf.identity(loss, 'total_loss')
    tf.identity(mel_loss_before, 'mel_loss_before')
    tf.identity(mel_loss_after, 'mel_loss_after')
    tf.identity(g_loss_cd, 'g_loss_cd')

    tf.summary.scalar('total_loss', loss)
    tf.summary.scalar('mel_loss_before', mel_loss_before)
    tf.summary.scalar('mel_loss_after', mel_loss_after)
    tf.summary.scalar('g_loss_cd', g_loss_cd)

    global_step = tf.train.get_or_create_global_step()

    if mode == tf.estimator.ModeKeys.TRAIN:

        train_op = train.optimizer.adamw.create_optimizer(
            loss,
            init_lr=0.0001,
            num_train_steps=total_steps,
            num_warmup_steps=int(0.1 * total_steps),
            end_learning_rate=0.00001,
            weight_decay_rate=0.001,
            beta_1=0.9,
            beta_2=0.98,
            epsilon=1e-6,
            clip_norm=1.0,
        )
        estimator_spec = tf.estimator.EstimatorSpec(
            mode=mode, loss=loss, train_op=train_op
        )

    elif mode == tf.estimator.ModeKeys.EVAL:

        estimator_spec = tf.estimator.EstimatorSpec(
            mode=tf.estimator.ModeKeys.EVAL, loss=loss
        )

    return estimator_spec


train_hooks = [
    tf.train.LoggingTensorHook(
        ['total_loss', 'mel_loss_before', 'mel_loss_after', 'g_loss_cd'],
        every_n_iter=1,
    )
]
train_dataset = get_dataset()

save_directory = 'transformervc-32-vggvox-v2'

train.run_training(
    train_fn=train_dataset,
    model_fn=model_fn,
    model_dir=save_directory,
    num_gpus=1,
    log_step=1,
    save_checkpoint_step=2000,
    max_steps=total_steps,
    train_hooks=train_hooks,
    eval_step=0,
)
