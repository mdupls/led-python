from random import randrange

OFF = (0, 0, 0, 0)

# Clear all LEDs
def clear(strip, start=None, stop=None):
    if start is None or stop is None:
        for i in range(len(strip)):
            strip[i] = OFF
    else:
        for i in range(start, stop):
            strip[i] = OFF

def range_mod(value, start, end):
    return ((value - start) % (end - start)) + start

def rand_color(w=None):
    r = randrange(0, 255)
    g = randrange(0, 255)
    b = randrange(0, 255)
    if w is None:
        w = randrange(0, 128)
    else:
        w = 0
    return (r,g,b,w)

#Convert HSV to RGB (based on colorsys.py).
def hsv_to_rgb(h, s, v, w):
    """
        Args: h (float): Hue 0 to 1.
              s (float): Saturation 0 to 1.
              v (float): Value 0 to 1 (Brightness).
    """
    if s == 0.0:   
        return v, v, v, w
    
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6
        
    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p, w
    if i == 1:
        return q, v, p, w
    if i == 2:
        return p, v, t, w
    if i == 3:
        return p, q, v, w
    if i == 4:
        return t, p, v, w
    if i == 5:
        return v, p, q, w