from utils import OFF
from effect import BaseEffect

class RandomWipeEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.direction = -1 if self.reverse else 1
        self.reset()

    def update(self):
        self.pixels[self.range_mod(self.step - self.direction)] = OFF  # Clear previous pixel
        self.pixels[self.step] = self.color_fn()

        # Move the LED
        self.step += self.direction

        # Reach the end
        if self.step < self.start or self.step > self.end:
            self.reset()
