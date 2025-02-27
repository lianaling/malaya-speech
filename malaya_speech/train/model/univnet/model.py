from ..universal_melgan.model import TFReflectionPad1d
from ..melgan.layer import WeightNormalization
from ..utils import shape_list
from .layer import get_initializer, LVCBlock
import tensorflow as tf

MAX_WAV_VALUE = 32768.0


class Generator(tf.keras.Model):

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.mel_channel = config.n_mel_channels
        self.noise_dim = config.noise_dim
        self.hop_length = config.hop_length
        self.min_mel = config.min_mel
        channel_size = config.channel_size
        kpnet_conv_size = config.kpnet_conv_size

        kernel_size = 7

        self.conv_pre = tf.keras.models.Sequential([
            TFReflectionPad1d(
                (kernel_size - 1) // 2,
                padding_type='REFLECT',
            ),
            WeightNormalization(tf.keras.layers.Conv1D(
                filters=channel_size,
                kernel_size=7,
            ))
        ])

        self.conv_post = tf.keras.models.Sequential([
            tf.keras.layers.LeakyReLU(alpha=0.2),
            TFReflectionPad1d(
                (kernel_size - 1) // 2,
                padding_type='REFLECT',
            ),
            WeightNormalization(tf.keras.layers.Conv1D(upsample_initial_channel, kernel_size, 1)),
            tf.keras.layers.Activation('tanh'),
        ])

        self.res_stack = []
        hop_length = 1
        for stride in config.strides:
            hop_length = stride * hop_length
            self.res_stack.append(
                LVCBlock(
                    channel_size,
                    self.mel_channel,
                    stride=stride,
                    dilations=config.dilations,
                    cond_hop_length=hop_length,
                    kpnet_conv_size=kpnet_conv_size
                )
            )

    def call(self, c, z=None):
        """
        c (Tensor): the conditioning sequence of mel-spectrogram (batch, in_length, mel_channels) 
        z (Tensor): the noise sequence (batch, in_length, noise_dim)
        """
        if z is None:
            b, l, _ = shape_list(c)
            z = tf.random.normal(shape=(b, l, self.noise_dim))
        z = self.conv_pre(z)
        for res_block in self.res_stack:
            z = res_block(z, c)
        z = self.conv_post(z)
        return z
