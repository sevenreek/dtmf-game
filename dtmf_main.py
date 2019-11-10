import pyaudio
import numpy as np
from dtmf_class import *
from dtmf_constants import *
if __name__=="__main__":
	pAudio = pyaudio.PyAudio()
	stream = pAudio.open(
		format = pyaudio.paInt16, 
		channels = 1, 
		rate = CFG_SAMPLING_RATE,
		input = True,
		frames_per_buffer = CFG_CHUNK_SIZE
		) 
	micReader = DTMFMicrophoneReader(stream,1000)
	keyListener = DTMFKeyPressListener(micReader)
	exit = False
	print("Running sampler")
	while(not exit):
		try:
			micReader.sample()
		except KeyboardInterrupt:
			exit=True