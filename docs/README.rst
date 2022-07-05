.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="logo" width="40%" src="https://f000.backblazeb2.com/file/huseinhouse-public/malaya-speech.png">
        </a>
    </p>
    <p align="center">
        <a href="https://pypi.python.org/pypi/malaya-speech"><img alt="Pypi version" src="https://badge.fury.io/py/malaya-speech.svg"></a>
        <a href="https://pypi.python.org/pypi/malaya-speech"><img alt="Python3 version" src="https://img.shields.io/pypi/pyversions/malaya-speech.svg"></a>
        <a href="https://github.com/huseinzol05/Malaya-Speech/blob/master/LICENSE"><img alt="MIT License" src="https://img.shields.io/github/license/huseinzol05/malaya-speech.svg?color=blue"></a>
        <a href="https://pepy.tech/project/malaya-speech"><img alt="total stats" src="https://static.pepy.tech/badge/malaya-speech"></a>
        <a href="https://pepy.tech/project/malaya-speech"><img alt="download stats / month" src="https://static.pepy.tech/badge/malaya-speech/month"></a>
        <a href="https://discord.gg/aNzbnRqt3A"><img alt="discord" src="https://img.shields.io/badge/discord%20server-malaya-rgb(118,138,212).svg"></a>
    </p>

=========

**Malaya-Speech** is a Speech-Toolkit library for bahasa Malaysia, powered by Deep Learning Tensorflow.

Documentation
--------------

Proper documentation is available at https://malaya-speech.readthedocs.io/

Installing from the PyPI
----------------------------------

CPU version
::

    $ pip install malaya-speech

GPU version
::

    $ pip install malaya-speech[gpu]

Only **Python 3.6.0 and above** and **Tensorflow 1.15.0 and above** are supported.

All examples tested on Tensorflow version 1.15.4, 1.15.5, 2.4.1, 2.5 and 2.9.

Development Release
---------------------------------

Install from `master` branch,
::

    $ pip install git+https://github.com/huseinzol05/malaya-speech.git


We recommend to use **virtualenv** for development. 

Documentation at https://malaya-speech.readthedocs.io/en/latest/

Features
--------

-  **Age Detection**, detect age in speech using Finetuned Speaker Vector.
-  **Speaker Diarization**, diarizing speakers using Pretrained Speaker Vector.
-  **Emotion Detection**, detect emotions in speech using Finetuned Speaker Vector.
-  **Force Alignment**, generate a time-aligned transcription of an audio file using RNNT and CTC.
-  **Gender Detection**, detect genders in speech using Finetuned Speaker Vector.
-  **Language Detection**, detect hyperlocal languages in speech using Finetuned Speaker Vector.
-  **Multispeaker Separation**, Multispeaker separation using FastSep on 8k Wav.
-  **Noise Reduction**, reduce multilevel noises using STFT UNET.
-  **Speaker Change**, detect changing speakers using Finetuned Speaker Vector.
-  **Speaker overlap**, detect overlap speakers using Finetuned Speaker Vector.
-  **Speaker Vector**, calculate similarity between speakers using Pretrained Speaker Vector.
-  **Speech Enhancement**, enhance voice activities using Waveform UNET.
-  **SpeechSplit Conversion**, detailed speaking style conversion by disentangling speech into content, timbre, rhythm and pitch using PyWorld and PySPTK.
-  **Speech-to-Text**, End-to-End Speech to Text for Malay, Mixed (Malay, Singlish and Mandarin) and Singlish using RNNT, Wav2Vec2, HuBERT and BEST-RQ CTC.
-  **Super Resolution**, Super Resolution 4x for Waveform.
-  **Text-to-Speech**, Text to Speech for Malay and Singlish using Tacotron2, FastSpeech2, FastPitch, GlowTTS, LightSpeech and VITS.
-  **Vocoder**, convert Mel to Waveform using MelGAN, Multiband MelGAN and Universal MelGAN Vocoder.
-  **Voice Activity Detection**, detect voice activities using Finetuned Speaker Vector.
-  **Voice Conversion**, Many-to-One, One-to-Many, Many-to-Many, and Zero-shot Voice Conversion.
-  **Hybrid 8-bit Quantization**, provide hybrid 8-bit quantization for all models to reduce inference time up to 2x and model size up to 4x.

Pretrained Models
------------------

Malaya-Speech also released pretrained models, simply check at `malaya-speech/pretrained-model <https://github.com/huseinzol05/malaya-speech/tree/master/pretrained-model>`_

-  **Wave UNET**,  Multi-Scale Neural Network for End-to-End Audio Source Separation, https://arxiv.org/abs/1806.03185
-  **Wave ResNet UNET**, added ResNet style into Wave UNET, no paper produced.
-  **Wave ResNext UNET**, added ResNext style into Wave UNET, no paper produced.
-  **Deep Speaker**, An End-to-End Neural Speaker Embedding System, https://arxiv.org/pdf/1705.02304.pdf
-  **SpeakerNet**, 1D Depth-wise Separable Convolutional Network for Text-Independent Speaker Recognition and Verification, https://arxiv.org/abs/2010.12653
-  **VGGVox**, a large-scale speaker identification dataset, https://arxiv.org/pdf/1706.08612.pdf
-  **GhostVLAD**, Utterance-level Aggregation For Speaker Recognition In The Wild, https://arxiv.org/abs/1902.10107
-  **Conformer**, Convolution-augmented Transformer for Speech Recognition, https://arxiv.org/abs/2005.08100
-  **ALConformer**, A lite Conformer, no paper produced.
-  **Jasper**, An End-to-End Convolutional Neural Acoustic Model, https://arxiv.org/abs/1904.03288
-  **Tacotron2**, Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions, https://arxiv.org/abs/1712.05884
-  **FastSpeech2**, Fast and High-Quality End-to-End Text to Speech, https://arxiv.org/abs/2006.04558
-  **MelGAN**, Generative Adversarial Networks for Conditional Waveform Synthesis, https://arxiv.org/abs/1910.06711
-  **Multi-band MelGAN**, Faster Waveform Generation for High-Quality Text-to-Speech, https://arxiv.org/abs/2005.05106
-  **SRGAN**, Modified version of SRGAN to do 1D Convolution, Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network, https://arxiv.org/abs/1609.04802
-  **Speech Enhancement UNET**, https://github.com/haoxiangsnr/Wave-U-Net-for-Speech-Enhancement
-  **Speech Enhancement ResNet UNET**, Added ResNet style into Speech Enhancement UNET, no paper produced.
-  **Speech Enhancement ResNext UNET**, Added ResNext style into Speech Enhancement UNET, no paper produced.
-  **Universal MelGAN**, Universal MelGAN: A Robust Neural Vocoder for High-Fidelity Waveform Generation in Multiple Domains, https://arxiv.org/abs/2011.09631
-  **FastVC**, Faster and Accurate Voice Conversion using Transformer, no paper produced.
-  **FastSep**, Faster and Accurate Speech Separation using Transformer, no paper produced.
-  **wav2vec 2.0**, A Framework for Self-Supervised Learning of Speech Representations, https://arxiv.org/abs/2006.11477
-  **FastSpeechSplit**, Unsupervised Speech Decomposition Via Triple Information Bottleneck using Transformer, no paper produced.
-  **Sepformer**, Attention is All You Need in Speech Separation, https://arxiv.org/abs/2010.13154
-  **FastSpeechSplit**, Faster and Accurate Speech Split Conversion using Transformer, no paper produced.
-  **HuBERT**, Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units, https://arxiv.org/pdf/2106.07447v1.pdf
-  **FastPitch**, Parallel Text-to-speech with Pitch Prediction, https://arxiv.org/abs/2006.06873
-  **GlowTTS**, A Generative Flow for Text-to-Speech via Monotonic Alignment Search, https://arxiv.org/abs/2005.11129
-  **BEST-RQ**, Self-supervised learning with random-projection quantizer for speech recognition, https://arxiv.org/pdf/2202.01855.pdf
-  **LightSpeech**, Lightweight and Fast Text to Speech with Neural Architecture Search, https://arxiv.org/abs/2102.04040
-  **VITS**, Conditional Variational Autoencoder with Adversarial Learning for End-to-End Text-to-Speech, https://arxiv.org/abs/2106.06103

References
-----------

If you use our software for research, please cite:

::

  @misc{Malaya, Speech-Toolkit library for bahasa Malaysia, powered by Deep Learning Tensorflow,
    author = {Husein, Zolkepli},
    title = {Malaya-Speech},
    year = {2020},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/huseinzol05/malaya-speech}}
  }

Acknowledgement
----------------

Thanks to `KeyReply <https://www.keyreply.com/>`_ for private V100s cloud and `Mesolitica <https://mesolitica.com/>`_ for private RTXs cloud to train Malaya-Speech models,

.. raw:: html

    <a href="#readme">
        <img alt="logo" width="20%" src="https://image4.owler.com/logo/keyreply_owler_20191024_163259_original.png">
    </a>

.. raw:: html

    <a href="#readme">
        <img alt="logo" width="20%" src="https://i1.wp.com/mesolitica.com/wp-content/uploads/2019/06/Mesolitica_Logo_Only.png?fit=857%2C532&ssl=1">
    </a>