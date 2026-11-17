"""Lesson 9 circuit: 4-digit display. Segments a-g, dp on 23 22 21 19 18 17 16 4 (through
220 Ω), digits D1-D4 on 25 26 27 32, button on 13."""
from circuits import Circuit
from circuits.kit import button, gnd_a

c = Circuit("L09_four_digits", "4-digit display: segments through 220 Ω, digits on 25, 26, 27, 32",
            sketches=["L09_Multiplex", "L09_Counter", "L09_Reaction"])
c.display("U1", "B:i25", digits=4)   # pins 1-6 along row i, 12-7 along row e
# Bottom-row segments: resistors across board B's gap at the ESP32 pin (as in Lesson 7),
# then jumpers that curve under the display to its pins.
bottom = [  # segment, ESP32 pin, column, jumper start, display hole, curve
    ("e", 18, 11, "B:h11", "B:j25", -1.0),
    ("d", 19, 12, "B:j12", "B:j26", -1.5),
    ("dp", 4, 7, "B:j7", "B:j27", -2.6),
    ("c", 21, 14, "B:h14", "B:j28", -1.9),
    ("g", 16, 8, "B:h8", "B:j29", -3.2),
]
refs = {"a": "R1", "b": "R2", "c": "R3", "d": "R4", "e": "R5", "f": "R6", "g": "R7", "dp": "R8"}
for seg, gpio, col, start, hole, bulge in bottom:
    c.resistor(refs[seg], "220Ω", f"B:e{col}", f"B:f{col}")
    c.wire(start, hole, bulge=bulge)
# Top-row segments: the display covers the gap there, so these resistors lie flat in the
# free rows above it.
c.resistor("R1", "220Ω", "B:b18", "B:b22")      # a <- 23
c.wire("B:a22", "B:a26", bend=0)
c.resistor("R2", "220Ω", "B:c17", "B:c21")      # b <- 22
c.wire("B:d21", "B:d30", bend=0)
c.wire("B:b9", "B:a24", bulge=2.0)              # f <- 17 (jumper first, then the resistor)
c.resistor("R6", "220Ω", "B:c24", "B:c27")
# Digits: straight from the ESP32's top row, no resistors
c.wire("A:f11", "B:a25", bulge=2.5)   # D1 <- 25
c.wire("A:g10", "B:b28", bulge=3.0)   # D2 <- 26
c.wire("A:h9", "B:a29", bulge=3.6)    # D3 <- 27
c.wire("A:i13", "B:j30", via=[(16.5, 14.0), (16.5, 34.55), (29.6, 34.55)])  # D4 <- 32, round the display
gnd_a(c)
button(c, "SW1", 13, "A:e21", to=("A:i5", "A:i21"), bend=0)

segs = [("a", 23), ("b", 22), ("c", 21), ("d", 19), ("e", 18), ("f", 17), ("g", 16), ("dp", 4)]
c.schematic.module("U1", left=[(s, g, [refs[s]]) for s, g in segs] + [("D1", 25), ("D2", 26), ("D3", 27), ("D4", 32)],
                   title="4-digit display",
                   numbers={"a": 11, "b": 7, "c": 4, "d": 2, "e": 1, "f": 10, "g": 5, "dp": 3,
                            "D1": 12, "D2": 9, "D3": 8, "D4": 6},
                   note="R1–R8: 220 Ω. A digit lights when its D pin is LOW.")
