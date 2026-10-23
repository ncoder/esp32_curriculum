# Lesson 6 teacher notes

**Before class:** sort the active and passive buzzers. They look alike from
the top; the passive one has an open bottom with a visible circuit board. Mark
them with a dot of nail polish or tape if you like. Each kit has 5 buttons,
which is exactly enough for the piano.

**Noise:** a classroom of buzzers is loud. Agree on a "hands off" signal, or
let students put a piece of tape over the buzzer hole to quieten it.

**Current:** the buzzers are driven straight from pin 33. At 3.3 V that is
fine for these small buzzers. The active buzzer is quieter than on a 5 V
Arduino; that's expected.

**Common problems**

- *Passive buzzer silent with `tone()`:* the active buzzer was used by
  mistake (it gives a muddy rattle with `tone()`), or the legs are in the same
  row.
- *Melody sounds rushed or wrong:* the arrays have different lengths, or the
  `for` count isn't 14.
- *Piano note stays on:* a key is wired to the wrong leg pair, so it reads as
  always pressed. Use diagonal legs.
- *Piano plays the higher note when two keys are held:* expected. The last
  pressed key in the array wins.

**Quiz answers**

1. Passive.
2. It plays the note C (262 Hz) on the buzzer, until `noTone(BUZZER)`.
3. Item 13 (`notes[13]`), because counting starts at 0.

**Song:** *Twinkle, Twinkle, Little Star*.

**Challenge solutions:** `solutions/L06_Siren` (challenge 2) and
`solutions/L06_PianoLights` (challenge 3). Challenge 1 only changes the
arrays; the bonus is a short combination of L04_ReadKnob and `tone()`.
