from effect import BaseEffect

class InwardWipeEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None, invert=False):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self.invert = invert
        self.direction = -1 if self.invert else 1
        self._even = self.length % 2 == 0
        self._reset = False
        self.reset()

    def reset(self):
        if self.invert:
            if self._even:
                self.right = self.start + (self.length // 2)
                self.left = self.right - 1
            else:
                self.left = self.right = self.start + (self.length // 2)
        else:
            self.left = self.start
            self.right = self.end
        
        if self.color_fn is not None:
            self.color = self.color_fn()

    def update(self):
        if self._reset:
            self.clear()
            self.reset()
            self._reset = False

        self.pixels[self.left] = self.color
        self.pixels[self.right] = self.color

        print(f"{self.segment}: (left, right) ({self.left}, {self.right})")

        self.left += self.direction
        self.right -= self.direction

        if self.invert:
            if self.left < self.start or self.right > self.end:
                self._reset = True
        else:
            if self.left > self.right:
                self._reset = True