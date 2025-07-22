# fake_hw.py

import tkinter as tk

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
        if bpp == 3:
            self.pixels = [(0, 0, 0)] * n
        else:
            self.pixels = [(0, 0, 0, 0)] * n  # start off
        self.window = tk.Tk()
        self.window.title(f"NeoPixel Strip on Pin {pin}")
        self.canvas = tk.Canvas(self.window, width=n * 30, height=50, bg="black")
        self.canvas.pack()
        self.rects = []
        for i in range(n):
            rect = self.canvas.create_rectangle(
                i * 30, 0, i * 30 + 28, 50, fill="black"
            )
            self.rects.append(rect)
        self.window.update()
        print(f"[MockNeoPixel] Created {n} pixels on pin {pin}")

    def __setitem__(self, index, color):
        print(f"[MockNeoPixel] Pixel {index} set to {color}")
        self.pixels[index] = color

    def __len__(self):
        return len(self.pixels)

    def write(self):
        print(f"[MockNeoPixel] Pixels updated: {self.pixels}")
        for i, color in enumerate(self.pixels):
            if self.bpp == 3:
                r, g, b = color
            elif self.bpp == 4:
                r, g, b, w = color
                # blend white channel for visualization
                r = min(255, r + w)
                g = min(255, g + w)
                b = min(255, b + w)
            else:
                r = g = b = 0
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(self.rects[i], fill=hex_color)
        self.window.update()