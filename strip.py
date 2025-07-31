from hardware import Pin, NeoPixel

RGB_BPP = 3 # RGB leds
RGBW_BPP = 4  # RGBW LEDs
TIM_400 = 0 # 400kHz leds
TIM_800 = 1 # 800kHz leds
RGB_PIXELS = 1 # RGB, 1 led=1 pixel

class Strip:
    def __init__(self, id, pin_num, num_leds, bpp=3, timing=TIM_400, segments=None, reverse=False, rotation=0, enabled=False):
        self.id = id
        self.enabled = enabled
        self.rotation = rotation
        self.pixels = NeoPixel(Pin(pin_num), num_leds, bpp=bpp, timing=timing)
        if segments is None:
            self.segments = [Segment(0, num_leds, reverse=reverse)]
        else:
            self.segments = segments
            self._validate_segments()
    
    def get_id(self):
        return self.id
    
    def _validate_segments(self):
        for i in range(len(self.segments)):
            segment = self.segments[i]
            index = segment.start + segment.length - 1
            if index >= len(self.pixels):
                raise RuntimeError(f"Segment lengths are out of bounds: (start, length) ({segment.start}, {segment.length}) for pixel length: {len(self.pixels)}")

class Segment:
    def __init__(self, start, length, reverse=False, enabled=True):
        self.start = start
        self.length = length
        self.reverse = reverse
        self.enabled = enabled

    def __len__(self):
        return self.length
    
    def __str__(self):
        return f"Segment [{self.start}, {self.start + self.length - 1}]"