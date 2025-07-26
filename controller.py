class Controller:
    def __init__(self, strip, scheduler):
        self.scheduler = scheduler
        self.effect = None
        self.strip = strip

    def start(self):
        self.scheduler.start(self._update)

    def stop(self):
        self.scheduler.stop()

    def _update(self):
        # Run current pattern
        if self.effect is not None:
            self.effect.update()
            self.strip.pixels.write()

    def set_speed(self, speed_ms):
        self.scheduler.interval_ms = speed_ms
        # Restart timer to apply new period
        self.stop()
        self.start()

    def set_effect(self, effect):
        effect.initialize(self.strip)
        self.effect = effect