from effect import BaseEffect

rainbow_colors = [(255, 0, 0, 128), (255, 127, 0, 128), (255, 255, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128), (75, 0, 130, 128), (148, 0, 211, 128)]

class RainbowCycleEffect(BaseEffect):
    def __init__(self):
        super().__init__()
        self.step = 0

    def update(self):
        for i in range(self.num_pixels):
            self.strip[i] = rainbow_colors[(i + self.step) % len(rainbow_colors)]

        self.step = (self.step + 1) % self.num_pixels
