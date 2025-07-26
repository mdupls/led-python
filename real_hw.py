# real_hw.py

from machine import Pin, Timer
from scheduler import Scheduler as SchedulerInterface, Timer as TimerInterface
import neopixel

# Direct pass-through:
NeoPixel = neopixel.NeoPixel

class Timer(TimerInterface):
    def __init__(self, root):
        self.root = root

    def after(self, delay_ms, callback):
        self.root.after(delay_ms, callback)

class Scheduler(SchedulerInterface):
    def __init__(self):
        self.timer = Timer(-1)

    def after(self, interval_ms, callback):
        self.timer.init(
            period=interval_ms,
            mode=Timer.PERIODIC,
            callback=callback
        )

    def stop(self):
        self.timer.deinit()
