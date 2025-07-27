from utils import clear, OFF
from effect import BaseEffect

class SolidWipeEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self.direction = -1 if self.reverse else 1
        self._reset = False
        self.reset()
        
    def reset(self):
        self.step = self.end if self.reverse else self.start
        
        if self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            self.clear()
            self.reset()
            self._reset = False

        self.pixels[self.step] = self.color

        self.step += self.direction

        if self.step < self.start or self.step > self.end:
            self._reset = True
