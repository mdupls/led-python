from utils import clear, OFF
from effect import BaseEffect

class WipeInwardEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None, invert=False):
        super().__init__()
        self.color_fn = color_fn
        self.color = color
        self.invert = invert
        self._reset = False

    def initialize(self, strip):
        super().initialize(strip)
        
        self.reset()

    def reset(self):
        if self.invert:
            if self.num_pixels % 2 == 0:
                self.right = self.num_pixels // 2
                self.left = self.right - 1
            else:
                self.left = self.right = self.num_pixels // 2
        else:
            self.left = 0
            self.right = self.num_pixels - 1
        
        if self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            clear(self.pixels)
            self.reset()
            self._reset = False

        self.pixels[self.left] = self.color
        self.pixels[self.right] = self.color

        self.left += self.direction
        self.right -= self.direction

        if self.invert:
            if self.left < 0 or self.right >= self.num_pixels:
                self._reset = True
        else:
            if self.left > self.right:
                self._reset = True