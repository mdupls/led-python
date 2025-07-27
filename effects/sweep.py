from utils import OFF
from effect import BaseEffect

class SweepEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self.direction = -1 if self.reverse else 1
        self._reset = False
        self._clearing_pass = False
        self.reset()

    def reset(self, new_color=True):
        self.step = self.end if self.reverse else self.start
        if new_color and self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            self.reset(new_color=self._clearing_pass)
            self._clearing_pass = not self._clearing_pass
            self._reset = False

        self.pixels[self.step] = OFF if self._clearing_pass else self.color

        self.step += self.direction

        if self.step < self.start or self.step > self.end:
            self._reset = True
