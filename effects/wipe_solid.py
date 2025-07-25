from utils import clear, OFF
from effect import BaseEffect

class WipeSolidEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color
        self._reset = False

    def initialize(self, strip):
        super().initialize(strip)

        self.reset()

    def reset(self):
        super().reset()
        if self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            clear(self.pixels)
            self.reset()
            self._reset = False

        self.pixels[self.step] = self.color

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step < 0 or self.step == self.num_pixels:
            self._reset = True
