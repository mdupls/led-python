class BaseEffect:
    def __init__(self):
        self.strip = None

    def initialize(self, strip):
        self.strip = strip
        self.pixels = strip.pixels
        self.num_pixels = len(strip.pixels)
        self.reverse = strip.reverse
        self.direction = -1 if strip.reverse else 1

    def reset(self):
        self.step = self.num_pixels - 1 if self.reverse else 0

    def update(self):
        raise NotImplementedError
    
    def next_delay_ms(self) -> int:
        """
        Optional: Return delay until next update.
        Default is fixed.
        """
        return 50

