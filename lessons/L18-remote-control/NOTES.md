# Lesson 18 teacher notes

**Before class:** check every remote has a working CR2025 battery (pull-tab
removed when you test). Pre-install **IRremote** (v4.x) if computers are
offline. Older tutorials use IRremote 2.x code (`IRrecv irrecv(pin)`,
`results.value`), which does **not** compile with 4.x. If a student copies
code from the internet, that's the usual reason it fails.

**Codes:** `L18_RemoteLights` uses the NEC command codes of the usual ELEGOO
21-key remote: POWER 0x45, VOL+ 0x46, FUNC/STOP 0x47, |<< 0x44, >|| 0x40,
>>| 0x43, DOWN 0x07, VOL– 0x15, UP 0x09, 0 0x16, EQ 0x19, ST/REPT 0x0D,
1 0x0C, 2 0x18, 3 0x5E, 4 0x08, 5 0x1C, 6 0x5A, 7 0x42, 8 0x52, 9 0x4A.
If a kit's remote differs, students use the codes they recorded in Sketch 1,
which is why that step comes first.

**Holding a button:** NEC sends a short "repeat" frame while a key is held.
IRremote 4.x reports it with the same command and
`IRDATA_FLAGS_IS_REPEAT` set. Sketch 1 shows the same code repeating; the
Dimmer solution uses the flag so that colours don't re-trigger but VOL+/–
keep ramping.

**Common problems**

- *Nothing received:* signal not on 14, or + and – swapped on the module
  (it gets warm, so unplug quickly).
- *Codes are random/0:* sunlight or fluorescent light, or a non-NEC remote.
  IRremote prints the protocol with `IrReceiver.printIRResultShort(&Serial);`
  which helps debug.
- *Colour wrong:* RGB leg order differs between batches; swap wires rather
  than code.

**Quiz answers**

1. It is infrared, which human eyes can't see.
2. Leaves the switch, so the next case isn't run too.
3. 16.
4. TV, air conditioner, sound bar, set-top box, LED light strips, toy cars…

**Challenge solutions:** `solutions/L18_Dimmer` (challenges 1–3 together),
`solutions/L18_Sender` (bonus transmitter; needs two ESP32s, or the same board
running both sketches one after the other).
