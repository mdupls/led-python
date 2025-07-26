from utils import OFF
from effect import BaseEffect
import random

class SparkleEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color

    def update(self):
        for i in range(self.num_pixels):
            if random.getrandbits(3) == 0:
                self.pixels[i] = self.color_fn() if self.color_fn is not None else self.color
            else:
                self.pixels[i] = OFF
