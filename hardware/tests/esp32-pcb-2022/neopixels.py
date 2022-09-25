import asyncio
from rainbowio import colorwheel
from pinouts import pcb


@asyncio.coroutine
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        asyncio.sleep(wait)

RED    = (255,   0,   0)
YELLOW = (255, 150,   0)
GREEN  = (  0, 255,   0)
CYAN   = (  0, 255, 255)
BLUE   = (  0,   0, 255)
PURPLE = (180,   0, 255)
WHITE  = (255, 255, 255)
OFF    = (  0,   0,   0)

pcb.pixels.fill(RED)
pcb.pixels.show()
