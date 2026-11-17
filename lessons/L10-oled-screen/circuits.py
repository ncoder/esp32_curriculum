"""Lesson 10 circuit: OLED screen on I²C (SDA 21, SCL 22)."""
from circuits import Circuit
from circuits.kit import oled_b

c = Circuit("L10_oled", "OLED screen: SDA 21, SCL 22, VCC 3V3", sketches=["L10_Hello", "L10_Shapes", "L10_Bounce"])
oled_b(c)
c.schematic.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1"], power={"VCC": "3V3", "GND": "GND"})
