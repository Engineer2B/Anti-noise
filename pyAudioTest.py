__author__ = 'Boris Breuer'
from utilities import printStatement
import pyaudio

pyAudio = pyaudio.PyAudio()
inputDevices = []
for indexDevice in range(1, pyAudio.get_device_count()):
    inputDevices.append(pyAudio.get_device_info_by_index(indexDevice))
printStatement.arbitraryobject(inputDevices)