"""Lesson 5 circuit: RGB LED on 25/26/27 (the Lesson 2 resistors stay), knob on 34."""
from circuits import Circuit
from circuits.kit import col, gnd_a, pot_a, v33_a

c = Circuit("L05_rgb", "RGB LED: red 25, green 26, blue 27; knob on 34",
            sketches=["L05_Fade", "L05_ColorMixer", "L05_KnobColor"])
for n, gpio, out_col in ((1, 25, 10), (2, 26, 8), (3, 27, 6)):
    c.resistor(f"R{n}", "220Ω", f"A:f{col(gpio)}", f"A:e{out_col}")
c.rgb_led("D1", r="A:c10", k="A:c9", g="A:c8", b="A:c6")
c.wire("D1.K", "A:-")
c.note("Here the RGB LED is turned round: from left to right its legs are blue, green, GND (longest), red.")
gnd_a(c)
v33_a(c)
pot_a(c, schematic=False)
c.schematic.rgb_led((25, 26, 27), ("R1", "R2", "R3"), "D1")
c.schematic.pot(34, "RV1")
