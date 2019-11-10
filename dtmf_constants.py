import numpy as np



CFG_SAMPLING_RATE = 8000
CFG_CHUNK_SIZE = 205
CFG_DETECT_THRESHOLD = 1000
SAMPLE_COUNT = CFG_CHUNK_SIZE
SAMPLE_FREQ = CFG_SAMPLING_RATE
FREQ_ROWS = np.array([697 , 770 , 852 , 941 ])
FREQ_COLS = np.array([1209, 1336, 1477, 1633])

CONST_K = np.floor([ 
            0.5 + SAMPLE_COUNT * FREQ_ROWS / SAMPLE_FREQ,
            0.5 + SAMPLE_COUNT * FREQ_COLS / SAMPLE_FREQ
          ])
CONST_W = 2 * np.pi * CONST_K / SAMPLE_COUNT
CONST_COEFF = 2 * np.cos(CONST_W)



DTMF_KEYCODING = np.array([
	['1', '2', '3', 'A'],
	['4', '5', '6', 'B'],
	['7', '8', '9', 'C'],
	['*', '0', '#', 'D']
	])
