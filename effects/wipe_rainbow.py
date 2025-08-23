from effect import BaseEffect

class RainbowWipeEffect(BaseEffect):
    def __init__(self, pixels, segment):
        super().__init__(pixels, segment)
        self.direction = -1 if self.reverse else 1
        self._wheels = [(step & 0xFF, (step + 85) & 0xFF, (step + 170) & 0xFF, 0) for step in range(256)]
        self.step = 0

        if self.reverse:
            s1 = self.end
            s2 = self.start - 1
        else:
            s1 = self.start
            s2 = self.end + 1

        self.range = range(s1, s2, self.direction)

    def update(self):
        start, end, step, direction = self.start, self.end, self.step, self.direction
        reverse = self.reverse
        wheels = self._wheels
        pixels = self.pixels
        rng = self.range

        base = step * direction

        if reverse:
            for i in rng:
                pixels[i] = wheels[(i - base) & 0xFF]
        else:
            total = start + end
            for i in rng:
                pixels[i] = wheels[(total - i - base) & 0xFF]

        self.step = (step - direction) & 0xFF
