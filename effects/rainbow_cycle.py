from effect import BaseEffect

rainbow_colors = [(255, 0, 0, 128), (255, 127, 0, 128), (255, 255, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128), (75, 0, 130, 128), (148, 0, 211, 128)]

class RainbowCycleEffect(BaseEffect):
    def __init__(self):
        super().__init__()

    def initialize(self, strip):
        super().initialize(strip)

        self.reset()

    def update(self):
        for i in range(self.start, self.end + 1):
            # reverse the index
            j = i if self.reverse else self.num_pixels - i - 1
            self.pixels[i] = rainbow_colors[(j + self.step * self.direction) % len(rainbow_colors)]

        self.step = (self.step + self.direction) % self.num_pixels
