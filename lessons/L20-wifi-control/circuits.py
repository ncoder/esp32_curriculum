"""Lesson 20 circuit: LED on 26, knob on 34 (left leg GND, right leg 3V3)."""
from circuits import Circuit
from circuits.kit import gnd_a, v33_a

c = Circuit("L20_wifi", "LED on 26, knob on 34", sketches=["L20_HelloWeb", "L20_LedControl"])
c.resistor("R1", "220Ω", "A:f10", "A:e10")
c.led("D1", "red", a="A:a10", k="A:-10")
gnd_a(c)
v33_a(c)
c.pot("RV1", "A:e22", "A:e23", "A:e24", side="down")
c.wire("RV1.1", "A:-")        # left leg -> GND
c.wire("RV1.2", "A:+")        # right leg -> 3V3
c.wire("ESP32.34", "RV1.W")
c.schematic.led(26, "R1", "D1")
c.schematic.pot(34, "RV1", ends=("GND", "3V3"))
