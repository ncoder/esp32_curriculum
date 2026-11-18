"""Lesson 20 circuit: LED on 26, knob on 34 (left leg GND, right leg 3V3)."""
from circuits import Circuit
from circuits.kit import gnd_a, led_a, pot_a, v33_a

c = Circuit("L20_wifi", "LED on 26, knob on 34", sketches=["L20_HelloWeb", "L20_LedControl"])
led_a(c, "R1", "D1", "red", 26, 8)
gnd_a(c)
v33_a(c)
pot_a(c, left="-", right="+")
