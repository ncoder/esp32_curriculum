# Lesson 5 teacher notes

**Before class:** check that the kit's RGB LEDs are **common cathode**
(longest leg to GND). Test one with a 220 Ω resistor from 3V3 to each short
leg. If yours light up with the longest leg on **3V3** instead, they are
common anode: wire the long leg to 3V3 and use `255 - value` for each colour.

**PWM demo:** wave the fading LED quickly through the air in a dark corner.
Students see a dotted streak, which shows the LED really is blinking.

**Common problems**

- *Colours in the wrong order:* the leg order varies between batches. Swap
  the wires on pins 25/26/27 rather than editing the code.
- *White looks pink or blue:* normal. The three colours aren't equally bright.
  Students can turn one down, e.g. `setColor(255, 200, 150)`.
- *`ledcSetup was not declared`:* the student copied old ESP32 example code
  from the internet. The course uses `analogWrite`, which works on esp32 core
  3.x.
- *One colour is missing:* that leg's resistor isn't in the same row as the
  leg.

**Quiz answers**

1. `0` switches the LED off; `255` makes it fully bright.
2. The LED blinks on and off faster than our eyes can see. If it is on for
   only a small part of each blink, it looks dim.
3. `setColor(0, 0, 255)`.

**Challenge solutions:** `solutions/L05_Rainbow` (challenge 2) and
`solutions/L05_Breathing` (challenge 3, with a 2D array of colours as a
stretch idea). Challenge 1 and the bonus combine earlier sketches.
