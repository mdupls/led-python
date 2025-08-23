# fake_hw.py

from runtime import Runtime as RuntimeInterface
import tkinter as tk
import time

class Pin:
    OUT = "OUT"
    IN = "IN"

    def __init__(self, pin_num, mode=None, value=None):
        self.pin_num = pin_num
        self.mode = mode
        self.value = value
        # print(f"[MockPin] Pin {pin_num} initialized as {mode} with value {value}")

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
        
        # print(f"[MockNeoPixel] Created {n} pixels on pin {pin}")

    def add_renderer(self, renderer, x, y, w, h, rotation=0):
        self.renderer = renderer
        self.window = renderer.window
        self.canvas = renderer.canvas
        thick = 5

        if rotation == 90 or rotation == 270:
            rect_fn = lambda i: (
                x, y + i * h, x + w + thick, y + (i + 1) * h
            )
        elif rotation == 180 or rotation == 0:
            rect_fn = lambda i: (
                x + i * w, y, x + (i + 1) * w, y + h + thick
            )

        self.rects = []

        for i in range(self.n):
            rect = self.canvas.create_rectangle(
                *rect_fn(i), fill="white", outline="black"
            )
            self.rects.append(rect)
        self.window.update()

    def __setitem__(self, index, color):
        # print(f"[MockNeoPixel] Pixel {index} set to {color}")
        self.pixels[index] = color

    def __len__(self):
        return len(self.pixels)

    def write(self):
        # print(f"[MockNeoPixel] Pixels updated: {len(self.pixels)}")
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

class Runtime(RuntimeInterface):
    def __init__(self):
        self.window = tk.Tk()

        # Set desired window size
        window_width = 1400
        window_height = 1000

        self.window_width = window_width
        self.window_height = window_height

        # Get screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the geometry
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.window.title(f"LED Python")
        self.canvas = tk.Canvas(self.window, width=window_width, height=window_height, bg="gray")
        self.canvas.pack()
        self.strips = []
        self.padding = 20

    def add(self, strips):
        self.strips = strips

        window_width = self.window_width - self.padding * 3
        window_height = self.window_height - self.padding * 2

        x = 0
        y = 0

        w = 10000
        h = 10000
        for i in range(len(strips)):
            strip = strips[i]
            rotation = strip.rotation

            if rotation == 90 or rotation == 270:
                h = min(h, window_height / len(strip.pixels))
                w = min(w, h)
            elif rotation == 180 or rotation == 0:
                w = min(w, window_width / len(strip.pixels))
                h = min(h, w)

        w = min(w, h)
        h = w
            
        for i in range(len(strips)):
            strip = strips[i]
            strip.pixels.add_renderer(self, x + self.padding * (2 if i > 0 else 1), y + self.padding * (i if i > 0 else 1), w, h, rotation=strip.rotation)

    def schedule_next(self, delay_ms, callback):
        self.window.after(delay_ms, callback)

    def run(self):
        self.window.mainloop()

class T:
    def ticks_ms(self):
        return time.perf_counter()
    
    def ticks_diff(self, end, start):
        return end - start
    
t = T()