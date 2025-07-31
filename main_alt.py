'''
        Neopixel LED Timing Test using uasyncio module 25-07-29
        Note:
            max frame rate = 800000/8*4/num of leds. So for 400 leds it would be 62.5frames/sec
            The ESP32 can support up to 30 threads
            It also has a second core 
'''

# Imports
import time
import uasyncio as asyncio
import machine
from machine import Pin, Timer
import sys
import errno
import utime
from neopixel import NeoPixel
from random import randrange, randint

# Const declarations
LOOP_REFRESH_SEC = 2.0
ON = 1
OFF = 0

# Global controller variables
message_On = "LED on"
message_Off = "LED off"
ctrl_live_counter = 0
status_led_state = 'Off'
start_time = 0
end_time = 0

# Define RGBW LED pins & channels
pins = [14, 17, 4]
ch1  = 14
ch2 = 17
# ch3 = 16
ch4 =4
number_channels = 3

# Define number of LEDs per string
num_leds = [276, 480, 432]  # Number of LEDs per string

# RGBW Driver Class
class RGBWDriver:
    def __init__(self, pin_numbers, num_leds_per_string):
        self.led_strings = [
            NeoPixel(Pin(pin), num_leds, bpp=4)  # bpp=4 for RGBW
            for pin, num_leds in zip(pin_numbers, num_leds_per_string)
        ]
    
    # Update a specific LED string with new colors
    async def update_leds(self, string_index, colors):
        if 0 <= string_index < len(self.led_strings):
            for i, color in enumerate(colors):
                self.led_strings[string_index][i] = color
            self.led_strings[string_index].write()
        await asyncio.sleep(0)  # Yield to the scheduler

    # Cycle through colors on all LED strings
    async def cycle_colors(self, delay=0.1):
        while True:
            for string in self.led_strings:
                for i in range(len(string)):
                    string[i] = (255, 0, 0, 0)  # Red
                string.write()
                await asyncio.sleep(delay)
                for i in range(len(string)):
                    string[i] = (0, 255, 0, 0)  # Green
                string.write()
                await asyncio.sleep(delay)
                for i in range(len(string)):
                    string[i] = (0, 0, 255, 0)  # Blue
                string.write()
                await asyncio.sleep(delay)

    async def sweep_colors(self, delay=0.1):
        while True:
            for string in self.led_strings:
                for i in range(len(string)):
                    string[i] = (255, 0, 0, 0)  # Red
                    string.write()

            await asyncio.sleep(delay)

            for string in self.led_strings:
                for i in range(len(string)):
                    string[i] = (0, 0, 0, 0)  # Red
                string.write()
                # for i in range(len(string)):
                #     string[i] = (0, 255, 0, 0)  # Green
                #     string.write()
                # await asyncio.sleep(delay)
                # for i in range(len(string)):
                #     string[i] = (0, 0, 255, 0)  # Blue
                #     string.write()
                # await asyncio.sleep(delay)
                # for i in range(len(string)):
                #     string[i] = (0, 0, 0, 0)  # Off
                # string.write()
                # await asyncio.sleep(delay)
                # for i in range(len(string)):
                #     string[i] = (0, 0, 0, 0)  # Off
                # string.write()
                # await asyncio.sleep(delay)
                # for i in range(len(string)):
                #     string[i] = (0, 0, 0, 0)  # Off
                # string.write()
                # await asyncio.sleep(delay)

# Create Status LED object
status_led = Pin(33, Pin.OUT, value=1)  # By default LED off
status_led_state = 'OFF'  # LED state "ON" or "OFF"

# Relay
pwr_rel = Pin(32, Pin.OUT, value=1) # 24V supply

# Create periodic timer - 0 object
tim0 = Timer(0)

# Tim 0 callback function...
def tim0_callback(tim0):
    global ctrl_live_counter

    # Decrement while counters not zero
    if ctrl_live_counter != 0: # Keep alive counter
        ctrl_live_counter -= 1

# Turn status LED on or off...
def setup_status_led(action):
    global status_led_state
    
    if action == ON:
        status_led.off() # Inverted, LED on
        status_led_state = 'ON'
    elif action == OFF:
        status_led.on() # Inverted, LED off
        status_led_state = 'OFF'
        
# Flash status LED at rate defined...
def blink_led(frequency=0.5, num_blinks=3):
    for _ in range(num_blinks):
        setup_status_led(ON)  # Turn on
        time.sleep(frequency)
        setup_status_led(OFF)  # Turn off
        time.sleep(frequency)

# Create random tupple
def rand_color():
    r = randrange(0, 255)
    g = randrange(0, 255)
    b = randrange(0, 255)
    w = randrange(0, 128)
    return  (r,g,b,w)

driver = RGBWDriver(pins, num_leds)

# Main loop
async def main():    
    
    # Create LED driver object
    driver = RGBWDriver(pins, num_leds)

    # Start cycling colors
    asyncio.create_task(driver.cycle_colors(0.2))

    # while True:
    #     # Update specific strings with random colors
    #     start_time = utime.ticks_ms() #Get initial timestamp
    #     await driver.update_leds(0, [rand_color()] * 36)  # Random color for all LEDs in string '0'
    #     done_time = utime.ticks_ms() #Get initial timestamp
    #     print("Total Elapsed time updating channel 1: {}ms", done_time-start_time)
        
    #     start_time = utime.ticks_ms() #Get initial timestamp
    #     await driver.update_leds(1, [rand_color()] * 36)  # Random color for all LEDs in string '0'
    #     done_time = utime.ticks_ms() #Get initial timestamp
    #     print("Total Elapsed time updating channel 2: {}ms", done_time-start_time)
        
    #     start_time = utime.ticks_ms() #Get initial timestamp
    #     await driver.update_leds(2, [rand_color()] * 36)  # Random color for all LEDs in string '0'
    #     done_time = utime.ticks_ms() #Get initial timestamp
    #     print("Total Elapsed time updating channel 3: {}ms", done_time-start_time)
        
    #     #start_time = utime.ticks_ms() #Get initial timestamp
    #     #await driver.update_leds(3, [rand_color()] * 36)  # Random color for all LEDs in string '0'
    #     #done_time = utime.ticks_ms() #Get initial timestamp
    #     #print("Total Elapsed time updating channel 4: {}ms", done_time-start_time)
        
    #     time.sleep(1) 
    # # loop...

try:
    asyncio.run(driver.sweep_colors(0.001))
except KeyboardInterrupt:
    print('Exiting program on keyboard interrupt')
    sys.exit()
finally:
    asyncio.new_event_loop()  # Reset the event loop and return it.