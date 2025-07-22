# main.py

from hardware import Pin, NeoPixel

if __name__ == "__main__":
    from time import sleep

    pin = Pin(17, Pin.OUT)
    strip = NeoPixel(17, 30, bpp=4)

    # Light up in sequence
    for i in range(strip.n):
        strip[i] = (0, 0, 255, 50)  # Blue + slight white
        strip.write()
        sleep(0.05)

    sleep(1)

    # Rainbow wipe
    colors = [
        (255, 0, 0, 0),
        (255, 127, 0, 0),
        (255, 255, 0, 0),
        (0, 255, 0, 0),
        (0, 0, 255, 0),
        (75, 0, 130, 0),
        (148, 0, 211, 0),
    ]
    for i in range(strip.n):
        strip[i] = colors[i % len(colors)]
    strip.write()

    sleep(2)

    # Clear
    for i in range(strip.n):
        strip[i] = (0, 0, 0, 0)
    strip.write()

    sleep(1)
