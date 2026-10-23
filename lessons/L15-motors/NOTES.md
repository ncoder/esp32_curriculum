# Lesson 15 teacher notes

**Before class:** check every 9 V battery (or plan to use a second USB
cable/charger into the power module's USB socket, which is cheaper and lasts
all day). Check that the power module's rail pins match the breadboard's +/–
markings when it is pushed in; on some breadboards it only fits one way
round correctly.

**Safety:** this is the first lesson with a second power source. The two
rules that matter: (1) the ESP32's 5V/3V3 pins must not be wired to the
module's rails, and (2) GND must be shared. Check every student's power
wiring before they switch on.

**Hardware**

- L293D: leg 16 (VCC1, logic) needs ≥ 4.5 V, so it is on the module's 5 V
  rail, not 3V3. The inputs accept 3.3 V signals (high threshold 2.3 V).
  The chip loses about 1.5–2 V internally, so the 3–6 V motor sees about
  3–3.5 V. That's enough to spin the fan, but low PWM values (< ~130) may
  not start it.
- The kit's DC motor may have bare tabs. If so, twist jumper wire ends
  through the tabs or use the crocodile clips if you have them.
- 28BYJ-48: 2048 full steps per output revolution (32 steps × ~64:1
  gearbox). The sketch uses 2-phase full stepping (two coils on), which gives
  good torque. Below ~2 ms per step it stalls and just buzzes.
- All motors are powered from the module. Keep the ULN2003 jumper (if
  present) on so the board gets power.

**Common problems**

- *Nothing moves but the ESP32 runs:* module switched off, flat battery, or
  ESP32 GND not connected to the module's – rail.
- *Fan only goes one way:* IN1/IN2 wires are on the wrong legs (2 and 7).
- *Stepper vibrates but doesn't turn:* IN1–IN4 are in the wrong order, or
  the delay is too short.
- *Chip gets hot:* GND legs 4/5 not connected, or the motor wires are
  shorted together. Switch off immediately.

**Quiz answers**

1. A motor needs much more current than a pin can give; it could damage the
   ESP32. We use a driver chip and a separate supply.
2. Swap IN1 and IN2 (one HIGH, one LOW the other way round).
3. 2.

**Challenge solutions:** `solutions/L15_FanKnob` (challenge 1) and
`solutions/L15_Clock` (challenge 3). Challenge 2:
`int steps = degrees * 2048L / 360;` then loop `abs(steps)` times calling
`step(steps > 0 ? 1 : -1)`.
