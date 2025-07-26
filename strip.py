from hardware import Pin, NeoPixel

RGB_BPP = 3 # RGB leds
RGBW_BPP = 4  # RGBW LEDs
TIM_400 = 0 # 400kHz leds
TIM_800 = 1 # 800kHz leds
RGB_PIXELS = 1 # RGB, 1 led=1 pixel

class Strip:
    def __init__(self, id, pin_num, num_leds, bpp=3, timing=TIM_400, direction=1, enabled=False):
        self.id = id
        self.direction = direction
        self.enabled = enabled
        self.pixels = NeoPixel(Pin(pin_num), num_leds, bpp=bpp, timing=timing)
    
    def get_id(self):
        return self.id