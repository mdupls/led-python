# main.py

from hardware import Pin, NeoPixel

# Use exactly like you would with MicroPython:
status_led = Pin(33, Pin.OUT, value=0)
status_led.on()

strip = NeoPixel(17, 10)
strip[0] = (255, 0, 0)
strip.write()
