"""Lesson 12 circuits: HC-SR04 (TRIG 17, ECHO 16 through a 1k/2k divider), then a buzzer on 33."""
from circuits import Circuit
from circuits.kit import buzzer33, gnd_a, gnd_b, v5_b

c = Circuit("L12_distance", "Ultrasonic sensor: TRIG 17, ECHO 16 through a 1 kΩ / 2 kΩ divider",
            sketches=["L12_Distance"])
gnd_b(c)
v5_b(c)
# The sensor sits off the board, eyes pointing away, on female-to-male wires.
c.module("U1", "hcsr04", (10, 42.0), rotate=180)   # pins left to right: GND 7, Echo 8, Trig 9, VCC 10
c.wire("U1.VCC", "B:+10")
c.wire("U1.GND", "B:-2")
c.wire("U1.Trig", "B:e7")                  # Trig -> 17 (TX2)
c.wire("U1.Echo", "B:j3")                  # Echo -> row E (column 3)
c.resistor("R1", "1kΩ", "B:g3", "B:g5")    # row E -> row M (column 5)
c.resistor("R2", "2kΩ", "B:h5", "B:-6")    # row M -> - rail
c.wire("B:f5", "B:e6")                     # row M -> 16 (RX2)
c.schematic.module("U1", left=[("Trig", 17), ("Echo", 16, [("shunt", "R2", "GND"), "R1"])],
                   top=[("VCC", "5V")], bottom=[("GND", "GND")], title="HC-SR04",
                   note="R1/R2 turn Echo's 5 V into about 3.3 V")

p = c.copy("L12_parking", "Parking sensor: add the passive buzzer on pin 33", sketches=["L12_Parking"])
gnd_a(p)
buzzer33(p)
