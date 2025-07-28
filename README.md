# led-python

## Build

### Run using fake hardware

```
MOCK_HW=1 python main.py
```

### Run on physical hardware

```
python main.py
```

#### Erasing ESP32 using esptool

```
python3 -m esptool --chip esp32 erase_flash
```

#### Installing MicroPython

```
esptool --baud 460800 write_flash 0x1000 <esp32_module>.bin
```