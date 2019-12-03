import pyaudio
import numpy as np
import scipy
import scipy.fftpack
import time
import msvcrt
import matplotlib.pyplot as plt
import curses
from dtmf_constants import *



class DTMFKeyPressListener:
    def __init__(self, observable):
        observable.addOnKeyPressListener(self)
    
    def onDTMFKeyPress(self, source, keyPressed):
        print('Pressed ', keyPressed)
		
class QueuedDTMFKeyListener(DTMFKeyPressListener):
	def __init__(self, observable, q):
		super().__init__(observable)
		self.q = q;
	def onDTMFKeyPress(self, source, keyPressed):
		super().onDTMFKeyPress(source, keyPressed)
		self.q.put(keyPressed)
class DTMFMicrophoneReader:
	def __init__(self, audioStream, detectionThreshold):
		self._keyPressListeners = []
		self._pauseDetected = False
		self.detectionThreshold = detectionThreshold
		self._audioStream = audioStream
		self._Q0 = np.zeros((2,4))
		self._Q1 = np.zeros((2,4))
		self._Q2 = np.zeros((2,4))
		self._lastKey = None
		self._audioStream.start_stream()
		self._keepSampling = True
	def addOnKeyPressListener(self, listener):
		self._keyPressListeners.append(listener)
	def onKeyPress(self, keyPressed):
		for observer in self._keyPressListeners:
			observer.onDTMFKeyPress(self, keyPressed)
	def sample(self):
		audio_data = np.fromstring( self._audioStream.read(CFG_CHUNK_SIZE, False), dtype = np.int16 )
		#dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))

		for sampleIndex in range(SAMPLE_COUNT):
			self._Q0 = CONST_COEFF * self._Q1 - self._Q2 + audio_data[sampleIndex]
			
			self._Q2 = self._Q1
			self._Q1 = self._Q0
		magnitude_sq = (self._Q1 * self._Q1) + (self._Q2 * self._Q2) - (self._Q1 * self._Q2 * CONST_COEFF)
		mgn = np.sqrt(magnitude_sq) / SAMPLE_COUNT
		self._Q0.fill(0)
		self._Q1.fill(0)
		self._Q2.fill(0)
		maxRow = np.argmax(mgn[0,:])
		maxCol = np.argmax(mgn[1,:])
		
		maxRowVal = mgn[0, maxRow]
		maxColVal = mgn[1, maxCol]
		if(maxRowVal > self.detectionThreshold and maxColVal > self.detectionThreshold and self._pauseDetected):
			keyCode = DTMF_KEYCODING[maxRow, maxCol]
			self._pauseDetected = False
			self.onKeyPress(keyCode)
		elif(maxRowVal < self.detectionThreshold and maxColVal < self.detectionThreshold):
			self._pauseDetected = True
	def sampleLoop(self):
		while(self._keepSampling):
			self.sample()
	def sampleStop(self):
		self._keepSampling = False

			
		
	

