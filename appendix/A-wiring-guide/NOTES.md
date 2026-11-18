# Appendix A teacher notes: wiring guide

The appendix is a reference, not a session. Students reach for it in the final
project (Lesson 21), or when a part they want isn't in a lesson.

## What's in it, and why

- **Index table:** every major part in the ELEGOO ESP-32 Super Starter Kit, with
  the lesson and section that shows it wired up.
- **A1–A10:** a wiring section for each part that no lesson shows simply. The
  rule: a lesson's picture counts when the part appears on its own, or with at
  most one small optional extra (a knob, a button, a buzzer) or with the parts it
  needs to work (resistors, a divider, LEDs that show a chip's outputs). Parts
  that only appear next to bigger parts got their own picture here:
  - button, tilt switch, knob and photoresistor (in Lessons 3–4 they share the
    board with the traffic lights)
  - DHT11 (Lesson 11 pairs it with the OLED), joystick (Lesson 14 keeps the
    servo), GY-6500 (Lesson 19 adds the OLED and a buzzer)
  - thermistor and IR transmitter (only described in words, in challenges)
  - the relay board (not used in any lesson)
- Where a lesson sketch already tests the part (L04_ReadKnob, L11_ReadDHT,
  L14_Joystick, L19_Tilt), the appendix points to it instead of adding a new one.

## Assumptions

| Part | What we assume | If yours differs |
|---|---|---|
| Relay board | A 5V relay module with pins S, +, – and screw terminals NO, COM, NC; switches on when S is HIGH (3.3 V is enough) | A "low-level trigger" board switches on when S is LOW: swap HIGH and LOW in A_Relay. If a board labels its pins IN, VCC, GND, they are S, +, – |
| Thermistor | 10 kΩ NTC, B = 3950 (same as the Lesson 11 bonus) | Readings will be a few degrees off with another B value |
| IR transmitter | Pins S, +, –. Some modules print them in another order | Students match the printed labels |

## Common problems

- *Relay doesn't click, but its red LED lights:* it's a low-level trigger board
  that stays on; swap HIGH and LOW in the sketch.
- *Relay doesn't click and its LED stays dark:* + isn't on 5 V (VIN), or S isn't
  on pin 32.
- *Relay LED is on when it should be off:* the wire is in NC instead of NO.
- *Thermistor reads −273 °C:* pin 34 isn't connected to the divider (it reads 0).
