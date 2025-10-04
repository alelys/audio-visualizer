import time
import numpy as np
import sounddevice as sd

import visualizer.audio
from visualizer.leds import pixels, xy_to_num, wheel
from visualizer.spectrum import get_levels_for_bins, smooth_spectrum
from visualizer.config import (
    WIDTH, FRAME_DELAY, COLOR_STEP, N_RAINBOWS,
    DEVICE_INDEX, SAMPLE_RATE, CHUNK
)

color_offset = 0
old_spectrum = np.zeros(WIDTH)
spectrum = np.zeros(WIDTH)
       

if __name__ == "__main__":
    try:
        with sd.InputStream(device=DEVICE_INDEX,
                            callback=visualizer.audio.audio_callback,
                            channels=1,
                            samplerate=SAMPLE_RATE,
                            blocksize=CHUNK):

            print("Visualizer is working...")
            
            while True:
                start_time = time.time()

                 # FFT + smoothing
                spectrum = get_levels_for_bins(samples=visualizer.audio.audio_buffer)
                spectrum = smooth_spectrum(spectrum, old_spectrum)

                # Coloring LEDs
                pixels.fill((0, 0, 0))

                for x in range(WIDTH):
                    level = int(spectrum[x])
                    color_pos = int((x / WIDTH * 256 * N_RAINBOWS)) + color_offset
                    color_pos = color_pos % 256

                    for y in range(level):
                        index = xy_to_num(x + 1, y + 1)
                        pixels[index] = wheel(color_pos) 

                pixels.show()

                old_spectrum = spectrum
                color_offset = (color_offset + COLOR_STEP) % 256

                # FPS control
                elapsed_time = time.time() - start_time
                sleep_time = max(0, FRAME_DELAY - elapsed_time)
                time.sleep(sleep_time)


    except KeyboardInterrupt:
        print("Finished.")
        pixels.fill((0, 0, 0))
        pixels.show()
        sd.stop()

   