from utils import clear, OFF
from effect import BaseEffect

class RainbowWipeEffect(BaseEffect):
    def __init__(self):
        super().__init__()
        self.step = 0

    def wheel(self, step):
        # return rainbow color
        return (
            (step & 0xFF, (step + 85) & 0xFF, (step + 170) & 0xFF, 0)
        )

    def update(self):
        for i in range(self.num_pixels):
            self.strip[i] = self.wheel((i + self.step) % 256)
        self.step = (self.step + 1) % 256
