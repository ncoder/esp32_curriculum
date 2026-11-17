"""Lesson 13 circuits: PIR on 27 + green LED on 26, then the burglar alarm."""
from circuits import Circuit
from circuits.kit import button, buzzer_side, gnd_a, led_a, v5_a

c = Circuit("L13_motion", "PIR sensor: OUT on 27 (powered from 5V); green LED on 26", sketches=["L13_Motion"])
gnd_a(c)
v5_a(c)                                          # A's + rail is 5 V in this lesson
c.module("U1", "pir", (23, -1.5))               # dome up, pins VCC 23, OUT 24, GND 25
c.wire("U1.VCC", "A:+23")
c.wire("U1.GND", "A:-26")
c.wire("U1.OUT", "A:g9", via=[(24.0, 12.5), (9.5, 12.5)])   # OUT -> 27
led_a(c, "R2", "D2", "green", 10, 10, schematic_gpio=26)
c.schematic.module("U1", left=[("OUT", 27)], top=[("VCC", "5V")], bottom=[("GND", "GND")], title="PIR HC-SR501")

a = c.copy("L13_alarm", "Burglar alarm: + red LED on 25, button on 13, buzzer on 33", sketches=["L13_Alarm"])
led_a(a, "R1", "D1", "red", 11, 12, schematic_gpio=25)
button(a, "SW1", 13, "A:e20", to=("A:i5", "A:i20"), bend=0)
buzzer_side(a)
