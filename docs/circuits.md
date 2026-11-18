# Drawing a lesson's circuit

Every wiring step in a handout shows two pictures side by side:

- a **circuit diagram** (schematic): the formal drawing, with part numbers, values and pin numbers
- a **breadboard picture**: what the circuit looks like on the two clipped-together breadboards

Both pictures come from one description in the lesson's `circuits.py`, drawn by
`tools/draw_circuits.py`. The tool also **checks** that the two pictures make
exactly the same connections, and that every pin the lesson's sketches use is
wired. You never draw or edit the SVG files by hand.

```
make circuits              # draw and check every lesson
make circuits LESSON=L05   # just one
```

The pictures land in `lessons/LNN-name/diagrams/NAME.schematic.svg` and
`NAME.breadboard.svg`, and are committed so they show up on GitHub. In
`lesson.md`, put `@circuit NAME` on its own line, usually right after the wiring
table, to show both pictures in the handout.

Appendices work the same way: `appendix/A-wiring-guide/circuits.py` is drawn by
`make circuits` too. An appendix circuit may list a lesson's sketch in `sketches`
(the check finds it in `lessons/`).

## A first example

```python
"""Lesson 1 circuit: one LED on pin 26."""
from circuits import Circuit
from circuits.kit import gnd_a

c = Circuit("L01_blink", "One red LED on pin 26", sketches=["L01_Blink"])
c.resistor("R1", "220Ω", "A:f10", "A:e10")      # from the pin 26 row, across the gap
c.led("D1", "red", a="A:a10", k="A:-10")         # short leg straight into the - rail
gnd_a(c)                                         # ESP32 GND -> board A's - rail
c.schematic.led(26, "R1", "D1")                  # GPIO26 -> R1 -> D1 -> GND
```

The first half places parts and wires on the breadboard. The last line describes
the same circuit for the schematic, using a ready-made pattern. `sketches` lists
the sketches that run on this circuit; the check makes sure their pins are wired.

## The breadboard

Board **A** is on top, board **B** below, and the ESP32 lies across the join
with its USB socket on the left. Its top row of pins is in row **j** of board A,
and its bottom row is in row **a** of board B, in columns 1–15:

```
board A row j:  VIN GND D13 D12 D14 D27 D26 D25 D33 D32 D35 D34 VN VP EN       (columns 1-15)
board B row a:  3V3 GND D15 D2  D4  RX2 TX2 D5  D18 D19 D21 RX0 TX0 D22 D23    (columns 1-15)
```

`tools/circuits/kit.py` has the same table as `COL`, so `col(26)` gives 7.

So each top-row pin has 4 free holes above it (rows f–i of board A), and each
bottom-row pin has 4 free holes below it (rows b–e of board B). The rest of the
space is free: board A's rows a–e, board B's rows f–j, and both boards'
columns 16–30. The 3V3 pin is on the bottom row: `kit.v33_b` wires it to board
B's + rail, and `kit.v33_a` takes it round the USB end to board A's + rail.

This is ELEGOO's 30-pin ESP32 DevKit V1. For a board with a different pin order,
change `ESP32_TOP` and `ESP32_BOTTOM` in `tools/circuits/parts.py` (and `COL`
in `kit.py`), then re-place the parts and run `make circuits`.

**Hole names:** `A:c12` is board A, row c, column 12. The outer rails are
`A:+12`, `A:-12` (the top edge of board A) and `B:+12`, `B:-12` (the bottom edge
of board B). The rails have no holes at columns 1, 7, 13, 19 and 25, and the
tool says so if you try. The inner rails, under the ESP32 but free from column
20 on, are `A:bn22`/`A:bp22` (board A's bottom −/+) and `B:tn22`/`B:tp22`
(board B's top −/+).

## Parts

| Call | Part |
|---|---|
| `c.resistor("R1", "220Ω", a, b)` | resistor; colour bands come from the value |
| `c.led("D1", "red", a=..., k=...)` | LED: `a` is the long (+) leg, `k` the short leg |
| `c.rgb_led("D1", r=, k=, g=, b=)` | common-cathode RGB LED |
| `c.button("SW1", "A:e21", width=2)` | push button across the gap (top-left leg in row e) |
| `c.pot("RV1", left, middle, right, side="up")` | potentiometer; the knob is drawn above or below |
| `c.ldr("LDR1", a, b)`, `c.tilt("S1", a, b)` | photoresistor, tilt switch |
| `c.thermistor("TH1", a, b)` | thermistor |
| `c.diode("D1", a=..., k=...)` | rectifier diode: `k` is the striped end |
| `c.transistor("Q1", e=, b=, c=)` | PN2222 (TO-92), three legs side by side, flat face towards you |
| `c.buzzer("BZ1", plus, minus, active=False)` | buzzer |
| `c.chip("U1", "74HC595", "B:f22")` | 16-leg chip across the gap, notch left, pin 1 in row f (`L293D` too) |
| `c.display("U1", "B:h24", digits=1)` | 1- or 4-digit 7-segment display, pin 1 in row f–i |
| `c.module("U1", "oled", "B:e27", rotate=180)` | a module plugged in by its header; `rotate=180` hangs it below the pins |
| `c.module("U1", "pir", (23, -1.5))` | a module off the board (a point, in pitches), joined with jumper wires |
| `c.servo("M1", body=(x, y), gnd=, vcc=, sig=)` | servo with its leads in holes |
| `c.motor("M1", body=(x, y), a=, b=)` | DC motor |
| `c.power_module("PS1", board="B", col=30)` | breadboard power supply on the right-hand end of a board |

Module kinds: `oled`, `dht11`, `ir_rx`, `ir_tx`, `gy6500`, `hcsr04`, `pir`, `joystick`,
`rc522`, `keypad`, `uln2003`, `relay` (the bare 5V relay, off the board on
female-to-male wires; `rotate=90` stands it beside the board). Their pins are listed in `MODULES` in
`tools/circuits/parts.py`. A new kind needs a pin list there and a small
`_draw_<kind>` method.

## Wires

```python
c.wire("ESP32.26", "R1.1")          # nearest free hole next to each pin
c.wire("ESP32.GND", "A:-")          # nearest free hole on a rail
c.wire("A:i5", "A:i21", bend=0)     # exact holes, drawn straight
c.wire("A:g9", "B:i27", via=[(20.7, 12.0), (20.7, 33.0)])   # routed round the ESP32
c.wire("B:f9", "B:g28", bulge=2.4)  # a curve this many pitches high (negative: the other way)
```

A wire end can be a hole, a rail, or a part's pin (`ESP32.26`, `ESP32.3V3`,
`R1.2`, `OLED.SDA`). For a pin in the breadboard, the tool picks the nearest free
hole in the same strip. For a module off the board, the wire goes to the pin
itself. Colours follow the net: black for GND, orange for 3V3, red for 5V, and a
different colour for each signal. Pass `color="#..."` to override.

Two things can't share a hole: the tool stops with a message naming both.

## The schematic patterns

| Call | Draws |
|---|---|
| `s.led(26, "R1", "D1")` | pin → resistor → LED → GND |
| `s.chain(13, ["SW1"], end="GND")` | pin → any two-leg parts in a row → GND (or `"3V3"`) |
| `s.pot(34, "RV1", ends=("3V3", "GND"))` | knob between two supplies, middle leg to the pin |
| `s.divider(35, top="LDR1", bottom="R4")` | 3V3 → top → pin → bottom → GND |
| `s.rgb_led((25, 26, 27), ("R1", "R2", "R3"), "D1")` | three resistors into one RGB LED |
| `s.module("U1", left=[...], top=[...], bottom=[...], right=[...])` | a block with pins, wired to the ESP32 |
| `s.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1", "U2"], power={...})` | shared I²C lines with modules underneath |
| `s.relay(32, "R1", "Q1", "K1", "D1", load=["R2", "D2"])` | pin → base resistor → NPN transistor → relay coil to 5V, diode across the coil; the switch takes 5V from COM to the `load` parts and GND |

`module()` covers chips, displays and sensor modules:

- `left`: `(pin, gpio)` wires the pin to an ESP32 GPIO; `(pin, gpio, ["R1"])`
  puts a resistor in the way; `(pin, gpio, [("shunt", "R2", "GND"), "R1"])` also
  hangs R2 from the wire to GND (a voltage divider).
- `top` / `bottom`: `(pin, net)` with net `"3V3"`, `"5V"`, `"GND"` or `"VM"`
  (the power module's 5 V).
- `right`: `(pin, net)`, `(pin, "chain", ["D1", "R1"], "GND")` for an LED on an
  output, or `(pin, "pair", other_pin, "M1")` for a motor between two outputs.
- `numbers={"DATA": 14, ...}` prints the chip's pin numbers; `note="..."` adds a
  line underneath.

## Lessons that build up a circuit

A lesson that adds parts in steps copies the previous step and adds to it:

```python
c = Circuit("L12_distance", "Ultrasonic sensor ...", sketches=["L12_Distance"])
...
p = c.copy("L12_parking", "Add the buzzer on pin 33", sketches=["L12_Parking"])
buzzer33(p)
```

`c.remove("SW2")` takes a part out again, along with its wires and schematic.

## Standard builds

`tools/circuits/kit.py` keeps parts that come back lesson after lesson in the
same holes, so the pictures match what students already have on their boards:
`traffic_leds`, `buzzer33`, `buzzer_side`, `button`, `led_a`, `led_b`,
`oled_b`, `dht_b`, and the power wires `gnd_a`, `gnd_b`, `v33_a`, `v5_a`,
`v5_b`. Use these first, and add to them when a new part starts coming back.

## When the check fails

```
FAIL  L07_display
      breadboard joins  ESP32.GPIO23, R1.~  but the schematic doesn't
      schematic joins   ESP32.GPIO22, R1.~  but the breadboard doesn't
```

The two pictures disagree: here R1 is wired to pin 23 on the breadboard, but the
schematic says 22. (`~` marks either leg of a part that works both ways round.)
`sketch L07_Count uses pin(s) 4, which are not wired` means the circuit is
missing a part the sketch needs.

Look at the result before committing. Wires should not cross a part's body, and
labels should not cover holes that students need. Open the SVGs, or build the
handout with `make pdfs LESSON=L07`.
