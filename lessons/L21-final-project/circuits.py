"""Lesson 21 circuit: the Smart Room Monitor example (DHT11 4, PIR 27, buzzer 33, OLED 21/22)."""
from circuits import Circuit
from circuits.kit import buzzer_side, dht_b, gnd_a, oled_b, v5_a

c = Circuit("L21_smart_room", "Smart Room Monitor: DHT11 on 4, PIR on 27, buzzer on 33, OLED on 21/22",
            sketches=["L21_SmartRoom"])
oled_b(c)
dht_b(c)
gnd_a(c)
v5_a(c)                                   # A's + rail is 5 V, for the PIR only
c.module("U3", "pir", (16, -1.5))        # pins VCC 16, OUT 17, GND 18
c.wire("U3.VCC", "A:+16")
c.wire("U3.GND", "A:-18")
c.wire("U3.OUT", "A:g9", via=[(17.0, 12.5), (9.5, 12.5)])   # OUT -> 27
buzzer_side(c)
c.schematic.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1"], power={"VCC": "3V3", "GND": "GND"})
c.schematic.module("U2", left=[("S", 4)], top=[("+", "3V3")], bottom=[("-", "GND")], title="DHT11")
c.schematic.module("U3", left=[("OUT", 27)], top=[("VCC", "5V")], bottom=[("GND", "GND")], title="PIR HC-SR501")
