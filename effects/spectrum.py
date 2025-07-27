from utils import hsv_to_rgb
from effect import BaseEffect
from random import randint

class SpectrumEffect(BaseEffect):

    def update(self):
        for i in self.range():
            hue = randint(50, 255)/255.0
            sat = randint(50, 255)/255.0
            brt = randint(0, 255)/255.0
        
            col = hsv_to_rgb(hue, sat, brt, 0)
            self.pixels[i] = col