# Lesson 12 teacher notes

**Before class:** find the 1 kΩ (brown-black-red) and 2 kΩ (red-black-red)
resistors in each kit, as students mix them up easily. Check that the passive
buzzer (open bottom, green board) is set aside from the active one.

**Why the divider:** the HC-SR04 is a 5 V part, and its Echo pin outputs
5 V. 1 kΩ on top and 2 kΩ to ground gives 5 × 2/3 ≈ 3.3 V at the ESP32 pin.
Many online tutorials skip this. The ESP32 usually survives, but we teach the
safe habit.

**Common problems**

- *Always −1 / "Nothing in range":* VCC is on 3V3 instead of 5V, Trig and Echo
  are swapped, or row M isn't wired to pin 16.
- *Jumpy readings:* soft or angled objects scatter the sound. Use a book held
  flat. Readings under 2 cm aren't reliable.
- *Buzzer silent:* it's the active buzzer (works, but sounds different), or the
  + and – legs are swapped.
- *Parking sketch feels sluggish far away:* expected, because the beep gap is
  up to 500 ms.

**Quiz answers**

1. The sound travels to the object *and back*, so the time covers twice the distance.
2. They turn the sensor's 5 V Echo signal into about 3.3 V, which is safe for the ESP32.
3. 1000 × 0.0343 ÷ 2 ≈ 17 cm.

**Challenge solutions:** `solutions/L12_Theremin` (challenge 3) and
`solutions/L12_ParkingScreen` (bonus, needs the Adafruit SSD1306 library).
Challenges 1 and 2 are small `if`/function additions to `L12_Parking`.
