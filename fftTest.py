__author__ = 'Boris Breuer'

import pyaudio
import numpy as np
import scipy.signal

CHUNK = 1024 * 2

WIDTH = 2
DTYPE = np.int16
MAX_INT = 32768.0

CHANNELS = 1
RATE = 11025 * 1
RECORD_SECONDS = 20

j = np.cdouble((0,1))

pyAudio = pyaudio.PyAudio()
stream = pyAudio.open(format=pyAudio.get_format_from_width(WIDTH),
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      output=True,
                      frames_per_buffer=CHUNK)

print("* recording")

# initialize filter variables
fir = np.zeros(CHUNK * 2)
fir[:(2 * CHUNK)] = 1.
fir /= fir.sum()

fir_last = fir
avg_freq_buffer = np.zeros(CHUNK)
obj = -np.inf
t = 10

# initialize sample buffer
buffer = np.zeros(CHUNK * 2)

from scipy.fftpack import fft
# Number of sample points
N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = fft(y)
yf2 = np.fft.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), round(N/2))
import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:round(N/2)]))
plt.grid()
plt.show()