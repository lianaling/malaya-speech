from malaya_speech.supervised import stt, lm
from herpetologist import check_type
import json

_transducer_availability = {
    'tiny-conformer': {
        'Size (MB)': 24.4,
        'Quantized Size (MB)': 9.14,
        'WER': 0.2128108,
        'CER': 0.08136871,
        'WER-LM': 0.1996828,
        'CER-LM': 0.0770037,
        'Language': ['malay'],
    },
    'small-conformer': {
        'Size (MB)': 49.2,
        'Quantized Size (MB)': 18.1,
        'WER': 0.19853302,
        'CER': 0.07449528,
        'WER-LM': 0.18536073,
        'CER-LM': 0.07114307,
        'Language': ['malay'],
    },
    'conformer': {
        'Size (MB)': 125,
        'Quantized Size (MB)': 37.1,
        'WER': 0.1636023,
        'CER': 0.0587443,
        'WER-LM': 0.1561821,
        'CER-LM': 0.0571897,
        'Language': ['malay'],
    },
    'large-conformer': {
        'Size (MB)': 404,
        'Quantized Size (MB)': 107,
        'WER': 0.1566839,
        'CER': 0.0619715,
        'WER-LM': 0.1486221,
        'CER-LM': 0.0590102,
        'Language': ['malay'],
    },
    'conformer-stack-2mixed': {
        'Size (MB)': 130,
        'Quantized Size (MB)': 38.5,
        'WER': 0.1036084,
        'CER': 0.050069,
        'WER-LM': 0.1029111,
        'CER-LM': 0.0502013,
        'Language': ['malay', 'singlish'],
    },
    'conformer-stack-3mixed': {
        'Size (MB)': 130,
        'Quantized Size (MB)': 38.5,
        'WER': 0.2347684,
        'CER': 0.133944,
        'WER-LM': 0.229241,
        'CER-LM': 0.1307018,
        'Language': ['malay', 'singlish', 'mandarin'],
    },
    'small-conformer-singlish': {
        'Size (MB)': 49.2,
        'Quantized Size (MB)': 18.1,
        'WER': 0.0878310,
        'CER': 0.0456859,
        'WER-LM': 0.08733263,
        'CER-LM': 0.04531657,
        'Language': ['singlish'],
    },
    'conformer-singlish': {
        'Size (MB)': 125,
        'Quantized Size (MB)': 37.1,
        'WER': 0.07779246,
        'CER': 0.0403616,
        'WER-LM': 0.07718602,
        'CER-LM': 0.03986952,
        'Language': ['singlish'],
    },
    'large-conformer-singlish': {
        'Size (MB)': 404,
        'Quantized Size (MB)': 107,
        'WER': 0.07014733,
        'CER': 0.03587201,
        'WER-LM': 0.06981206,
        'CER-LM': 0.03572307,
        'Language': ['singlish'],
    },
}

_ctc_availability = {
    'hubert-conformer-tiny': {
        'Size (MB)': 36.6,
        'Quantized Size (MB)': 10.3,
        'WER': 0.3359682,
        'CER': 0.0882573,
        'WER-LM': 0.1992265,
        'CER-LM': 0.0635223,
        'Language': ['malay'],
    },
    'hubert-conformer': {
        'Size (MB)': 115,
        'Quantized Size (MB)': 31.1,
        'WER': 0.238714,
        'CER': 0.0608998,
        'WER-LM': 0.1414791,
        'CER-LM': 0.0450751,
        'Language': ['malay'],
    },
    'hubert-conformer-large': {
        'Size (MB)': 392,
        'Quantized Size (MB)': 100,
        'WER': 0.2203140,
        'CER': 0.0549270,
        'WER-LM': 0.1280064,
        'CER-LM': 0.03853289,
        'Language': ['malay'],
    },
    'hubert-conformer-large-3mixed': {
        'Size (MB)': 392,
        'Quantized Size (MB)': 100,
        'WER': 0.2411256,
        'CER': 0.0787939,
        'WER-LM': 0.13276059,
        'CER-LM': 0.05748197,
        'Language': ['malay', 'singlish', 'mandarin'],
    },
    'best-rq-conformer-tiny': {
        'Size (MB)': 36.6,
        'Quantized Size (MB)': 10.3,
        'WER': 0.3192907,
        'CER': 0.078988,
        'WER-LM': 0.179582,
        'CER-LM': 0.055521,
        'Language': ['malay'],
    },
    'best-rq-conformer': {
        'Size (MB)': 115,
        'Quantized Size (MB)': 31.1,
        'WER': 0.2536784,
        'CER': 0.0658045,
        'WER-LM': 0.1542058,
        'CER-LM': 0.0482278,
        'Language': ['malay'],
    },
    'best-rq-conformer-large': {
        'Size (MB)': 392,
        'Quantized Size (MB)': 100,
        'WER': 0.2346511,
        'CER': 0.0601605,
        'WER-LM': 0.1300819,
        'CER-LM': 0.044521,
        'Language': ['malay'],
    },
}

_huggingface_availability = {
    'mesolitica/wav2vec2-xls-r-300m-mixed': {
        'Size (MB)': 1180,
        'WER': 0.1322198,
        'CER': 0.0481054,
        'WER-LM': 0.0988016,
        'CER-LM': 0.0411965,
        'Language': ['malay', 'singlish', 'mandarin'],
    },
}

google_accuracy = {
    'malay': {
        'WER': 0.164775,
        'CER': 0.0597320,
    },
    'singlish': {
        'WER': 0.4941349,
        'CER': 0.3026296,
    }
}

_language_model_availability = {
    'bahasa': {
        'Size (MB)': 17,
        'LM order': 3,
        'Description': 'Gathered from malaya-speech ASR bahasa transcript',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 3 --prune 0 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
    'bahasa-news': {
        'Size (MB)': 24,
        'LM order': 3,
        'Description': 'Gathered from malaya-speech bahasa ASR transcript + News (Random sample 300k sentences)',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 3 --prune 0 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
    'bahasa-combined': {
        'Size (MB)': 29,
        'LM order': 3,
        'Description': 'Gathered from malaya-speech ASR bahasa transcript + Bahasa News (Random sample 300k sentences) + Bahasa Wikipedia (Random sample 150k sentences).',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 3 --prune 0 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
    'redape-community': {
        'Size (MB)': 887.1,
        'LM order': 4,
        'Description': 'Mirror for https://github.com/redapesolutions/suara-kami-community',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 4 --prune 0 1 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
    'dump-combined': {
        'Size (MB)': 310,
        'LM order': 3,
        'Description': 'Academia + News + IIUM + Parliament + Watpadd + Wikipedia + Common Crawl + training set from https://github.com/huseinzol05/malaya-speech/tree/master/pretrained-model/prepare-stt',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 3 --prune 0 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
    'manglish': {
        'Size (MB)': 202,
        'LM order': 3,
        'Description': 'Manglish News + Manglish Reddit + Manglish forum + training set from https://github.com/huseinzol05/malaya-speech/tree/master/pretrained-model/prepare-stt.',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 3 --prune 0 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
    'bahasa-manglish-combined': {
        'Size (MB)': 608,
        'LM order': 3,
        'Description': 'Combined `dump-combined` and `manglish`.',
        'Command': [
            './lmplz --text text.txt --arpa out.arpa -o 3 --prune 0 1 1',
            './build_binary -q 8 -b 7 -a 256 trie out.arpa out.trie.klm',
        ],
    },
}


def available_ctc():
    """
    List available Encoder-CTC ASR models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_ctc_availability)


def available_language_model():
    """
    List available Language Model for CTC.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_language_model_availability)


def available_transducer():
    """
    List available Encoder-Transducer ASR models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_transducer_availability)


def available_huggingface():
    """
    List available HuggingFace Malaya-Speech ASR models.
    """
    from malaya_speech.utils import describe_availability

    return describe_availability(_huggingface_availability)


@check_type
def language_model(
    model: str = 'dump-combined', **kwargs
):
    """
    Load KenLM language model.

    Parameters
    ----------
    model : str, optional (default='dump-combined')
        Model architecture supported. Allowed values:

        * ``'bahasa'`` - Gathered from malaya-speech ASR bahasa transcript.
        * ``'bahasa-news'`` - Gathered from malaya-speech ASR bahasa transcript + Bahasa News (Random sample 300k sentences).
        * ``'bahasa-combined'`` - Gathered from malaya-speech ASR bahasa transcript + Bahasa News (Random sample 300k sentences) + Bahasa Wikipedia (Random sample 150k sentences).
        * ``'redape-community'`` - Mirror for https://github.com/redapesolutions/suara-kami-community
        * ``'dump-combined'`` - Academia + News + IIUM + Parliament + Watpadd + Wikipedia + Common Crawl + training set from https://github.com/huseinzol05/malaya-speech/tree/master/pretrained-model/prepare-stt.
        * ``'manglish'`` - Manglish News + Manglish Reddit + Manglish forum + training set from https://github.com/huseinzol05/malaya-speech/tree/master/pretrained-model/prepare-stt.
        * ``'bahasa-manglish-combined'`` - Combined `dump-combined` and `manglish`.

    Returns
    -------
    result : str
    """
    model = model.lower()
    if model not in _language_model_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.stt.available_language_model()`.'
        )

    path_model = lm.load(
        model=model,
        module='language-model',
        **kwargs
    )
    return path_model


@check_type
def deep_ctc(
    model: str = 'hubert-conformer', quantized: bool = False, **kwargs
):
    """
    Load Encoder-CTC ASR model.

    Parameters
    ----------
    model : str, optional (default='hubert-conformer')
        Model architecture supported. Allowed values:

        * ``'hubert-conformer-tiny'`` - Finetuned HuBERT Conformer TINY.
        * ``'hubert-conformer'`` - Finetuned HuBERT Conformer.
        * ``'hubert-conformer-large'`` - Finetuned HuBERT Conformer LARGE.
        * ``'hubert-conformer-large-3mixed'`` - Finetuned HuBERT Conformer LARGE for (Malay + Singlish + Mandarin) languages.
        * ``'best-rq-conformer-tiny'`` - Finetuned BEST-RQ Conformer TINY.
        * ``'best-rq-conformer'`` - Finetuned BEST-RQ Conformer.
        * ``'best-rq-conformer-large'`` - Finetuned BEST-RQ Conformer LARGE.


    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.wav2vec.Wav2Vec2_CTC class
    """
    model = model.lower()
    if model not in _ctc_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.stt.available_ctc()`.'
        )

    return stt.wav2vec2_ctc_load(
        model=model,
        module='speech-to-text-ctc-v2',
        quantized=quantized,
        mode=_ctc_availability[model],
        **kwargs
    )


@check_type
def deep_transducer(
    model: str = 'conformer', quantized: bool = False, **kwargs
):
    """
    Load Encoder-Transducer ASR model.

    Parameters
    ----------
    model : str, optional (default='conformer')
        Model architecture supported. Allowed values:

        * ``'tiny-conformer'`` - TINY size Google Conformer.
        * ``'small-conformer'`` - SMALL size Google Conformer.
        * ``'conformer'`` - BASE size Google Conformer.
        * ``'large-conformer'`` - LARGE size Google Conformer.
        * ``'conformer-stack-2mixed'`` - BASE size Stacked Google Conformer for (Malay + Singlish) languages.
        * ``'conformer-stack-3mixed'`` - BASE size Stacked Google Conformer for (Malay + Singlish + Mandarin) languages.
        * ``'small-conformer-singlish'`` - SMALL size Google Conformer for singlish language.
        * ``'conformer-singlish'`` - BASE size Google Conformer for singlish language.
        * ``'large-conformer-singlish'`` - LARGE size Google Conformer for singlish language.

    quantized : bool, optional (default=False)
        if True, will load 8-bit quantized model.
        Quantized model not necessary faster, totally depends on the machine.

    Returns
    -------
    result : malaya_speech.model.transducer.Transducer class
    """
    model = model.lower()
    if model not in _transducer_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.stt.available_transducer()`.'
        )

    return stt.transducer_load(
        model=model,
        module='speech-to-text-transducer',
        languages=_transducer_availability[model]['Language'],
        quantized=quantized,
        **kwargs
    )


@check_type
def huggingface(model: str = 'mesolitica/wav2vec2-xls-r-300m-mixed', **kwargs):
    """
    Load Finetuned models from HuggingFace. Required Tensorflow >= 2.0.

    Parameters
    ----------
    model : str, optional (default='mesolitica/wav2vec2-xls-r-300m-mixed')
        Model architecture supported. Allowed values:

        * ``'mesolitica/wav2vec2-xls-r-300m-mixed'`` - wav2vec2 XLS-R 300M finetuned on (Malay + Singlish + Mandarin) languages.

    Returns
    -------
    result : malaya_speech.model.huggingface.CTC class
    """
    model = model.lower()
    if model not in _huggingface_availability:
        raise ValueError(
            'model not supported, please check supported models from `malaya_speech.stt.available_huggingface()`.'
        )

    return stt.huggingface_load(model=model, **kwargs)
