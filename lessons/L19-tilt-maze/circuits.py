"""Lesson 19 circuit: GY-6500 and OLED sharing I²C (21/22), buzzer on 33."""
from circuits import Circuit
from circuits.kit import buzzer_side, gnd_a

c = Circuit("L19_tilt", "GY-6500 + OLED on the same I²C pins (SDA 21, SCL 22); buzzer on 33",
            sketches=["L19_Tilt", "L19_RollingBall", "L19_DotGame"])
# OLED standing over the boards' join, powered straight from the ESP32's 3V3 and GND rows
c.module("U1", "oled", "B:a24")                  # GND a24, VCC a25, SCL a26, SDA a27
c.wire("B:b1", "B:b25", bend=0)                  # VCC <- 3V3
c.wire("B:c2", "B:c24", bend=0)                  # GND
# GY-6500 flat in board B's lower half (your game controller). The ESP32's I²C pins go
# to its rows first, and on from there to the OLED: I²C parts can share the two wires.
c.module("U2", "gy6500", "B:j20", rotate=180)   # VCC j20, GND j19, SCL j18, SDA j17, ... FSYNC j11
c.wire("B:e11", "B:f17")                         # SDA <- 21
c.wire("B:e14", "B:f18")                         # SCL <- 22
c.wire("B:g17", "B:d27")                         # SDA -> OLED
c.wire("B:g18", "B:e26")                         # SCL -> OLED
c.wire("B:f19", "B:e24")                         # GND <- the OLED's GND row
c.wire("B:f20", "B:e25")                         # VCC <- the OLED's VCC row (3V3)
gnd_a(c)
buzzer_side(c)
c.schematic.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1", "U2"], power={"VCC": "3V3", "GND": "GND"})
