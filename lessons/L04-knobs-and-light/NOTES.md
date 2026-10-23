# Lesson 4 teacher notes

**Before class:** find the 10 kΩ potentiometer (blue knob), the photoresistors
and the 10 kΩ resistors (brown-black-orange) in each kit.

**Rails:** this is the first lesson that uses the **+** rail. Check every
student connects it to **3V3**, not to **5V/VIN**. 5 V on pin 34 or 35 can
damage the ESP32.

**Common problems**

- *Reading stuck at 0:* the middle leg isn't on pin 34, or the pot's GND/3V3
  wires are in the wrong rows.
- *Reading stuck at 4095:* the GND leg is missing.
- *Reading only uses part of the range, or jumps around a little:* this is
  normal. The ESP32's ADC isn't very precise near 0 and 3.3 V, and the
  readings wobble by a few counts.
- *Serial Plotter shows nothing:* the Serial Monitor is still open, or the
  baud rate isn't 115200.
- *Night light reversed:* the photoresistor and the 10 kΩ resistor are
  swapped (resistor to 3V3, sensor to GND). That works too, but dark then gives
  *high* numbers. Either swap them back or change `<` to `>`.

**Quiz answers**

1. 0 to 4095.
2. 100.
3. The ESP32 can only measure voltage. The resistor and photoresistor
   together make a voltage divider, whose voltage changes with the light.

**Challenge solutions:** `solutions/L04_LevelMeter` (challenge 2) and
`solutions/L04_LightAlarm` (challenge 3). Challenges 1 and the bonus are
small edits.
