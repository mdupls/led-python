from utils import rand_color, OFF
from effect import BaseEffect

class WipeRandomEffect(BaseEffect):
    def __init__(self, color_fn=None):
        super().__init__()
        self.color_fn = color_fn

    def initialize(self, strip):
        super().initialize(strip)

        self.reset()

    def update(self):
        self.pixels[(self.step - self.direction) % self.num_pixels] = OFF  # Clear previous pixel
        self.pixels[self.step] = self.color_fn()

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step < 0 or self.step == self.num_pixels:
            self.reset()
