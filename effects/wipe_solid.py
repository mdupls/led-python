from utils import clear, OFF
from effect import BaseEffect

class WipeSolidEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self._reset = False
        self.reset()

        print(f"{self.start} {self.end}")
        
    def reset(self):
        super().reset()
        if self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            clear(self.pixels, self.start, self.end + 1)
            self.reset()
            self._reset = False

        self.pixels[self.step] = self.color

        self.step += self.direction

        if self.step <= self.start or self.step >= self.end:
            self._reset = True
