# led-python

## Build

### Run

```
python3 main.py
```

#### Erasing ESP32 using esptool

```
python3 -m esptool --chip esp32 erase_flash
```

#### Installing MicroPython

```
esptool --baud 460800 write_flash 0x1000 <esp32_module>.bin
```


```
python3 -m unittest tests/effects/test_wipe_rainbow.py
```
