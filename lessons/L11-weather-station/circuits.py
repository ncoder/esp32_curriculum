"""Lesson 11 circuit: OLED from Lesson 10 + DHT11 on pin 4."""
from circuits import Circuit
from circuits.kit import dht_b, oled_b

c = Circuit("L11_weather", "DHT11 on pin 4 + the OLED from Lesson 10",
            sketches=["L11_ReadDHT", "L11_Station", "L11_Comfort"])
oled_b(c)
dht_b(c)
c.schematic.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1"], power={"VCC": "3V3", "GND": "GND"})
c.schematic.module("U2", left=[("S", 4)], top=[("+", "3V3")], bottom=[("-", "GND")], title="DHT11")
