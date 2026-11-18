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
  - relay, PN2222 transistor and diode (not used in any lesson)
- Where a lesson sketch already tests the part (L04_ReadKnob, L11_ReadDHT,
  L14_Joystick, L19_Tilt), the appendix points to it instead of adding a new one.

## Assumptions

| Part | What we assume | If yours differs |
|---|---|---|
| 5V relay | A bare Songle SRD-05VDC-SL-C (5 pins), not a relay *module*. Coil about 70 mA at 5 V, so it is driven through the PN2222 | A relay **module** (3 pins IN, VCC, GND) has the transistor and diode built in: VCC to VIN, GND to GND, IN to pin 32 |
| PN2222 | TO-92 case, E-B-C left to right with the flat face towards you | Some "2N2222" parts are C-B-E: check the datasheet |
| Thermistor | 10 kΩ NTC, B = 3950 (same as the Lesson 11 bonus) | Readings will be a few degrees off with another B value |
| IR transmitter | Pins S, +, –. Some modules print them in another order | Students match the printed labels |

## Common problems

- *Relay doesn't click:* the transistor is turned round (flat face away), or the
  coil wires are on COM. With the USB plugged in, pin 32 HIGH should read about
  0.1 V at the collector.
- *ESP32 resets when the relay clicks:* the diode is missing or backwards.
- *Relay LED is on when it should be off:* the wire is on NC instead of NO.
- *Thermistor reads −273 °C:* pin 34 isn't connected to the divider (it reads 0).
