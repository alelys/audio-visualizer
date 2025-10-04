import board
import neopixel
from .config import (
    BLOCK_HORIZONTAL_PIXELS, BLOCK_VERTICAL_PIXELS,
    HORIZONTAL_BLOCK_COUNT, VERTICAL_BLOCK_COUNT
)

# Matrix calculations

TOTAL_BLOCK_COUNT = VERTICAL_BLOCK_COUNT * HORIZONTAL_BLOCK_COUNT
BLOCK_SIZE = BLOCK_HORIZONTAL_PIXELS * BLOCK_VERTICAL_PIXELS
NUM_PIXELS = BLOCK_SIZE * TOTAL_BLOCK_COUNT


# Initialize NeoPixel LED matrix on pin D9

pixels = neopixel.NeoPixel(board.D9, NUM_PIXELS, brightness=0.1, auto_write=False)


# mapping function (check mapping.png for details)
# Maps 2D matrix coordinates (x, y) to LED index in NeoPixel strip.

def xy_to_num(x, y):   

    if x < 1 or x > HORIZONTAL_BLOCK_COUNT * BLOCK_HORIZONTAL_PIXELS:
        raise ValueError(f"x={x} out of bounds")
    if y < 1 or y > VERTICAL_BLOCK_COUNT * BLOCK_VERTICAL_PIXELS:
        raise ValueError(f"y={y} out of bounds")

    horizontal_block = 1 + (x-1)//BLOCK_HORIZONTAL_PIXELS       
    vertical_block = 1 + (y-1)//BLOCK_VERTICAL_PIXELS           
    x_in_block = (x-1) % BLOCK_HORIZONTAL_PIXELS + 1            
    y_in_block = (y-1) % BLOCK_VERTICAL_PIXELS + 1               

    mapping = x_in_block - y_in_block*8 + 63                    
    vertical_offset = (VERTICAL_BLOCK_COUNT-vertical_block) * BLOCK_SIZE * HORIZONTAL_BLOCK_COUNT 
    horizontal_offset = (horizontal_block-1) * BLOCK_SIZE  

    return mapping + horizontal_offset + vertical_offset


# generate RGB colors based on position (0-255)

def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)