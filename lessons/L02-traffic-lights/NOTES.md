# Lesson 2 teacher notes

**Before class:** pre-sort red, yellow and green LEDs and 220 Ω resistors
(red-red-brown) into small cups. Students who kept their Lesson 1 circuit only
need to add two LEDs.

**Warm-up:** many students have never noticed the order of a traffic light.
Draw the sequence on the board together. If you have students from different
countries, compare: the UK and Germany show red + yellow before green, the US
doesn't.

**Common problems**

- *One LED never lights:* backwards LED, or its resistor is in the wrong row.
  Swapping two LEDs quickly shows whether the problem is the LED or the wiring.
- *Wrong colour lights up:* the pins are swapped. Change the wire or the
  `const int` line; both are fine.
- *`'lights' was not declared in this scope`:* a typo in the function name, or
  the function was typed inside `setup()`/`loop()`.
- *The chase sketch lights LEDs in a strange order:* a typo in the array.

**Quiz answers**

1. A named set of instructions you can run (call) whenever you want. It saves
   typing and makes code easier to read and change.
2. 27 (counting starts at 0).
3. 5 times (i = 0, 1, 2, 3, 4).

**Challenge solutions:** `solutions/L02_UKTraffic` (challenge 1) and
`solutions/L02_Bounce` (challenge 3). Challenges 2 and the bonus are small
edits.
