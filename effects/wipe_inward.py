from utils import clear, OFF
from effect import BaseEffect

class WipeInwardEffect(BaseEffect):
    def __init__(self, color_fn=None, color=None):
        super().__init__()
        self.color_fn = color_fn
        self.color = color if color is not None else color_fn()
        self.step = 0  # Current step of the wipe

    def setStrip(self, strip):
        super().setStrip(strip)

        self.mid = self.num_pixels // 2
        self.max_step = self.mid  # How many steps to complete
    
    def update(self):
        # Light from both ends inward
        left = self.step
        right = self.num_pixels - 1 - self.step

        self.pixels[left] = self.color
        self.pixels[right] = self.color

        self.step += 1

        if self.step > self.max_step:
            clear(self.pixels)  # Clear the strip when done
            self.step = 0  # Reset step for next run
            if self.color_fn is not None:
                self.color = self.color_fn()