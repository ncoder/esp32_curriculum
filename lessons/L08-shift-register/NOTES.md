# Lesson 8 teacher notes

**Before class:** take the 7-segment wiring from Lesson 7 off the breadboard.
Pins 18, 19 and 23 are reused here. If you have a spare 74HC595, show it
under a magnifier; the notch and pin numbering confuse many students.

**Bit order:** `shiftOut(..., MSBFIRST, ...)` sends bit 7 first, so it ends
up on Q7 and bit 0 on Q0. With LEDs wired Q7 (left) to Q0 (right), the
LEDs read exactly like the binary number in the Serial Monitor. If a student
wires them the other way round, the program still works but the count reads
backwards. That makes a nice discussion point.

**Common problems**

- *No LEDs, chip cold:* MR (pin 10) is not tied to 3V3, or OE (pin 13) is not
  tied to GND. Both are easy to forget.
- *Random flickering:* the ESP32's GND isn't connected to the chip's GND rail.
- *All LEDs lit faintly:* the + and – rails are swapped on one breadboard.
  Some 400-point boards have their red/blue lines on opposite sides.
- *Order scrambled:* Q0 is on pin 15, on the *other* side of the chip from
  Q1–Q7. Students often put Q0 next to Q1.
- *Pot reads 0 or 4095 only:* the middle leg isn't the one going to pin 34.

**Quiz answers**

1. DATA carries the next bit, CLOCK says "take it" and shifts everything
   along, and LATCH copies all 8 bits to the outputs at once.
2. `00001010`.
3. 255 (`11111111`).

**Challenge solutions:** `solutions/L08_KnightRider` (challenge 2) and
`solutions/L08_BarGraph` (challenge 3). Challenge 1 only edits the
`patterns` array. For the bonus, use `showByte(random(1, 16))` and wait for
a button press.
