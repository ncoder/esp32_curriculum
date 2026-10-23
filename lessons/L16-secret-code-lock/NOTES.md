# Lesson 16 teacher notes

**Before class:** install the **Keypad** library (Mark Stanley, Alexander
Brevig) and check that **ESP32Servo** is still installed. Have plenty of
male-to-male jumpers ready: the keypad alone uses 8.

**Hardware**

- The kit's membrane keypad is assumed to be 4×4 (`123A / 456B / 789C /
  *0#D`), with the connector order R1–R4 then C1–C4 left to right, face up.
  If your keypads are wired the other way round, the keys come out mirrored;
  the handout tells students to flip the plug or reverse the pin arrays.
- Keypad pins (13, 14, 27, 26, 25, 4, 16, 17) are all normal I/O pins. The
  library uses internal pull-ups, so no resistors are needed.
- The servo again runs from the ESP32's 5V pin. A brownout reset when the
  bolt moves means the USB supply is weak (see Lesson 14 notes).

**Common problems**

- *`Keypad.h: No such file`:* library not installed, or the wrong
  "Keypad" was picked; there are several in the Library Manager.
- *Some keys never work:* one row/column wire is loose, or is on an
  input-only pin (34–39 won't work for keypad rows).
- *Correct code says WRONG:* a stray key got added. Press `*` to clear
  first, or print `typed` to see what's in it.
- *Servo twitches at power-up:* normal. It moves to 0° when attached.

**Quiz answers**

1. 5 + 6 = 11 wires; 5 × 6 = 30 keys.
2. `'7'` is a single character (`char`); `"7"` is text (a `String`), even
   if it's only one character long.
3. `"9"`, because `*` cleared `"42"`.

**Challenge solutions:** `solutions/L16_ChangeCode` covers challenges 1–3
(stars, three-strikes lockout, and changing the code with A). The bonus
answer: 1000 possible 3-digit codes (000–999).
