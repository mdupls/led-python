# hardware.py

def is_micropython():
    try:
        import machine
        return True
    except ImportError:
        return False

if is_micropython():
    import real_hw as hw
else:
    import fake.fake_hw as hw

Pin = hw.Pin
NeoPixel = hw.NeoPixel
Runtime = hw.Runtime
t = hw.t
