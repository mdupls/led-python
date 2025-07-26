# hardware.py

import os
import sys

def is_testing():
    return ('unittest' in sys.modules) or ('pytest' in sys.modules)

if os.getenv("MOCK_HW") or is_testing():
    import fake_hw as hw
else:
    import real_hw as hw

Pin = hw.Pin
NeoPixel = hw.NeoPixel
Scheduler = hw.Scheduler
Timer = hw.Timer
