from utils import clear, OFF
from effect import BaseEffect

class BounceEffect(BaseEffect):
    def __init__(self, pixels, segment, color_fn=None, color=None):
        super().__init__(pixels, segment)
        self.color_fn = color_fn
        self.color = color
        self.direction = -1 if self.reverse else 1
        self.step = self.end if self.reverse else self.start
        self._bounce = False
        self.speed = int(segment.length / 16)

    def update(self):
        step = self.step
        direction = self.direction
        start = self.start
        end = self.end
        reverse = self.reverse

        # Check for color change at ends
        if (reverse and step == end) or (not reverse and step == start):
            if self.color_fn is not None:
                self.color = self.color_fn()

        # Clear previous pixel
        # self.pixels[self.range_mod(step - direction)] = OFF
        clear(self.pixels, start, end + 1)

        # Set current pixel
        self.pixels[step] = self.color

        # Bounce logic
        if self._bounce:
            self.direction = -direction
            self._bounce = False

        # Move step
        step += self.direction * self.speed
        self.step = step % (self.end + 1)

        # Check if at boundary
        if step == start or step == end:
            self._bounce = True
