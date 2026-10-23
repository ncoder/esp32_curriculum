# Lesson 14 teacher notes

**Before class:** install the **ESP32Servo** library on every computer
(Tools → Manage Libraries). Find the servo horns and the tiny screws in each
kit; students only need to press a horn on, not screw it.

**Hardware**

- The SG90 is powered from the ESP32's 5V/VIN pin (USB 5 V). Its signal
  is fine at 3.3 V.
- The joystick module's `+5V` pin **must** go to 3V3. At 5 V the outputs
  exceed the ESP32's 3.3 V input range.
- Pins 34/35 are input-only ADC1 pins with no pull-ups; the joystick
  button on 14 uses `INPUT_PULLUP`.
- Centre readings vary (typically 1700–2100), so the code uses a wide dead
  zone (1000–3000) rather than an exact centre.

**Common problems**

- *Servo doesn't move:* the library isn't installed (compile error), the
  orange signal wire isn't on 18, or red isn't on 5V.
- *ESP32 resets / "Brownout detector was triggered" in the Serial Monitor:*
  the servo pulled too much current from USB. Use a better USB port or
  hub, or power the servo from the power supply module (sharing GND).
- *X stuck at 0 or 4095:* VRx/VRy are swapped with GND/power, or the joystick
  is on 5V.
- *Click doesn't register:* SW isn't on 14, or `INPUT_PULLUP` was mistyped.

**Quiz answers**

1. A servo turns to and holds a set angle (0–180°); a normal motor
   just spins continuously.
2. 180.
3. The ESP32 can only read up to 3.3 V; 5 V could damage the analog
   pins (and readings would max out).

**Challenge solutions:** `solutions/L14_Memory` is challenge 3. Challenges 1
and 2 are one- or two-line changes to `L14_Pointer`; for challenge 1, use
`int step = map(x, 0, 4095, 5, -5); angle = angle + step;` (still with a
dead zone check around the middle).
