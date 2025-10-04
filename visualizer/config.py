# LED Matrix
HEIGHT = 16
WIDTH = 48    

# LED (check mapping.png for details)
BLOCK_VERTICAL_PIXELS = 8                 
BLOCK_HORIZONTAL_PIXELS = 8            
VERTICAL_BLOCK_COUNT = 2
HORIZONTAL_BLOCK_COUNT = 6

# Audio
DEVICE_INDEX = 1            
SAMPLE_RATE = 44100     
CHUNK = 512
BUFFER_SIZE = CHUNK * 4       # bigger buffer -> smoother transitions
MAX_FREQ = 20000 
  
# VISUALIZATION
VOL_MIN = 0                   # increase value to get rid of noise        
VOL_MAX = 1.8                 # change value to adjust sensitivity
TARGET_FPS = 35
FRAME_DELAY = 1 / TARGET_FPS       
SKIP_BIN = 4                  # skipping initial frequency bins for better visualization
COLOR_STEP = 2                # higher value -> RGB colors change faster
N_RAINBOWS = 0.25             # amount of rainbows on strip (0.5 , 1 , 2...)



