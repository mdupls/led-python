from effect import BaseEffect

rainbow_colors = [(255, 0, 0, 128), (255, 127, 0, 128), (255, 255, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128), (75, 0, 130, 128), (148, 0, 211, 128)]

class RainbowCycleEffect(BaseEffect):
    def __init__(self, *args):
        super().__init__(*args)
        self.direction = -1 if self.reverse else 1
        self.step = self.end if self.reverse else self.start

    def update(self):
        for i in range(self.start, self.end + 1):
            # reverse the index
            j = i if self.reverse else self.end - i
            self.pixels[i] = rainbow_colors[(j + self.step * self.direction) % len(rainbow_colors)]

        step = self.step + self.direction

        if step < self.start:
            self.step = self.end
        elif self.step > self.end:
            self.step = self.start
        else:
            self.step = step
