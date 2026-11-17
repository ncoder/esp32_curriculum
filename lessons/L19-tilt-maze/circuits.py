"""Lesson 19 circuit: GY-6500 and OLED sharing I²C (21/22), buzzer on 33."""
from circuits import Circuit
from circuits.kit import buzzer_side, gnd_a, oled_b

c = Circuit("L19_tilt", "GY-6500 + OLED on the same I²C pins (SDA 21, SCL 22); buzzer on 33",
            sketches=["L19_Tilt", "L19_RollingBall", "L19_DotGame"])
oled_b(c)
c.module("U2", "gy6500", "B:j19", rotate=180)   # VCC j19, GND j18, SCL j17, SDA j16, ... FSYNC j10
c.wire("B:e14", "B:f16")                         # SDA <- 21 (same row as the OLED's SDA wire)
c.wire("B:e17", "B:f17")                         # SCL <- 22
c.wire("B:e19", "B:f18")                         # GND
c.wire("A:h19", "B:g19", via=[(19.6, 13.0), (19.6, 29.5), (19.0, 29.5)])   # VCC <- 3V3
gnd_a(c)
buzzer_side(c)
c.schematic.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1", "U2"], power={"VCC": "3V3", "GND": "GND"})
