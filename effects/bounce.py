from utils import clear, OFF
from effect import BaseEffect

class BounceEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color
        self._bounce = False

    def initialize(self, strip):
        super().initialize(strip)

        self.reset()

    def update(self):
        # keep track of the direction
        direction = self.direction

        if self.reverse:
            if self.step == self.num_pixels - 1:
                self._change_color()
        else:
            if self.step == 0:
                self._change_color()

        self.pixels[(self.step - direction) % self.num_pixels] = OFF  # Clear previous pixel
        self.pixels[self.step] = self.color

        # if we bounced, reverse the direction
        if self._bounce:
            self.direction *= -1
            self._bounce = False

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step == 0 or self.step == self.num_pixels - 1:
            self._bounce = True

    def _change_color(self):
        if self.color_fn is not None:
            self.color = self.color_fn()
