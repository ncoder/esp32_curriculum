# Lesson 13 teacher notes

**Before class:** power each PIR once and set its TIME knob to the shortest
setting (fully anticlockwise on most HC-SR501 boards) and SENSITIVITY to the
middle. Out of the box some are set to minutes, which makes the alarm look
broken. The knob order differs between makers, so the handout has students
find out which is which by experiment.

**Hardware:** the HC-SR501 needs 5 V on VCC (it has a 3.3 V regulator
inside), and its OUT pin is 3.3 V logic, so it connects directly to GPIO 27.
The "repeat trigger" jumper (H) is not fitted on every board.

**Common problems**

- *Triggers by itself constantly:* still warming up (~60 s), a sunny
  window or heater in view, or SENSITIVITY too high. Twenty laptops' warm air
  can also trigger it.
- *Never triggers:* VCC on 3V3 instead of 5V, or OUT on the wrong pin. Check
  with `L13_Motion` first.
- *LED stays on for ages:* the TIME knob is turned up.
- *Alarm fires immediately when armed:* the student is moving in front of
  it. This is expected; it motivates challenge 2.
- *Button arms and disarms in one press:* the button legs are on the same
  side (always connected). Use diagonally opposite legs.

**Quiz answers**

1. The PIR detects *changes* in infrared (heat) as a warm body moves
   between the lens zones. A still object doesn't change, and a statue isn't
   warm anyway.
2. NOT. `!true` is `false`.
3. The OUT pin stays HIGH for seconds; we only want to count once, at the
   moment it changes from LOW to HIGH (the rising edge).

**Challenge solutions:** `solutions/L13_AlarmLog` covers challenges 2 and 3
(exit delay plus a `mm:ss` log). Challenge 1 just means removing the `tone()`
calls from `siren()`.
