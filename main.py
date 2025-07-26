# main.py

# Imports
from hardware import Pin, NeoPixel, Scheduler, Timer
from utils import rand_color

# Effects imports
from effects.solid import SolidEffect
from effects.fade import FadeEffect
from effects.wipe import WipeEffect
from effects.wipe_solid import WipeSolidEffect
from effects.wipe_inward import WipeInwardEffect
from effects.rainbow_wipe import RainbowWipeEffect
from effects.rainbow_cycle import RainbowCycleEffect
from effects.bounce import BounceEffect
from effects.sparkle import SparkleEffect
from effects.fancy import FancyEffect
from effects.spectrum import SpectrumEffect

# Constants
RGB_LED_TYPE = 0
RGBW_LED_TYPE = 1
RGB_BPP = 3 # RGB leds
RGBW_BPP = 4  # RGBW LEDs
TIM_400 = 0 # 400kHz leds
TIM_800 = 1 # 800kHz leds
RGB_PIXELS = 1 # RGB, 1 led=1 pixel

# Globals
color = (255,0,0,0) # Red
cycles = 1
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
        self.enabled = enabled
        self.np = NeoPixel(Pin(pin_num), num_leds, bpp=bpp, timing=timing)
    
    def get_id(self):
        return self.id
    
# Create neopixel objects (Def timing = 800kHz)
ch1_np = MyNeoPixel("ch1", pin_num=14, num_leds=50, bpp=RGBW_BPP, timing=TIM_800, enabled=False) #276
ch2_np = MyNeoPixel("ch2", pin_num=17, num_leds=40, bpp=RGBW_BPP, timing=TIM_800, enabled=False) #480
ch3_np = MyNeoPixel("ch3", pin_num=16, num_leds=30, bpp=RGBW_BPP, timing=TIM_800, enabled=False)
ch4_np = MyNeoPixel("ch4", pin_num=4, num_leds=20, bpp=RGBW_BPP, timing=TIM_800, enabled=True) #432

timer = Scheduler(ch1_np.np.window, 50)

class LEDController:
    def __init__(self, ch, timer):
        self.timer = timer
        self.position = 0
        self.direction = 1  # 1 for right, -1 for left
        self.effect = None
        self.ch = ch

    def start(self):
        self.timer.start(self._update)

    def stop(self):
        self.timer.stop()

    def _update(self):
        # Run current pattern
        if self.effect is not None:
            self.effect.update()
            self.ch.np.write()

    def set_speed(self, speed_ms):
        self.timer.interval_ms = speed_ms
        # Restart timer to apply new period
        self.stop()
        self.start()

    def set_effect(self, effect):
        effect.setStrip(self.ch.np)
        self.effect = effect

mysleep = Timer(ch1_np.np.window)

def main():    
    # try:
    #     while True:

    # scheduler.start(lambda: wipe(ch1_np, 1, color))
    # scheduler.after(3000, lambda: wipe_solid(scheduler, ch1_np, 2, color))

    leds = LEDController(ch1_np, timer=timer)
    leds.start()

    # leds.set_effect(SolidEffect())
    # leds.set_effect(SolidEffect(color=(255, 0, 0, 0)))
    # leds.set_effect(FadeEffect(color=rand_color(w=0)))
    leds.set_effect(FadeEffect(color_fn=lambda: rand_color(w=0)))
    # leds.set_effect(WipeEffect(color=rand_color(w=0)))
    # leds.set_effect(WipeEffect(color_fn=lambda: rand_color(w=0)))
    # leds.set_effect(WipeSolidEffect(color=rand_color(w=0)))
    # leds.set_effect(WipeSolidEffect(color_fn=lambda: rand_color(w=0)))
    # leds.set_effect(RainbowWipeEffect())
    # leds.set_effect(RainbowCycleEffect())
    # leds.set_effect(WipeInwardEffect(color=rand_color(w=0)))
    # leds.set_effect(WipeInwardEffect(color_fn=lambda: rand_color(w=0)))
    # leds.set_effect(BounceEffect(color=rand_color(w=0)))
    # leds.set_effect(BounceEffect(color_fn=lambda: rand_color(w=0)))
    # leds.set_effect(SparkleEffect(color_fn=lambda: rand_color(w=0)))
    # leds.set_effect(SparkleEffect(color=(255, 0, 0, 0)))
    # leds.set_effect(FancyEffect())
    # leds.set_effect(SpectrumEffect())

    # leds.set_speed(50)

    # mysleep.after(5000, lambda: leds.set_speed(10))
    # mysleep.after(10000, lambda: leds.set_pattern(wipe_solid))

    ch1_np.np.window.mainloop()
            
    # except KeyboardInterrupt:
    #     print("\nCtrl-C pressed")
    # finally:
    #     if ch1_np.enabled:
    #         clear(ch1_np)
    #     if ch2_np.enabled:
    #         clear(ch2_np)
    #     if ch3_np.enabled:
    #         clear(ch3_np)
    #     if ch4_np.enabled:
    #         clear(ch4_np)
    #     print('Strips turned off and exiting...')
           
main()