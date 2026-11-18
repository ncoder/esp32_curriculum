"""Lesson 4 circuits: a knob on pin 34, then a light sensor on pin 35."""
from circuits import Circuit
from circuits.kit import gnd_a, pot_a, traffic_leds, v33_a

c = Circuit("L04_knob", "Potentiometer on pin 34 (LEDs from Lesson 2 still in place)",
            sketches=["L04_ReadKnob", "L04_SpeedKnob"])
traffic_leds(c)
gnd_a(c)
v33_a(c)
pot_a(c)

d = c.copy("L04_light", "Photoresistor + 10 kΩ divider on pin 35", sketches=["L04_NightLight"])
d.ldr("LDR1", "A:a16", "A:+16")                 # one leg straight into the + rail
d.resistor("R4", "10kΩ", "A:b16", "A:-18")      # from the same row to the - rail
d.wire("ESP32.35", "LDR1.1")
d.schematic.divider(35, top="LDR1", bottom="R4")
