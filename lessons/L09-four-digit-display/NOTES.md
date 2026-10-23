# Lesson 9 teacher notes

**Before class:** check that the 4-digit display is **common cathode**. In
the ELEGOO kits it is a 5461AS. Test it: put pin 12 (D1) on GND and touch
pin 11 (a) through a 220 Ω resistor to 3V3; the top bar of the first digit
should light. For a common-anode display, swap HIGH/LOW for the digit pins
in `showDigit` and invert the segment values (`!digits[n][s]`).

**Current:** each digit pin sinks the current of up to 8 segments (around
5–6 mA each with 220 Ω at 3.3 V). That is more than the ESP32's recommended
per-pin current, but because each digit is only on 25% of the time and the
GPIO driver limits current, it works fine in practice. If you'd rather be
cautious, use the 330 Ω resistors instead. The display will be a little
dimmer.

**Common problems**

- *Ghosting (faint wrong segments on neighbouring digits):* students changed
  segments before switching the digits off. `showDigit` switches all digits
  off first, so check they typed it in that order.
- *All four digits show the same number:* the digit pins are all connected to
  one rail, or a `digitPins` value is repeated.
- *One digit always dark:* its digit wire. D2 and D3 (pins 9 and 8) sit next
  to each other on the top row and get swapped.
- *Reaction game counts to 9999 and sticks:* the button isn't on pin 13, or
  it's on the wrong pair of legs (always pressed or never pressed).
- *Score 0 every time:* the student is holding the button. That leads straight
  into challenge 1.

**Quiz answers**

1. One.
2. 45 and 7.
3. While `delay()` runs, the code isn't calling `showDigit`, so only the last
   digit stays lit and the others go dark.

**Challenge solutions:** `solutions/L09_Stopwatch` (challenge 3).
Challenge 1: inside the get-ready loop, add
`if (digitalRead(BUTTON_PIN) == LOW) { score = 9999; ... }`; the simplest
version sets a `bool cheated` flag and skips to the show-score step.
Challenge 2: a global `int best = 9999;` and
`if (score < best) { best = score; Serial.println("New record!"); }`.
