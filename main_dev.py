# main.py

# Imports
from hardware import Pin, Runtime
from utils import rand_color
from strip import Strip, Segment, RGBW_BPP, TIM_800
from controller import Controller

# Effects imports
from effects.solid import SolidEffect
from effects.fade import FadeEffect
from effects.sweep import SweepEffect
from effects.wipe import WipeEffect
from effects.wipe_solid import SolidWipeEffect
from effects.wipe_inward import InwardWipeEffect
from effects.wipe_rainbow import RainbowWipeEffect
from effects.cycle_rainbow import RainbowCycleEffect
from effects.bounce import BounceEffect
from effects.sparkle import SparkleEffect
from effects.wipe_random import RandomWipeEffect
from effects.spectrum import SpectrumEffect

# Constants
RGB_LED_TYPE = 0
RGBW_LED_TYPE = 1

# Pins
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

segments = [
    Segment(0, 10, reverse=True),
    Segment(10, 40),
    Segment(50, 10)
]
strip1 = Strip("ch1", pin_num=14, num_leds=276, bpp=RGBW_BPP, timing=TIM_800, enabled=True, rotation=90) #276 #14

segments = [
    Segment(0, 10, reverse=True),
    Segment(10, 15),
    Segment(25, 15)
]
strip2 = Strip("ch2", pin_num=17, num_leds=480, bpp=RGBW_BPP, timing=TIM_800, enabled=True) #480 #17

segments = [
    Segment(0, 20)
]
strip3 = Strip("ch3", pin_num=4, num_leds=432, bpp=RGBW_BPP, timing=TIM_800, enabled=True) #432

runtime = Runtime()

runtime.add([strip1, strip2, strip3])

controllers = []
controllers.append(Controller(strip1, runtime))
controllers.append(Controller(strip2, runtime))
controllers.append(Controller(strip3, runtime))

controllers[0].set_effect_fn(BounceEffect, color_fn=lambda: rand_color(w=0))

controllers[1].set_effect_fn(BounceEffect, color_fn=lambda: rand_color(w=0))
# controllers[1].set_effect_fn(SolidEffect, segment_index=1, color=rand_color(w=0))
# controllers[1].set_effect_fn(BounceEffect, segment_index=2, color_fn=lambda: rand_color(w=0))

controllers[2].set_effect_fn(BounceEffect, color_fn=lambda: rand_color(w=0))
# controllers[2].set_effect_fn(SparkleEffect, segment_index=1, color=rand_color(w=0))

print("Running...")

# leds.set_effect(SolidEffect())
# leds.set_effect(SolidEffect(color=rand_color(w=0)))
# leds.set_effect(FadeEffect(color=rand_color(w=0)))
# leds.set_effect(FadeEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(SweepEffect(color=rand_color(w=0)))
# leds.set_effect(SweepEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(WipeEffect(color=rand_color(w=0)))
# leds.set_effect(WipeEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(RandomWipeEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(SolidWipeEffect(color=rand_color(w=0)))
# leds.set_effect(SolidWipeEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(RainbowWipeEffect())
# leds.set_effect(RainbowCycleEffect())
# leds.set_effect(InwardWipeEffect(color=rand_color(w=0)))
# leds.set_effect(InwardWipeEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(BounceEffect(color=rand_color(w=0)))
# leds.set_effect(BounceEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(SparkleEffect(color=rand_color(w=0)))
# leds.set_effect(SparkleEffect(color_fn=lambda: rand_color(w=0)))
# leds.set_effect(SpectrumEffect())
# leds.set_speed(50)

def effect1(controller):
    controller.set_effect_fn(RainbowWipeEffect)

def effect2(controller):
    controller.set_effect_fn(InwardWipeEffect, color_fn=lambda: rand_color(w=0))

def effect3(controller):
    controller.set_effect_fn(SweepEffect(color_fn=lambda: rand_color(w=0)))

effects = [
    effect1,
    effect2,
    effect3
]

for i in range(len(controllers)):
    controllers[i].set_speed(16)

for i in range(len(controllers)):
    controllers[i].start()

# def next_effect():
#     # count = (count + 1) % len(effects)
#     for i in range(len(controllers)):
#         effects[1](controllers[i])
#     runtime.schedule_next(2000, next_effect)

# runtime.schedule_next(2000, next_effect)
    
print("Started animations...")

runtime.run()