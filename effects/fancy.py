from utils import rand_color, OFF
from effect import BaseEffect

class FancyEffect(BaseEffect):
    def __init__(self):
        super().__init__()
        self.step = 0

    def update(self):
        self.strip[(self.step - 1) % self.num_pixels] = OFF  # Clear previous pixel
        self.strip[self.step % self.num_pixels] = rand_color()

        self.step += 1