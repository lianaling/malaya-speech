# %%
# Define constant sampling rate
# Load files from csv
# Append each audio and label as one pair to list
# Convert from flac to wav
# Write each pair to tfrecord using writer

# %%
# Define constants

sr = 16000
maxlen = 18
maxlen_subwords = 100
minlen_text = 1
global_count = 0

# %%
import io
from pydub import AudioSegment, playback

audios = []

with open('../../data/ls-audios.txt') as f:
    audios = f.read().splitlines()

for a in audios:
    print(a)
    f = AudioSegment.from_file(a, format='flac')
    stream = io.BytesIO()
    w = f.export(stream, format='wav')
    playback.play(AudioSegment.from_wav(w))
    break
