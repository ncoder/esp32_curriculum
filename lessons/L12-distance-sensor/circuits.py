"""Lesson 12 circuits: HC-SR04 (TRIG 17, ECHO 16 through a 1k/2k divider), then a buzzer on 33."""
from circuits import Circuit
from circuits.kit import buzzer33, gnd_a, gnd_b, v5_b

c = Circuit("L12_distance", "Ultrasonic sensor: TRIG 17, ECHO 16 through a 1 kΩ / 2 kΩ divider",
            sketches=["L12_Distance"])
gnd_b(c)
v5_b(c)
# The sensor sits off the board, eyes pointing away, on female-to-male wires.
c.module("U1", "hcsr04", (11, 42.0), rotate=180)   # pins left to right: GND, Echo, Trig, VCC
c.wire("U1.VCC", "B:+11")
c.wire("U1.GND", "B:-6")
c.wire("U1.Trig", "B:e9")                  # Trig -> 17
c.wire("U1.Echo", "B:j5")                  # Echo -> row E (column 5)
c.resistor("R1", "1kΩ", "B:g5", "B:g7")    # row E -> row M (column 7)
c.resistor("R2", "2kΩ", "B:h7", "B:-8")    # row M -> - rail
c.wire("B:f7", "B:e8")                     # row M -> 16
c.schematic.module("U1", left=[("Trig", 17), ("Echo", 16, [("shunt", "R2", "GND"), "R1"])],
                   top=[("VCC", "5V")], bottom=[("GND", "GND")], title="HC-SR04",
                   note="R1/R2 turn Echo's 5 V into about 3.3 V")

p = c.copy("L12_parking", "Parking sensor: add the passive buzzer on pin 33", sketches=["L12_Parking"])
gnd_a(p)
buzzer33(p)
