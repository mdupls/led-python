# hardware.py

import os

if os.getenv("MOCK_HW"):
    import fake_hw as hw
else:
    import real_hw as hw

Pin = hw.Pin
NeoPixel = hw.NeoPixel
