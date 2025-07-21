# fake_hw.py

class Pin:
    OUT = "OUT"
    IN = "IN"

    def __init__(self, pin_num, mode=None, value=None):
        self.pin_num = pin_num
        self.mode = mode
        self.value = value
        print(f"[MockPin] Pin {pin_num} initialized as {mode} with value {value}")

    def on(self):
        print(f"[MockPin] Pin {self.pin_num} ON")
        self.value = 1

    def off(self):
        print(f"[MockPin] Pin {self.pin_num} OFF")
        self.value = 0

    def value(self, val=None):
        if val is None:
            return self.value
        else:
            print(f"[MockPin] Pin {self.pin_num} value set to {val}")
            self.value = val

class NeoPixel:
    def __init__(self, pin, n, bpp=3, timing=1):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.pixels = [(0, 0, 0)] * n
        print(f"[MockNeoPixel] Created {n} pixels on pin {pin}")

    def __setitem__(self, index, color):
        print(f"[MockNeoPixel] Pixel {index} set to {color}")
        self.pixels[index] = color

    def write(self):
        print(f"[MockNeoPixel] Pixels updated: {self.pixels}")
