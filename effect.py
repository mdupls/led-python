class BaseEffect:
    def __init__(self):
        self.strip = None
        self.num_pixels = 0

    def setStrip(self, strip):
        self.strip = strip
        self.num_pixels = len(strip)

    def update(self):
        raise NotImplementedError
    
    def next_delay_ms(self) -> int:
        """
        Optional: Return delay until next update.
        Default is fixed.
        """
        return 50

