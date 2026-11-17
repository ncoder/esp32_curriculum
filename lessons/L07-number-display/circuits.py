"""Lesson 7 circuit: 1-digit display, segments on 23 22 21 19 18 17 16 4, button on 13."""
from circuits import Circuit
from circuits.kit import button, gnd_a, gnd_b

c = Circuit("L07_display", "1-digit display + a button on pin 13",
            sketches=["L07_Segments", "L07_Count", "L07_Dice"])
c.display("U1", "B:h24")          # pin 1 at B:h24; the top pins land in row d
# One 220 Ω resistor per segment, across board B's gap right next to the ESP32 pin,
# then a jumper from the resistor's row to the display pin.
SEGS = [  # segment, ESP32 pin, its column, jumper start, display hole, curve
    ("a", 23, 18, "B:g18", "B:a27", 3.4),
    ("b", 22, 17, "B:i17", "B:b28", 4.2),
    ("c", 21, 14, "B:g14", "B:i27", -1.2),
    ("d", 19, 12, "B:g12", "B:j25", -2.0),
    ("e", 18, 11, "B:j11", "B:i24", -0.8),
    ("f", 17, 9, "B:g9", "B:b25", 2.6),
    ("g", 16, 8, "B:i8", "B:c24", 2.2),
    ("dp", 4, 7, "B:j7", "B:j28", -3.0),
]
for n, (seg, gpio, col, start, hole, bulge) in enumerate(SEGS, 1):
    c.resistor(f"R{n}", "220Ω", f"B:e{col}", f"B:f{col}")
    c.wire(start, hole, bulge=bulge)
c.wire("B:j26", "B:-26")          # COM (pin 3) -> - rail
gnd_b(c)
gnd_a(c)
button(c, "SW1", 13, "A:e21", to=("A:i5", "A:i21"), bend=0)
c.schematic.module("U1", left=[(s, g, [f"R{n}"]) for n, (s, g, *_) in enumerate(SEGS, 1)],
                   bottom=[("COM", "GND")], title="7-segment display",
                   numbers={"a": 7, "b": 6, "c": 4, "d": 2, "e": 1, "f": 9, "g": 10, "dp": 5, "COM": 3},
                   note="R1–R8: 220 Ω")
