from utils import OFF
from effect import BaseEffect

class BounceEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self.direction = -1 if self.reverse else 1
        self.step = self.end if self.reverse else self.start
        self._bounce = False

    def update(self):
        # keep track of the direction
        direction = self.direction

        if self.reverse:
            if self.step == self.end:
                self._change_color()
        else:
            if self.step == self.start:
                self._change_color()

        self.pixels[self.range_mod(self.step - direction)] = OFF  # Clear previous pixel
        self.pixels[self.step] = self.color

        # if we bounced, reverse the direction
        if self._bounce:
            self.direction *= -1
            self._bounce = False

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step == self.start or self.step == self.end:
            self._bounce = True

    def _change_color(self):
        if self.color_fn is not None:
            self.color = self.color_fn()
