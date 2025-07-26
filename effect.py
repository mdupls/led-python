class BaseEffect:
    def __init__(self):
        self.strip = None

    def initialize(self, strip):
        self.strip = strip
        self.pixels = strip.pixels
        self.num_pixels = len(strip.pixels)

    def update(self):
        raise NotImplementedError
    
    def next_delay_ms(self) -> int:
        """
        Optional: Return delay until next update.
        Default is fixed.
        """
        return 50

