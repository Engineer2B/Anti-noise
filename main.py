__author__ = 'Boris Breuer'

import pyaudio
import numpy as np
from utilities import printStatement
# import scipy.signal

CHUNK = 1024 * 2

WIDTH = 2
DTYPE = np.int16
MAX_INT = 32768.0

CHANNELS = 1
RATE = 11025 * 1
RECORD_SECONDS = 20

j = np.complex(0, 1)

pyAudio = pyaudio.PyAudio()

# Print input device information
pyAudio = pyaudio.PyAudio()
inputDevices = []
for indexDevice in range(1, pyAudio.get_device_count()):
    inputDevices.append(pyAudio.get_device_info_by_index(indexDevice))
printStatement.arbitraryobject(inputDevices)

stream = pyAudio.open(format=pyAudio.get_format_from_width(WIDTH),
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      output=True,
                      frames_per_buffer=CHUNK)

print("* recording")

# Initialize filter variables to array(1/(CHUNK*2)&,CHUNK*2)
filterValues = np.zeros(CHUNK * 2)
filterValues[:(2 * CHUNK)] = 1.
filterValues /= filterValues.sum()

lastFilterValues = filterValues
avg_freq_buffer = np.zeros(CHUNK)
obj = -np.inf
t = 10

# initialize sample buffer
buffer = np.zeros(CHUNK * 2)

# for i in np.arange(RATE / CHUNK * RECORD_SECONDS):
while True:
    # read audio
    ar1024strAudioChunk = stream.read(CHUNK)
    audio_data = np.fromstring(ar1024strAudioChunk, dtype=DTYPE)
    normalized_data = audio_data / MAX_INT
    freq_data = np.fft.fft(normalized_data)

    # synthesize audio
    buffer[CHUNK:] = np.random.randn(CHUNK)
    freq_buffer = np.fft.fft(buffer)
    # Calculate fast Fourier transform
    filterFFT = np.fft.fft(filterValues)
    freq_synth = filterFFT * freq_buffer
    synth = np.real(np.fft.ifft(freq_synth))

    # adjust fir
    # objective is to make abs(freq_synth) as much like long-term average of freq_buffer
    MEMORY = 100
    avg_freq_buffer = (avg_freq_buffer * MEMORY + np.abs(freq_data)) / (MEMORY + 1)
    obj_last = obj

    obj = np.real(np.dot(avg_freq_buffer[1:51], np.abs(freq_synth[1:100:2])) / np.dot(freq_synth[1:100:2],
                                                                                      np.conj(freq_synth[1:100:2])))
    if not np.isnan(obj):
        if np.isnan(obj_last):
            lastFilterValues = filterValues
        elif obj > obj_last:
            lastFilterValues = filterValues
    filterValues = lastFilterValues.copy()

    # adjust filter in frequency space
    filterFFT = np.fft.fft(filterValues)
    # t += np.clip(np.random.randint(3)-1, 0, 64)
    t = np.random.randint(100)

    filterFFT[t] += np.random.randn() * .05

    # transform frequency space filter to time space, click-free
    filterValues = np.real(np.fft.ifft(filterFFT))
    filterValues[:CHUNK] *= np.linspace(1., 0., CHUNK) ** .1
    filterValues[CHUNK:] = 0

    # move chunk to start of buffer
    buffer[:CHUNK] = buffer[CHUNK:]

    # write audio
    audio_data = np.array(np.round_(synth[CHUNK:] * MAX_INT), dtype=DTYPE)
    ar1024strAudioChunk = audio_data.tostring()
    stream.write(ar1024strAudioChunk, CHUNK)

print("* done")

stream.stop_stream()
stream.close()

pyAudio.terminate()
