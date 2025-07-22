# main.py

# Imports

from time import sleep
from hardware import Pin, NeoPixel
from random import randrange, randint

# Constants
RGB_LED_TYPE = 0
RGBW_LED_TYPE = 1
RGB_BPP = 3 # RGB leds
RGBW_BPP = 4  # RGBW LEDs
TIM_400 = 0 # 400kHz leds
TIM_800 = 1 # 800kHz leds
RGB_PIXELS = 1 # RGB, 1 led=1 pixel
DELAY = 0.001
OFF = (0, 0, 0, 0)

# Globals
color = (255,0,0,0) # Red
cycles = 1
rainbow_colors = [(255, 0, 0, 128), (255, 127, 0, 128), (255, 255, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128), (75, 0, 130, 128), (148, 0, 211, 128)]
rgb_colors = [ (0, 255, 0, 0), (255, 0, 0, 0), (0, 0, 255, 0)] # Green, red and blue in list

# Create input/output pin objects
status_led = Pin(33, Pin.OUT, value = 1) # Red status led, 1 = off

pwr_rel = Pin(32, Pin.OUT, value=1) # 24V supply
rel2 = Pin(13, Pin.OUT, value=0) # Spare relay

emac_txd0 = Pin(19, Pin.OUT, value=0) # Ethernet
emac_txd1 = Pin(22, Pin.OUT, value=0)
emac_txen = Pin(21, Pin.OUT, value=0)
emac_rxd0 = Pin(25, Pin.IN)
emac_rxd1 = Pin(26, Pin.IN)
mdc =  Pin(23, Pin.OUT, value=0)
mdio =  Pin(18, Pin.IN)
crs_dv = Pin(27, Pin.OUT, value=0)
emac_clk = Pin(0, Pin.OUT, value=0)

class MyNeoPixel:
    def __init__(self, id, pin_num, num_leds, bpp=3, timing=TIM_400, enabled=False):
        self.id = id
        self.zero_data = [OFF] * num_leds
        self.enabled = enabled
        self.np = NeoPixel(Pin(pin_num), num_leds, bpp=bpp, timing=timing)
    
    def get_id(self):
        return self.id
    
# Create neopixel objects (Def timing = 800kHz)
ch1_np = MyNeoPixel("ch1", pin_num=14, num_leds=50, bpp=RGBW_BPP, timing=TIM_800, enabled=True) #276
ch2_np = MyNeoPixel("ch2", pin_num=17, num_leds=40, bpp=RGBW_BPP, timing=TIM_800, enabled=True) #480
ch3_np = MyNeoPixel("ch3", pin_num=16, num_leds=30, bpp=RGBW_BPP, timing=TIM_800, enabled=True)
ch4_np = MyNeoPixel("ch4", pin_num=4, num_leds=20, bpp=RGBW_BPP, timing=TIM_800, enabled=True) #432

def zero_data(np):
    return [OFF] * len(np)
    
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

# Create random tupple
def rand_color(w=None):
    r = randrange(0, 255)
    g = randrange(0, 255)
    b = randrange(0, 255)
    if w is None:
        w = randrange(0, 128)
    else:
        w = 0
    return  (r,g,b,w)

# Clear all LEDs
def clear(ch):
    #print("Clear")
    np = ch.np
    for i in range(len(np)):
        np[i] = ch.zero_data[i]
        
def solid_color(ch, duration, color):
    np = ch.np
    for j in range(len(np)):
        np[j] = color
    np.write()
    sleep(duration)
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))
    
def solid_random_color(ch, duration):
    solid_color(ch, duration, rand_color(w=0))
    print('          {} cycles done'.format(cycles))

# 1. Cycle one pixel at a time, all other pixels off, single color
def cycle_single_color(ch, cycles, color):
    np = ch.np
    n = len(np)
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j - 1] = OFF
            np[j] = color # Set color 
            np.write() 
            sleep(DELAY) # Delay between pixels
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))

# 2. Cycle one pixel at a time, all other pixels off, reg, green, blue sequence
def cycle_rgb_color(ch, cycles):
    c = 0
    np = ch.np
    n = len(np)
    for i in range(cycles):  # Sets the number of cycles     
        for j in range(n):  # Iterates through number of pixels
            np[j - 1] = OFF
            np[j] = rgb_colors[c] # Set color
            np.write()
            sleep(DELAY)
            if c == 2:
                c = 0
            else:
                c += 1
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))
    
# 3. Cycle one pixel at a time, all other pixels off, random color
def cycle_random_color(ch, cycles):
    np = ch.np
    n = len(np)
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j - 1] = OFF
            np[j] = rand_color() # Select random color
            np.write()
            sleep(DELAY)
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))

# 4. Cycle continious, not turning off previous pixels single color
def cycle_cont_single(ch, cycles, color):
    np = ch.np
    n = len(np)
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j] = color # Set color 
            np.write()
            sleep(DELAY)
        clear(ch)
        np.write()
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))
    
# 5. Cycle continious, not turning off previous pixels
def cycle_cont_random(ch, cycles):
    np = ch.np
    n = len(np)
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j] = rand_color() # Select random color
            np.write()
            sleep(DELAY)
        clear(ch)
        np.write()
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))
    
# 6. Cycle continious, not turning off previous pixels, red, green and blue sequence
def cycle_cont_rgb(ch, cycles):
    c = 0
    np = ch.np
    n = len(np)
    for i in range(cycles):  # Sets the number of cycles     
        for j in range(n):  # Iterates through number of pixels
            np[j] = rgb_colors[c] # Set color
            np.write()
            sleep(DELAY) 
            if c == 2:
                c = 0
            else:
                c += 1
        clear(ch)
        np.write()
    clear(ch)
    np.write()
    print('          {} cycles done'.format(cycles))   
         
# 7. Bounce LEDs
def bounce(ch, cycles):
    np = ch.np
    n = len(np)
    for i in range(cycles * 2 * n):
        for j in range(n):
            np[j] = (0, 0, 128, 0)
        if (i // n) % 2 == 0:
            np[i % n] = OFF
        else:
            np[n - 1 - (i % n)] = OFF
        np.write()
        sleep(DELAY)
    clear(ch)
    np.write()
    print('          Bounce done')
    
# 8. Fade LEDs in/out
def fade_in_out(ch, cycles):
    np = ch.np
    n = len(np)
    for i in range(0, cycles * 2 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0, 0)
        np.write()
        sleep(DELAY)
    clear(ch)
    np.write()
    print('          Fade done') 
    
# 9. Fancy show
def fancy_show(ch, cycles):
    np = ch.np
    n = len(np)
    for i in range(cycles * n):
        sleep(DELAY)
        np[(i - 1) % n] = OFF
        np[i % n] = rand_color()
        np.write()
        sleep(DELAY)
    clear(ch)
    np.write()
    print('          Fancy done')
    
# 10. Scroll thru Spectrum
def spectrum(ch, cycles):
    np = ch.np
    n = len(np)
    #print("Loop 1")
    for i in range(cycles):  # Sets the number of cycles before exit
        for j in range(n):  # Iterates thru pixels 'n'
            for k in range(5):  # Change the pixel HSV 5 times
                           
                hue = randint(50, 255)/255.0       
                sat = randint(50, 255)/255.0
                brt = randint(50, 255)/2048.0
            
                col = hsv_to_rgb(hue, sat,  brt, 0)   # np[0] refers to the first LED, 0 in this case. Hue, saturation and brightness
                #print('Col = ', col)
                #print('1: j % n = ', j % n)
                np[j % n] = col  # np[i%n] refers to the pixel to be written
                np.write()  # Set pixel to specified color
                sleep(DELAY)
            sleep(DELAY)
        sleep(DELAY)
    
    #print("Loop 2")
    for l in range(cycles):  # Sets the number of cycles before exit
        for m in range(n):  # Iterates thru pixels 'n'
            for r in range(5):  # Change the pixel HSV 5 times
            
                hue = randint(50, 255)/255.0       
                sat = randint(50, 255)/255.0
                brt = randint(50, 255)/2048.0
            
                col = hsv_to_rgb(hue, sat,  brt, 0)   # np[0] refers to the first LED, 0 in this case. Hue, saturation and brightness
                #print('Col = ', col)
                #print('2: m % n = ', (n - 1) - (m % n))
                np[(n - 1) - (m % n)] = col  # np[i%n] refers to the pixel to be written, pixels reversed
                np.write()  # Set pixel to specified color
                sleep(DELAY)
            sleep(DELAY)
        sleep(DELAY)
    clear(ch)
    np.write()
    print('          Spectrum done') 
    
# 11. Rainbow cycle
def rainbow_cycle(ch, cycles):
    np = ch.np
    n = len(np)
    for i in range(len(rainbow_colors)):
        for j in range(n):
            np[j] = rainbow_colors[(i + j) % len(rainbow_colors)]
            np.write()
        sleep(DELAY)
    clear(ch)
    np.write()
    print('          Rainbow done')
  
def main():    
    try:
        while True:
            
            print()
            if ch1_np.enabled:
                solid_color(ch1_np, 2, color)
            if ch2_np.enabled:
                solid_color(ch2_np, 2, color)
            if ch3_np.enabled:
                solid_color(ch3_np, 2, color)
            if ch4_np.enabled:
                solid_color(ch4_np, 2, color)
            sleep(2)
            
            print()
            if ch1_np.enabled:
                solid_random_color(ch1_np, 2)
            if ch2_np.enabled:
                solid_random_color(ch2_np, 2)
            if ch3_np.enabled:
                solid_random_color(ch3_np, 2)
            if ch4_np.enabled:
                solid_random_color(ch4_np, 2)
            sleep(2)
            
            print('1: Single color')
            if ch1_np.enabled:
                cycle_single_color(ch1_np, cycles, color)
            if ch2_np.enabled:
                cycle_single_color(ch2_np, cycles, color)
            if ch3_np.enabled:
                cycle_single_color(ch3_np, cycles, color)
            if ch4_np.enabled:
                cycle_single_color(ch4_np, cycles, color)
            sleep(2)
            
            print('2: Single RGB sequence')
            if ch1_np.enabled:
                cycle_rgb_color(ch1_np, cycles)
            if ch2_np.enabled:
                cycle_rgb_color(ch2_np, cycles)
            if ch3_np.enabled:
                cycle_rgb_color(ch3_np, cycles)
            if ch4_np.enabled:
                cycle_rgb_color(ch4_np, cycles)
            sleep(2)
            
            print('3: Single random colors')
            if ch1_np.enabled:
                cycle_random_color(ch1_np, cycles)
            if ch2_np.enabled:
                cycle_random_color(ch2_np, cycles)
            if ch3_np.enabled:
                cycle_random_color(ch3_np, cycles)
            if ch4_np.enabled:
                cycle_random_color(ch4_np, cycles)
            sleep(2)
            
            print('4: Continuous single color')
            if ch1_np.enabled:
                cycle_cont_single(ch1_np, cycles, color)
            if ch2_np.enabled:
                cycle_cont_single(ch2_np, cycles, color)
            if ch3_np.enabled:
                cycle_cont_single(ch3_np, cycles, color)
            if ch4_np.enabled:
                cycle_cont_single(ch4_np, cycles, color)
            sleep(2)
             
            print('5: Continuous random colors')
            if ch1_np.enabled:
                cycle_cont_random(ch1_np, cycles)
            if ch2_np.enabled:
                cycle_cont_random(ch2_np, cycles)
            if ch3_np.enabled:
                cycle_cont_random(ch3_np, cycles)
            if ch4_np.enabled:
                cycle_cont_random(ch4_np, cycles)
            sleep(2)
           
            print('6: Continuous RGB')
            if ch1_np.enabled:
                cycle_cont_rgb(ch1_np, cycles)
            if ch2_np.enabled:
                cycle_cont_rgb(ch2_np, cycles)
            if ch3_np.enabled:
                cycle_cont_rgb(ch3_np, cycles)
            if ch4_np.enabled:
                cycle_cont_rgb(ch4_np, cycles)
            sleep(2)
            
            print('7: Bounce')
            if ch1_np.enabled:
                bounce(ch1_np, cycles)
            if ch2_np.enabled:
                bounce(ch2_np, cycles)
            if ch3_np.enabled:
                bounce(ch3_np, cycles)
            if ch4_np.enabled:
                bounce(ch4_np, cycles)
            sleep(2)
            
            print('8: Fade')
            if ch1_np.enabled:
                fade_in_out(ch1_np, cycles)
            if ch2_np.enabled:
                fade_in_out(ch2_np, cycles)
            if ch3_np.enabled:
                fade_in_out(ch3_np, cycles)
            if ch4_np.enabled:
                fade_in_out(ch4_np, cycles)
            sleep(2)
            
            print('9: Fancy show')
            if ch1_np.enabled:
                fancy_show(ch1_np, cycles)
            if ch2_np.enabled:
                fancy_show(ch2_np, cycles)
            if ch3_np.enabled:
                fancy_show(ch3_np, cycles)
            if ch4_np.enabled:
                fancy_show(ch4_np, cycles)
            sleep(2)
            
            print('10: Scroll through spectrum')
            if ch1_np.enabled:
                spectrum(ch1_np, cycles)
            if ch2_np.enabled:
                spectrum(ch2_np, cycles)
            if ch3_np.enabled:
                spectrum(ch3_np, cycles)
            if ch4_np.enabled:
                spectrum(ch4_np, cycles)
            sleep(2)
            
            print('11: Flash rainbow')
            if ch1_np.enabled:
                rainbow_cycle(ch1_np, cycles)
            if ch2_np.enabled:
                rainbow_cycle(ch2_np, cycles)
            if ch3_np.enabled:
                rainbow_cycle(ch3_np, cycles)
            if ch4_np.enabled:
                rainbow_cycle(ch4_np, cycles)
            sleep(2)
            
    except KeyboardInterrupt:
        print("\nCtrl-C pressed")
    finally:
        if ch1_np.enabled:
            clear(ch1_np)
        if ch2_np.enabled:
            clear(ch2_np)
        if ch3_np.enabled:
            clear(ch3_np)
        if ch4_np.enabled:
            clear(ch4_np)
        print('Strips turned off and exiting...')
           
main()