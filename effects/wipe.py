from utils import OFF
from effect import BaseEffect

class WipeEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self.reset()

    def reset(self):
        super().reset()
        if self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        self.pixels[self.range_mod(self.step - self.direction)] = OFF  # Clear previous pixel
        self.pixels[self.step] = self.color

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step < self.start or self.step > self.end:
            self.reset()
