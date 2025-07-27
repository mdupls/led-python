class Controller:
    def __init__(self, strip, scheduler):
        self.scheduler = scheduler
        self.effects = []
        self.strip = strip

    def start(self):
        self.scheduler.start(self._update)

    def stop(self):
        self.scheduler.stop()

    def _update(self):
        # Run current pattern
        for i in range(len(self.effects)):
            self.effects[i].update()

        self.strip.pixels.write()

    def set_speed(self, speed_ms):
        self.scheduler.interval_ms = speed_ms
        # Restart timer to apply new period
        self.stop()
        self.start()

    def set_effect_fn(self, effect_fn, **kwargs):
        self.effects = []
        for i in range(len(self.strip.segments)):
            self.effects.append(effect_fn(self.strip.pixels, self.strip.segments[i], **kwargs))