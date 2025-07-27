class Controller:
    def __init__(self, strip, scheduler):
        self.scheduler = scheduler
        self.effects = []
        self.strip = strip
        self.speed_ms = 50

    def start(self):
        self.scheduler.start(self._update)

    def stop(self):
        self.scheduler.stop()

    def _update(self):
        # Run current pattern
        for i in range(len(self.effects)):
            effect = self.effects[i]
            effect.update()

        self.strip.pixels.write()

    def set_speed(self, speed_ms):
        self.speed_ms = speed_ms
        self.scheduler.interval_ms = speed_ms
        # Restart timer to apply new period
        self.stop()
        self.start()

    def set_effect_fn(self, effect_fn, **kwargs):
        delay = self.speed_ms
        self.effects = []
        for i in range(len(self.strip.segments)):
            effect = effect_fn(self.strip.pixels, self.strip.segments[i], **kwargs)
            segment_delay = effect.delay_ms()
            if segment_delay is not None:
                if segment_delay >= 0:
                    if delay > 0:
                        delay = min(delay, segment_delay)
                elif segment_delay < 0:
                    delay = segment_delay
            self.effects.append(effect)

        # A bit hacky, but attemping to handle effects that don't require timers such as solid colors
        if delay < 0:
            self.stop()
            self._update() # Run once
        else:
            self.set_speed(delay)