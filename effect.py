class BaseEffect:
    def __init__(self, pixels, segment):
        self.pixels = pixels
        self.segment = segment
        self.start = segment.start
        self.end = self.start + segment.length - 1
        self.length = segment.length
        self.reverse = segment.reverse
        self.direction = -1 if self.reverse else 1

    def reset(self):
        self.step = self.end if self.reverse else self.start

    def update(self):
        raise NotImplementedError
    
    def next_delay_ms(self) -> int:
        """
        Optional: Return delay until next update.
        Default is fixed.
        """
        return 50

