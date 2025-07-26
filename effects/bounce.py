from utils import OFF
from effect import BaseEffect

class BounceEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color if color is not None else color_fn()
        self.step = 0
        self.direction = 1

    def update(self):
        self.strip[(self.step - self.direction) % self.num_pixels] = OFF  # Clear previous pixel
        self.strip[self.step] = self.color

        # Move the LED
        self.step += self.direction

        # Bounce off ends
        if self.step == 0 or self.step == self.num_pixels - 1:
            self.direction *= -1  # Reverse direction
            if self.color_fn is not None:
                self.color = self.color_fn()
