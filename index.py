'''
        Neopixel LED Test
        25-01-11
        /
'''

# Imports
from machine import Pin
import neopixel
import time
from random import randrange, randint

# Constants
RGB_LED_TYPE = 0
RGBW_LED_TYPE = 1
RGB_BPP = 3 # RGB leds
RGBW_BPP = 4  # RGBW LEDs
TIM_400 = 0 # 400kHz leds
TIM_800 = 1 # 800kHz leds
RGB_PIXELS = 1 # RGB, 1 led=1 pixel
RGBW_PIXEL_LEDS = 1 # For RGBW LEDs every six LEDs is one pixel
DELAY = 0

# Globals
ch1_num_leds = 60
ch2_num_leds = 276
ch3_num_leds = 480
ch4_num_leds = 432
color = (0,255,0,0) # Green
cycles = 3
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

ch1_p = Pin(16) # Strip led channels
ch2_p = Pin(14)
ch3_p = Pin(17)
ch4_p = Pin(4)

# Create neopixel objects (Def timing = 800kHz)
ch1_np = neopixel.NeoPixel(ch1_p, ch1_num_leds, bpp=RGBW_BPP, timing=TIM_800)
ch2_np = neopixel.NeoPixel(ch2_p, ch2_num_leds, bpp=RGBW_BPP, timing=TIM_800)
ch3_np = neopixel.NeoPixel(ch3_p, ch3_num_leds, bpp=RGBW_BPP, timing=TIM_800)
ch4_np = neopixel.NeoPixel(ch4_p, ch4_num_leds, bpp=RGBW_BPP, timing=TIM_800)

# Get pixels per channel
ch1_n = int(ch1_np.n/RGBW_PIXEL_LEDS)
ch2_n = int(ch2_np.n/RGBW_PIXEL_LEDS)
ch3_n = int(ch3_np.n/RGBW_PIXEL_LEDS)
ch4_n = int(ch4_np.n/RGBW_PIXEL_LEDS)

def sleep():
    time.sleep_ms(DELAY)
    
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
def rand_color():
    r = randrange(0, 255)
    g = randrange(0, 255)
    b = randrange(0, 255)
    w = randrange(0, 128)
    return  (r,g,b,w)

# Clear all LEDs
def clear(np, n):     
    #print("Clear")
    for i in range(n): # Number of pixels
        np[i] = (0, 0, 0, 0)
    np.write()

# 1. Cycle one pixel at a time, all other pixels off, single color
def cycle_single_color(np, n, cycles, color):
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j ] = color # Set color 
            np.write() 
            sleep() # Delay between pixels
            clear(np, n) # Clear present pixel before continuing
    clear(np, n)         
    print('          {} cycles done'.format(cycles))

# 2. Cycle one pixel at a time, all other pixels off, reg, green, blue sequence
def cycle_rgb_color(np, n, cycles):
    c = 0
    for i in range(cycles):  # Sets the number of cycles     
        for j in range(n):  # Iterates through number of pixels
            np[j ] = rgb_colors[c] # Set color
            np.write()
            sleep() 
            clear(np, n) 
            if c == 2:
                c = 0
            else:
                c += 1
    clear(np, n)
    print('          {} cycles done'.format(cycles))
    
# 3. Cycle one pixel at a time, all other pixels off, random color
def cycle_random_color(np, n, cycles):
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j ] = rand_color() # Select random color
            np.write()
            sleep()
            clear(np, n)
        clear(np, n)
    clear(np, n)
    print('          {} cycles done'.format(cycles))

# 4. Cycle continious, not turning off previous pixels single color
def cycle_cont_single(np, n, cycles, color):
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j ] = color # Set color 
            np.write()
            sleep()
        clear(np, n)
    clear(np, n)
    print('          {} cycles done'.format(cycles))
    
# 5. Cycle continious, not turning off previous pixels
def cycle_cont_random(np, n, cycles):
    for i in range(cycles):  # Sets the number of cycles
        for j in range(n):  # Iterates through number of pixels
            np[j] = rand_color() # Select random color
            np.write()
            sleep()
        clear(np, n)
    clear(np, n)
    print('          {} cycles done'.format(cycles))
    
# 6. Cycle continious, not turning off previous pixels, red, green and blue sequence
def cycle_cont_rgb(np, n, cycles):
    c = 0
    for i in range(cycles):  # Sets the number of cycles     
        for j in range(n):  # Iterates through number of pixels
            np[j ] = rgb_colors[c] # Set color
            np.write()
            sleep() 
            if c == 2:
                c = 0
            else:
                c += 1
        clear(np, n)
    clear(np, n)
    print('          {} cycles done'.format(cycles))   
         
# 7. Bounce LEDs
def bounce(np, n):
    for i in range(8 * n):
        for j in range(n):
            np[j] = (0, 0, 128, 0)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0, 0)
        np.write()
        sleep()
    clear(np, n)
    print('          Bounce done')
    
# 8. Fade LEDs in/out
def fade_in_out(np, n):
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0, 0)
        np.write()
        sleep()
    clear(np, n)
    print('          Fade done') 
    
# 9. Fancy show
def fancy_show(np, n):
    for i in range(4 * n): 
        for j in range(n):
            np[j] = (0, 0, 0, 0)
            #print("I % N = ", i % n)
        np.write()
        sleep()
        np[i % n] = rand_color()
        np.write()
        sleep()
    clear(np, n)
    print('          Fancy done')
    
# 10. Scroll thru Spectrum
def spectrum(np, n):    
    #print("Loop 1")
    for i in range(1 * n ):  # Sets the number of cycles before exit
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
                sleep()
            sleep()
        sleep()
    
    #print("Loop 2")
    for l in range(1 * n):  # Sets the number of cycles before exit
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
                sleep()
            sleep()
        sleep()
    clear(np, n)
    print('          Spectrum done') 
    
# 11. Rainbow cycle
def rainbow_cycle(np, n):
    for i in range(len(rainbow_colors)):
        for j in range(len(np)):
            np[j] = rainbow_colors[(i + j) % len(rainbow_colors)]
            np.write()
        sleep()
    clear(np, n)
    print('          Rainbow done')
  
def main():    
    try:
        while True:
            
            print('1: Single color')
            cycle_single_color(ch1_np, ch1_n, cycles, color)
            cycle_single_color(ch2_np, ch2_n, cycles, color)
            cycle_single_color(ch3_np, ch3_n, cycles, color)
            cycle_single_color(ch4_np, ch4_n, cycles, color)
            time.sleep(2)
            
            print('2: Single RGB sequence')
            cycle_rgb_color(ch1_np, ch1_n, cycles)
            cycle_rgb_color(ch2_np, ch2_n, cycles)
            cycle_rgb_color(ch3_np, ch3_n, cycles)
            cycle_rgb_color(ch4_np, ch4_n, cycles)
            time.sleep(2)
            
            print('3: Single random colors')
            cycle_random_color(ch1_np, ch1_n, cycles)
            cycle_random_color(ch2_np, ch2_n, cycles)
            cycle_random_color(ch3_np, ch3_n, cycles)
            cycle_random_color(ch4_np, ch4_n, cycles)
            time.sleep(2)
            
            print('4: Continuous single color')
            cycle_cont_single(ch1_np, ch1_n, cycles, color)
            cycle_cont_single(ch2_np, ch2_n, cycles, color)
            cycle_cont_single(ch3_np, ch3_n, cycles, color)
            cycle_cont_single(ch4_np, ch4_n, cycles, color)
            time.sleep(2)
             
            print('5: Continuous random colors')
            cycle_cont_random(ch1_np, ch1_n, cycles)
            cycle_cont_random(ch2_np, ch2_n, cycles)
            cycle_cont_random(ch3_np, ch3_n, cycles)
            cycle_cont_random(ch4_np, ch4_n, cycles)
            time.sleep(2)
           
            print('6: Continuous RGB')
            cycle_cont_rgb(ch1_np, ch1_n, cycles)
            cycle_cont_rgb(ch2_np, ch2_n, cycles)
            cycle_cont_rgb(ch3_np, ch3_n, cycles)
            cycle_cont_rgb(ch4_np, ch4_n, cycles)
            time.sleep(2)
            
            print('7: Bounce')
            bounce(ch1_np, ch1_n)
            bounce(ch2_np, ch2_n)
            bounce(ch3_np, ch3_n)
            bounce(ch4_np, ch4_n)
            time.sleep(2)
            
            print('8: Fade')
            fade_in_out(ch1_np, ch1_n)
            fade_in_out(ch2_np, ch2_n)
            #fade_in_out(ch3_np, ch3_n)
            fade_in_out(ch4_np, ch4_n)
            time.sleep(2)
            
            print('9: Fancy show')
            fancy_show(ch1_np, ch1_n)
            fancy_show(ch2_np, ch2_n)
            fancy_show(ch3_np, ch3_n)
            fancy_show(ch4_np, ch4_n)
            time.sleep(2)
            
            print('10: Scroll through spectrum')
            spectrum(ch1_np, ch1_n)
            spectrum(ch2_np, ch2_n)
            spectrum(ch3_np, ch3_n)
            spectrum(ch4_np, ch4_n)
            time.sleep(2)
            
            print('11: Flash rainbow')
            rainbow_cycle(ch1_np, ch1_n)
            rainbow_cycle(ch2_np, ch2_n)
            rainbow_cycle(ch3_np, ch3_n)
            rainbow_cycle(ch4_np, ch4_n)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nCtrl-C pressed")
    finally:
        clear(ch1_np, ch1_n)
        clear(ch2_np, ch2_n)
        clear(ch3_np, ch3_n)
        clear(ch4_np, ch4_n)
        print('Strips turned off and exiting...')
           
main()

# End