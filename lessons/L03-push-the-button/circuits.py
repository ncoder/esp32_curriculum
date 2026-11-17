"""Lesson 3 circuits: a button on 13 next to the traffic lights, then a tilt switch on 14."""
from circuits import Circuit
from circuits.kit import button, gnd_a, traffic_leds

c = Circuit("L03_button", "Traffic lights + a button on pin 13",
            sketches=["L03_Button", "L03_Toggle"])
traffic_leds(c)
gnd_a(c)
button(c, "SW1", 13, "A:e21", to=("A:i5", "A:i21"), bend=0)

t = c.copy("L03_tilt", "Tilt switch on pin 14 (where the second button was)",
           sketches=["L03_Counter", "L03_ShakeAlarm"])
t.tilt("S1", "A:f26", "A:e26")
t.wire("A:h8", "A:h26", bend=0)          # pin 14 -> tilt switch
t.wire("S1.2", "A:-")
t.schematic.chain(14, ["S1"])
