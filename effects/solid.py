from effect import BaseEffect
from utils import rand_color

class SolidEffect(BaseEffect):
    def __init__(self, pixels, segment, color=rand_color(w=0)):
        super().__init__(pixels, segment)
        self.color = color

    def update(self):
        for i in range(self.start, self.end + 1):
            self.pixels[i] = self.color

    def next_delay_ms(self) -> int:
        return -1 # No refresh needed, solid color effect does not change