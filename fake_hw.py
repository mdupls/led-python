# fake_hw.py

from scheduler import Scheduler as SchedulerInterface, Timer as TimerInterface
import tkinter as tk

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

    def add_renderer(self, renderer, x, y, rotation=0):
        self.renderer = renderer
        self.window = renderer.window
        self.canvas = renderer.canvas
        
        size = 10

        if rotation == 90 or rotation == 270:
            rect_fn = lambda i: (
                x, y + i * size, x + size, y + (i + 1) * size
            )
        elif rotation == 180 or rotation == 0:
            rect_fn = lambda i: (
                x + i * size, y, x + (i + 1) * size, y + size
            )

        self.rects = []

        for i in range(self.n):
            rect = self.canvas.create_rectangle(
                *rect_fn(i), fill="white", outline="black"
            )
            self.rects.append(rect)
        # self.window.update()

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
        # self.window.update()

class Timer(TimerInterface):
    def __init__(self, root):
        self.root = root

    def after(self, delay_ms, callback):
        self.root.after(delay_ms, callback)
    
class Scheduler(SchedulerInterface):
    def __init__(self, root, interval_ms):
        self.root = root
        self.interval_ms = interval_ms
        self._job = None

    def _tick(self, callback):
        callback()
        self._job = self.root.after(self.interval_ms, self._tick, callback)

    def start(self, callback):
        if self._job is None:
            self._tick(callback)

    def stop(self):
        if self._job:
            self.root.after_cancel(self._job)
            self._job = None

class Renderer:
    def __init__(self):
        self.window = tk.Tk()

        # Set desired window size
        window_width = 1024
        window_height = 600

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

    def add(self, strip, x, y):
        self.strips.append(strip)

        strip.pixels.add_renderer(self, x + self.padding, y + self.padding, rotation=strip.rotation)

def create_factory():
    renderer = Renderer()
    
    createTimer = lambda: Timer(renderer.window)
    createScheduler = lambda: Scheduler(renderer.window, 50)

    return renderer, createTimer, createScheduler