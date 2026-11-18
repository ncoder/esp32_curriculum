"""Lesson 1 circuit: one LED on pin 26. Run `make circuits` to redraw."""
from circuits import Circuit
from circuits.kit import gnd_a

c = Circuit("L01_blink", "One red LED on pin 26", sketches=["L01_Blink"])
c.resistor("R1", "220Ω", "A:f7", "A:e8")        # from the D26 row, across the gap
c.led("D1", "red", a="A:a8", k="A:-8")           # short leg straight into the - rail
gnd_a(c)
c.schematic.led(26, "R1", "D1")
