import numpy as np
from .config import SAMPLE_RATE, BUFFER_SIZE, WIDTH, HEIGHT, VOL_MIN, VOL_MAX, MAX_FREQ, SKIP_BIN


# Precompute FFT bin mapping

freq_bins = np.fft.rfftfreq(BUFFER_SIZE, 1 / SAMPLE_RATE)       

MAX_BIN = np.argmax(freq_bins > MAX_FREQ)    
if MAX_BIN == 0:                                                       
    MAX_BIN = len(freq_bins)

freqs = np.fft.rfftfreq(BUFFER_SIZE, 1 / SAMPLE_RATE)[:MAX_BIN]      
f_min = freqs[SKIP_BIN] if freqs[0] == 0 else freqs[0]                 
log_edges = np.logspace(np.log10(f_min), np.log10(MAX_FREQ), WIDTH+1)   
bin_ranges = np.searchsorted(freqs, log_edges)    


# Perform FFT on audio samples and convert magnitude spectrum into bar heights

def get_levels_for_bins(samples):
    fft_vals = np.fft.rfft(samples * np.hanning(len(samples)))
    magnitudes = np.abs(fft_vals[:MAX_BIN])    

    bars = []

    for i in range(WIDTH):
        start_idx = bin_ranges[i]
        end_idx = bin_ranges[i+1]

        if start_idx == end_idx:
            value = magnitudes[start_idx] if start_idx < len(magnitudes) else 0
        else:
            value = np.sum(magnitudes[start_idx:end_idx])       

        bars.append(value)

    bars = np.log1p(bars)
    bars = np.interp(bars, [VOL_MIN, VOL_MAX], [0, HEIGHT])
    return np.clip(bars, 0, HEIGHT).astype(int)


# Smoothing

def smooth_spectrum(new_spectrum, old_spectrum):
    result = []
    for new, old in zip(new_spectrum, old_spectrum):
        if new > old:
            result.append(new)
        elif new < old:
            result.append(max(0, old - 1))
        else:
            result.append(old)
    return result    