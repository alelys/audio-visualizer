import numpy as np
import sounddevice as sd
from .config import SAMPLE_RATE, BUFFER_SIZE, CHUNK, DEVICE_INDEX


audio_buffer = np.zeros(BUFFER_SIZE, dtype=np.float32)

# Callback function that continuously updates the audio buffer with new audio samples from the input stream

def audio_callback(indata, frames, time_info, status):
    global audio_buffer

    if status:
        print("Audio status:", status)

    audio_buffer = np.roll(audio_buffer, -frames)
    audio_buffer[-frames:] = indata[:, 0]
