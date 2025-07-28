class Controller:
    def __init__(self, strip, runtime):
        self.runtime = runtime
        self.strip = strip
        self.effects = [None] * len(self.strip.segments)
        self.speed_ms = 50
        self._stopped = True

    def start(self):
        self._stopped = False
        self.runtime.schedule_next(0, self._update)

    def stop(self):
        self._stopped = True

    def _next(self):
        self.runtime.schedule_next(self.speed_ms, self._update)

    def _update(self):
        if self._stopped:
            return
        
        # Run current pattern
        for i in range(len(self.effects)):
            effect = self.effects[i]
            if effect is not None:
                effect.update()

        self.strip.pixels.write()
        self._next()

    def set_speed(self, speed_ms):
        self.speed_ms = speed_ms

    def set_effect_fn(self, effect_fn, segment_index=None, **kwargs):
        if segment_index is None:
            self.effects = []
            for i in range(len(self.strip.segments)):
                effect = effect_fn(self.strip.pixels, self.strip.segments[i], **kwargs)
                self.effects.append(effect)
        else:
            effect = effect_fn(self.strip.pixels, self.strip.segments[segment_index], **kwargs)
            self.effects[segment_index] = effect