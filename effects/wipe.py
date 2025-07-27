from utils import OFF
from effect import BaseEffect

class WipeEffect(BaseEffect):
    def __init__(self, segment, color_fn=None, color=None):
        super().__init__(segment)
        self.color_fn = color_fn
        self.color = color if color is not None else color_fn()

    def initialize(self, strip):
        super().initialize(strip)

        self.reset()

    def update(self):
        self.pixels[(self.step - self.direction) % self.num_pixels] = OFF  # Clear previous pixel
        self.pixels[self.step] = self.color

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step < 0 or self.step == self.num_pixels:
            self.reset()
            if self.color_fn is not None:
                self.color = self.color_fn()
