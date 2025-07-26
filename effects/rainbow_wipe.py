from utils import clear, OFF
from effect import BaseEffect

class RainbowWipeEffect(BaseEffect):
    def __init__(self):
        super().__init__()
        self.step = 0

    def update(self):
        start = self.num_pixels - 1 if self.reverse else 0
        stop = -1 if self.reverse else self.num_pixels
        for i in range(start, stop, self.direction):
            # reverse the index
            j = i if self.reverse else self.num_pixels - i - 1
            self.pixels[i] = self._wheel((j - self.step * self.direction) % 256)
        self.step = (self.step - self.direction) % 256

    def _wheel(self, step):
        # return rainbow color
        return (
            (step & 0xFF, (step + 85) & 0xFF, (step + 170) & 0xFF, 0)
        )
