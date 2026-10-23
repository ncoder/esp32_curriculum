# Lesson 3 teacher notes

**Before class:** students should still have the Lesson 2 traffic light on
the breadboard. If not, allow 10 minutes to rebuild it. Count out 2 buttons
and 1 tilt switch per student.

**Pull-ups:** the "pressed = LOW" idea confuses many students. A useful
picture: the pin is held up by a weak spring (the pull-up), and the button
pulls it down to the floor (GND).

**Common problems**

- *LED always on, or always off:* the button is wired to two legs of the same
  internal pair, so it is never "open". Use diagonal legs.
- *Button does nothing:* the button isn't across the middle gap, so all four
  legs are shorted by the breadboard strips.
- *`if (x = LOW)` compiles but behaves strangely:* `=` instead of `==`.
- *Shake alarm triggers on its own or never triggers:* tilt switches are noisy
  and some need a firm shake. Hold the breadboard and shake it, or tap the
  switch with a finger.
- *Counter jumps by 2 or 3:* button bounce. Check the `delay(20);` is there.

**Quiz answers**

1. `LOW`.
2. `=` stores a value in a variable; `==` compares two values.
3. `true` or `false`.

**Challenge solutions:** `solutions/L03_Crossing` (challenge 2) and
`solutions/L03_TwoPlayer` (challenge 3). Challenge 1 is a short edit of
L03_Button. For the bonus, one approach is a press counter (as in
L03_Counter) checked when button 14 is pressed.
