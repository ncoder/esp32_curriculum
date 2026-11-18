"""Lesson 9 circuit: 4-digit display. Segments a-g, dp on 23 22 21 19 18 17 16 4 (through
220 Ω), digits D1-D4 on 25 26 27 32, button on 13."""
from circuits import Circuit
from circuits.kit import col, gnd_a

c = Circuit("L09_four_digits", "4-digit display: segments through 220 Ω, digits on 25, 26, 27, 32",
            sketches=["L09_Multiplex", "L09_Counter", "L09_Reaction"])
c.display("U1", "B:i25", digits=4)   # pins 1-6 along row i (cols 25-30), 12-7 along row e
# Segments: a resistor across board B's gap at each ESP32 pin (as in Lesson 7), then a jumper.
refs = {"a": "R1", "b": "R2", "c": "R3", "d": "R4", "e": "R5", "f": "R6", "g": "R7", "dp": "R8"}
segs = [("a", 23), ("b", 22), ("c", 21), ("d", 19), ("e", 18), ("f", 17), ("g", 16), ("dp", 4)]
for s_, g in segs:
    c.resistor(refs[s_], "220Ω", f"B:e{col(g)}", f"B:f{col(g)}")
# bottom-row display pins: curves under the display's lower edge
for seg, start, hole, bulge in (("e", "B:j9", "B:j25", -1.0), ("d", "B:i10", "B:j26", -1.5),
                                ("dp", "B:j5", "B:j27", -2.4), ("c", "B:h11", "B:j28", -1.9),
                                ("g", "B:i6", "B:j29", -2.9)):
    c.wire(start, hole, bulge=bulge)
# top-row display pins: up past the display's left end, then along rows a-d
c.wire("B:g15", "B:d26", via=[(16.4, 31.0), (16.4, 26.0)])               # a <- 23
c.wire("B:h14", "B:c30", via=[(15.6, 32.0), (15.6, 28.6), (16.9, 28.6), (16.9, 25.0)])  # b <- 22
c.wire("B:j7", "B:b27", via=[(7.0, 34.6), (17.4, 34.6), (17.4, 24.0)])  # f <- 17
# digits: straight from the ESP32's top row, round its antenna end, no resistors
c.wire("A:f8", "B:a25", via=[(19.8, 11.0), (19.8, 23.0)])    # D1 <- 25
c.wire("A:g7", "B:a28", via=[(20.6, 12.0), (20.6, 22.4), (28.0, 22.4)])  # D2 <- 26
c.wire("A:h6", "B:a29", via=[(21.4, 13.0), (21.4, 21.8), (29.0, 21.8)])  # D3 <- 27
c.wire("A:i10", "B:j30", via=[(22.2, 14.0), (22.2, 21.2), (31.3, 21.2), (31.3, 35.0), (30.0, 35.0)])  # D4 <- 32
gnd_a(c)
c.button("SW1", "A:e24")
c.wire("A:f3", "A:a24", bulge=1.0)  # 13 -> button
c.wire("SW1.2", "A:-")
c.schematic.chain(13, ["SW1"])
c.schematic.module("U1", left=[(s_, g, [refs[s_]]) for s_, g in segs] + [("D1", 25), ("D2", 26), ("D3", 27), ("D4", 32)],
                   title="4-digit display",
                   numbers={"a": 11, "b": 7, "c": 4, "d": 2, "e": 1, "f": 10, "g": 5, "dp": 3,
                            "D1": 12, "D2": 9, "D3": 8, "D4": 6},
                   note="R1–R8: 220 Ω. A digit lights when its D pin is LOW.")
