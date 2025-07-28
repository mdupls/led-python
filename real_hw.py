# real_hw.py

from machine import Pin
import uasyncio as asyncio
from runtime import Runtime as RuntimeInterface
import neopixel

# Direct pass-through:
NeoPixel = neopixel.NeoPixel

class Runtime(RuntimeInterface):

    def add(self, strip, x, y):
        pass

    def schedule_next(self, delay_ms, callback):
        asyncio.create_task(self._schedule(delay_ms, callback))

    async def _schedule(self, delay_ms, callback):
        await asyncio.sleep_ms(delay_ms)
        callback()

    def run(self):
        asyncio.run(self._main())

    async def _main(self):
        while True:
            await asyncio.sleep(1)  # Idle loop
