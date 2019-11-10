import pyaudio
import numpy as np
import scipy
import scipy.fftpack
import time
import msvcrt
import matplotlib.pyplot as plt
import curses
stdscr = curses.initscr()
CFG_SAMPLING_RATE = 8000
CFG_CHUNK_SIZE = 205
CFG_DETECT_THRESHOLD = 1000
SAMPLE_COUNT = CFG_CHUNK_SIZE
SAMPLE_FREQ = CFG_SAMPLING_RATE
FREQ_ROWS = np.array([697 , 770 , 852 , 941 ])
FREQ_COLS = np.array([1209, 1336, 1477, 1633])



CONST_K = np.floor([ 
            [0.5 + SAMPLE_COUNT * FREQ_ROWS / SAMPLE_FREQ],
            [0.5 + SAMPLE_COUNT * FREQ_COLS / SAMPLE_FREQ]
          ])
CONST_W = 2 * np.pi * CONST_K / SAMPLE_COUNT
CONST_COEFF = 2 * np.cos(CONST_W)

Q0 = np.zeros((2,4))
Q1 = np.zeros((2,4))
Q2 = np.zeros((2,4))
print(CONST_K)
i=0
f,ax = plt.subplots(2)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,205)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,4000)
ax[1].set_ylim(-10,100)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

if __name__=="__main__":
	pAudio = pyaudio.PyAudio()
	stream = pAudio.open(
		format = pyaudio.paInt16, 
		channels = 1, 
		rate = CFG_SAMPLING_RATE,
		input = True,
		frames_per_buffer = CFG_CHUNK_SIZE
		)
	exit = False
	stream.start_stream()
	while(not exit):
		try:
			audio_data = np.fromstring( stream.read(CFG_CHUNK_SIZE, False), dtype = np.int16 )
			dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))

			li.set_xdata(np.arange(len(audio_data)))
			li.set_ydata(audio_data)
			li2.set_xdata(np.arange(len(dfft))*CFG_SAMPLING_RATE/CFG_CHUNK_SIZE)
			li2.set_ydata(dfft)

			plt.pause(0.01)
			
			for sampleIndex in range(SAMPLE_COUNT):
				Q0 = CONST_COEFF * Q1 - Q2 + audio_data[sampleIndex]
				Q2 = Q1
				Q1 = Q0
			

			
			
			
			magnitude_sq = (Q1 * Q1) + (Q2 * Q2) - (Q1 * Q2 * CONST_COEFF)
			mgn = np.sqrt(magnitude_sq) / SAMPLE_COUNT

			
			stdscr.erase()
			stdscr.addstr(0,0,np.array_str(mgn))
		#	stdscr.addstr(0,0, "|      | %4d | %4d | %4d | %4d |" % (FREQ_COLS[0],FREQ_COLS[1],FREQ_COLS[2],FREQ_COLS[3]))
		#	stdscr.addstr(1,0, "| %4d | %4f | %4f | %4f | %4f |" % (FREQ_ROWS[0], mgn[0,0], mgn[0,1], mgn[0,2], mgn[0,3]))
		#	stdscr.addstr(2,0, "| %4d | %4f | %4f | %4f | %4f |" % (FREQ_ROWS[1], mgn[1,0], mgn[1,1], mgn[1,2], mgn[1,3]))
		#	stdscr.addstr(3,0, "| %4d | %4f | %4f | %4f | %4f |" % (FREQ_ROWS[2], mgn[2,0], mgn[2,1], mgn[2,2], mgn[2,3]))
		#	stdscr.addstr(4,0, "| %4d | %4f | %4f | %4f | %4f |" % (FREQ_ROWS[3], mgn[3,0], mgn[3,1], mgn[3,2], mgn[3,3]))			
			Q0.fill(0)
			Q1.fill(0)
			Q2.fill(0)
			stdscr.refresh()
		except KeyboardInterrupt:
			exit=True
	stream.stop_stream()
	stream.close()
	pAudio.terminate()
