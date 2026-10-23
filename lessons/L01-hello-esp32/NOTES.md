# Lesson 1 teacher notes

**Before class:** install Arduino IDE 2 and the *esp32 by Espressif Systems*
core on every computer (see [SETUP.md](../../SETUP.md)). The core is a big
download, so installing it during class costs 10+ minutes. Plug in each board
once to check that a port appears; on Windows, install the CP210x driver.

**Kit tour (0:00):** have students find the LEDs, resistors (the 220 Ω ones are
in the biggest bag), the OLED screen, motors and sensors. Tell them which
lesson each part shows up in. It builds excitement.

**Common problems**

- *No port:* a charge-only USB cable, or the CP210x driver is missing.
- *`Connecting.....` then a timeout:* hold BOOT during upload.
- *Serial Monitor shows garbage:* the baud rate isn't 115200.
- *Nothing printed at all:* the board finished `setup()` before the monitor
  opened. Press EN to restart it.
- *LED dark:* the LED is backwards (most common), or the resistor and LED legs
  aren't in the same row.

**Quiz answers**

1. `setup()` runs once at start; `loop()` repeats forever.
2. The long leg.
3. 3000.

**Challenge solutions:** `solutions/L01_SOS`. Challenges 1, 2 and the bonus
only need small edits to `L01_Blink`.
