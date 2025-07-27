from effect import BaseEffect

class RainbowWipeEffect(BaseEffect):
    def __init__(self, pixels, segment):
        super().__init__(pixels, segment)
        self.direction = -1 if self.reverse else 1
        self.step = 0

    def update(self):
        start = self.end if self.reverse else self.start
        stop = self.start - 1 if self.reverse else self.end + 1
        for i in range(start, stop, self.direction):
            # reverse the index
            j = i if self.reverse else self.start + self.end - i
            self.pixels[i] = self._wheel((j - self.step * self.direction) % 256)
        self.step = (self.step - self.direction) % 256

    def _wheel(self, step):
        # return rainbow color
        return (
            (step & 0xFF, (step + 85) & 0xFF, (step + 170) & 0xFF, 0)
        )
