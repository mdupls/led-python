from utils import OFF
from effect import BaseEffect

class SweepEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color
        self._reset = False
        self._clearing_pass = False

    def initialize(self, strip):
        super().initialize(strip)

        self.reset()

    def reset(self, new_color=True):
        self.step = self.num_pixels - 1 if self.reverse else 0
        if new_color and self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            self.reset(new_color=self._clearing_pass)
            self._clearing_pass = not self._clearing_pass
            self._reset = False

        direction = -1 if self.reverse else 1

        self.pixels[self.step] = OFF if self._clearing_pass else self.color

        # Move the LED
        self.step += direction

        # Bounce off ends
        if self.step < 0 or self.step == self.num_pixels:
            self._reset = True
