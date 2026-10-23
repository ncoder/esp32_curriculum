# Lesson 7 teacher notes

**Before class:** check that your kit's display is **common cathode** (the
ELEGOO 5161AS is). Test one: put COM (pin 3) to GND and touch pin 7 through a
220 Ω resistor to 3V3. If bar **a** lights, it's common cathode. If yours is
common anode, wire COM to **3V3** instead, and students change
`digitalWrite(segPins[s], digits[n][s])` to `!digits[n][s]` (and `HIGH`↔`LOW`
in L07_Segments).

**Wiring takes most of the first hour.** Twelve-year-olds lose their place
with 9 near-identical rows; insist on ticking the table row by row. Pair
students: one reads the table aloud, the other wires.

**Common problems**

- *Nothing lights:* COM isn't on GND, or the display is upside down (the
  decimal point must be bottom right).
- *One bar dark:* a resistor isn't in the same row as the display pin.
- *Wrong bars light:* two wires are swapped. L07_Segments names each bar in
  the Serial Monitor, so students can find which two.
- *Dice rolls again and again:* students left out the `while` loop that waits
  for the button to be released.
- *Pins 21 and 22* are the I²C pins in later lessons. That doesn't matter
  here, but take these wires out before Lesson 10.

**Quiz answers**

1. b, c, f, g.
2. Row 3 (the digit 3), column 6 (bar g).
3. 1, 2, 3, 4, 5 or 6.

**Challenge solutions:** `solutions/L07_Hex` (challenge 2),
`solutions/L07_DiceSound` (challenges 3 and bonus). The countdown is an edit
to L07_Count: `for (int n = 9; n >= 0; n--)`, then a loop that calls
`showDigit(0)` and switches all bars off with 300 ms gaps.

**Leave it wired:** Lesson 9 reuses pins 23, 22, 21, 19, 18, 17, 16, 4 for
the segments of the 4-digit display.
