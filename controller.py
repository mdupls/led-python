from hardware import t

class Controller:
    def __init__(self, strip, runtime, debug=True):
        self.runtime = runtime
        self.strip = strip
        self.effects = [None] * len(strip.segments)
        self.speed_ms = 16
        self._stopped = True
        self._use_timer = t is not None
        self.DEBUG = debug

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

        use_timer = self._use_timer

        if use_timer:
            effect_start_time = t.ticks_ms()

        for effect in self.effects:
            if effect:
                effect.update()

        if use_timer:
            start_time = t.ticks_ms()

        self.strip.pixels.write()

        if use_timer and self.DEBUG:
            done_time = t.ticks_ms()

            # Debug on desktop:
            # print(
            #     f"Total Elapsed time updating channel {self.strip.id}: "
            #     f"effects: {t.ticks_diff(start_time, effect_start_time):.6f}ms "
            #     f"write: {t.ticks_diff(done_time, start_time):.6f}ms"
            # )

            print(
                f"Total Elapsed time updating channel {self.strip.id}: "
                f"effects: {t.ticks_diff(start_time, effect_start_time)}ms "
                f"write: {t.ticks_diff(done_time, start_time)}ms"
            )

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