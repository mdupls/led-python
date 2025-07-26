from utils import clear, OFF
from effect import BaseEffect

class WipeSolidEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color if color is not None else color_fn()
        self.step = 0
        self.reset = False
        self.direction = 1

    def update(self):
        if self.reset:
            clear(self.strip)
            self.reset = False
            self.step = 0
            if self.color_fn is not None:
                self.color = self.color_fn()

        self.strip[self.step] = self.color

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step == self.num_pixels:
            self.reset = True
