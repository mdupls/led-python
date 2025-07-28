# hardware.py

# import os
# import sys

def is_micropython():
    try:
        import machine
        return True
    except ImportError:
        return False

# def is_testing():
#     return ('unittest' in sys.modules) or ('pytest' in sys.modules)

if is_micropython():
    import real_hw as hw
else:
    import fake_hw as hw

Pin = hw.Pin
NeoPixel = hw.NeoPixel
Runtime = hw.Runtime
