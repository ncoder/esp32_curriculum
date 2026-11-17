"""Lesson 18 circuits: IR receiver on 14, then the RGB LED on 25/26/27."""
from circuits import Circuit
from circuits.kit import gnd_a, v33_a

c = Circuit("L18_ir", "IR receiver: S on 14, + to 3V3", sketches=["L18_ReadCodes"])
gnd_a(c)
c.wire("A:f19", "A:+20", bend=0)            # 3V3 -> + rail
c.module("U1", "ir_rx", "A:e26", rotate=180)   # pins - e26, + e25, S e24, dome over the gap
c.wire("U1.-", "A:-26")
c.wire("U1.+", "A:+24")
c.wire("A:i8", "A:c24", via=[(20.5, 14.0), (20.5, 6.0)])   # S -> 14
c.schematic.module("U1", left=[("S", 14)], top=[("+", "3V3")], bottom=[("-", "GND")], title="IR receiver")

r = c.copy("L18_rgb", "Remote control lights: + RGB LED on 25, 26, 27", sketches=["L18_RemoteLights"])
for n, pin_col, out_col in ((1, 11, 12), (2, 10, 10), (3, 9, 8)):
    r.resistor(f"R{n}", "220Ω", f"A:f{pin_col}", f"A:e{out_col}")
r.rgb_led("D1", r="A:c12", k="A:c11", g="A:c10", b="A:c8")
r.wire("D1.K", "A:-")
r.schematic.rgb_led((25, 26, 27), ("R1", "R2", "R3"), "D1")
