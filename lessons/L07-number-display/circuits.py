"""Lesson 7 circuit: 1-digit display, segments on 23 22 21 19 18 17 16 4, button on 13."""
from circuits import Circuit
from circuits.kit import button, col, gnd_a, gnd_b

c = Circuit("L07_display", "1-digit display + a button on pin 13",
            sketches=["L07_Segments", "L07_Count", "L07_Dice"])
c.display("U1", "B:h22")          # pin 1 at B:h22; the top pins land in row d
# One 220 Ω resistor per segment, across board B's gap right next to the ESP32 pin,
# then a jumper from the resistor's row to the display pin.
SEGS = [  # segment, ESP32 pin, jumper start row, display hole, curve
    ("a", 23, "g", "B:a25", 1.6),
    ("b", 22, "h", "B:b26", 1.8),
    ("c", 21, "i", "B:i25", -1.0),
    ("d", 19, "j", "B:j23", -1.4),
    ("e", 18, "i", "B:i22", -0.8),
    ("f", 17, "g", "B:b23", 2.4),
    ("g", 16, "h", "B:c22", 2.0),
    ("dp", 4, "j", "B:j26", -2.2),
]
for n, (seg, gpio, row, hole, bulge) in enumerate(SEGS, 1):
    k = col(gpio)
    c.resistor(f"R{n}", "220Ω", f"B:e{k}", f"B:f{k}")
    c.wire(f"B:{row}{k}", hole, bulge=bulge)
c.wire("B:j24", "B:-24")          # COM (pin 3) -> - rail
gnd_b(c)
gnd_a(c)
button(c, "SW1", 13, "A:e20", to=("A:i3", "A:i20"), bend=0)
c.schematic.module("U1", left=[(s, g, [f"R{n}"]) for n, (s, g, *_) in enumerate(SEGS, 1)],
                   bottom=[("COM", "GND")], title="7-segment display",
                   numbers={"a": 7, "b": 6, "c": 4, "d": 2, "e": 1, "f": 9, "g": 10, "dp": 5, "COM": 3},
                   note="R1–R8: 220 Ω")
