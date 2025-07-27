class Controller:
    def __init__(self, strip, scheduler):
        self.scheduler = scheduler
        self.strip = strip
        self.effects = [None] * len(self.strip.segments)
        self.speed_ms = 50

    def start(self):
        self.scheduler.start(self._update)

    def stop(self):
        self.scheduler.stop()

    def _update(self):
        # Run current pattern
        for i in range(len(self.effects)):
            effect = self.effects[i]
            if effect is not None:
                effect.update()

        self.strip.pixels.write()

    def set_speed(self, speed_ms):
        self.speed_ms = speed_ms
        self.scheduler.interval_ms = speed_ms
        # Restart timer to apply new period
        self.stop()
        self.start()

    def set_effect_fn(self, effect_fn, segment_index=None, **kwargs):
        if segment_index is None:
            self.effects = []
            for i in range(len(self.strip.segments)):
                effect = effect_fn(self.strip.pixels, self.strip.segments[i], **kwargs)
                self.effects.append(effect)
        else:
            effect = effect_fn(self.strip.pixels, self.strip.segments[segment_index], **kwargs)
            self.effects[segment_index] = effect