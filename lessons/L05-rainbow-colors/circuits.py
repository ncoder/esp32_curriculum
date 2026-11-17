"""Lesson 5 circuit: RGB LED on 25/26/27 (the Lesson 2 resistors stay), knob on 34."""
from circuits import Circuit
from circuits.kit import gnd_a, v33_a

c = Circuit("L05_rgb", "RGB LED: red 25, green 26, blue 27; knob on 34",
            sketches=["L05_Fade", "L05_ColorMixer", "L05_KnobColor"])
for n, pin_col, out_col in ((1, 11, 12), (2, 10, 10), (3, 9, 8)):
    c.resistor(f"R{n}", "220Ω", f"A:f{pin_col}", f"A:e{out_col}")
# Seen from the front the legs run blue, green, GND (longest), red: the LED is turned round.
c.rgb_led("D1", r="A:c12", k="A:c11", g="A:c10", b="A:c8")
c.wire("D1.K", "A:-")
c.note("Here the RGB LED is turned round: from left to right its legs are blue, green, GND (longest), red.")
gnd_a(c)
v33_a(c)
c.pot("RV1", "A:e22", "A:e23", "A:e24", side="down")
c.wire("RV1.1", "A:+")
c.wire("RV1.2", "A:-")
c.wire("ESP32.34", "RV1.W")
c.schematic.rgb_led((25, 26, 27), ("R1", "R2", "R3"), "D1")
c.schematic.pot(34, "RV1")
