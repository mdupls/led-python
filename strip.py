from hardware import Pin, NeoPixel

RGB_BPP = 3 # RGB leds
RGBW_BPP = 4  # RGBW LEDs
TIM_400 = 0 # 400kHz leds
TIM_800 = 1 # 800kHz leds
RGB_PIXELS = 1 # RGB, 1 led=1 pixel

class Strip:
    def __init__(self, id, pin_num, num_leds, bpp=3, timing=TIM_400, reverse=False, rotation=0, enabled=False):
        self.id = id
        self.reverse = reverse
        self.enabled = enabled
        self.rotation = rotation
        self.pixels = NeoPixel(Pin(pin_num), num_leds, bpp=bpp, timing=timing)
        
        # # Could better insolate this from MicroPython NeoPixel scenarios
        # # This is for testing purposes only on a desktop
        # if self.pixels.window is not None:
        #     self.pixels.setup_canvas(rotation)
    
    def get_id(self):
        return self.id