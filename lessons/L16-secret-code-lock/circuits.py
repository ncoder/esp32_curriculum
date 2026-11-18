"""Lesson 16 circuits: 4x4 keypad (rows 13 14 27 26, columns 25 4 16 17) + buzzer, then the lock parts."""
from circuits import Circuit
from circuits.kit import buzzer_side, gnd_a, gnd_b, led_b, v5_b

c = Circuit("L16_keypad", "Keypad: rows on 13, 14, 27, 26; columns on 25, 4, 16, 17; buzzer on 33",
            sketches=["L16_Keys"])
gnd_a(c)
c.module("K1", "keypad", (2, -1.5))           # pins R1 R2 R3 R4 C1 C2 C3 C4 at x = 2 ... 9
for pin, hole in (("R1", "A:i3"), ("R2", "A:h5"), ("R3", "A:g6"), ("R4", "A:f7"), ("C1", "A:g8")):
    c.wire(f"K1.{pin}", hole)
# the column wires go round the USB end of the ESP32 to its bottom row
for pin, hole, x in (("C2", "B:b5", -3.6), ("C3", "B:c6", -4.2), ("C4", "B:d7", -4.8)):
    c.wire(f"K1.{pin}", hole, via=[(x, -0.6), (x, 24 + "bcd".index(hole[2]))])
buzzer_side(c)
c.schematic.module("K1", left=[("R1", 13), ("R2", 14), ("R3", 27), ("R4", 26),
                               ("C1", 25), ("C2", 4), ("C3", 16), ("C4", 17)], title="4×4 keypad")

d = c.copy("L16_lock", "The lock: servo on 18 (5 V), red LED on 19, green LED on 23", sketches=["L16_Lock"])
led_b(d, "R1", "D1", "red", 19, led_col=12)
led_b(d, "R2", "D2", "green", 23)
d.servo("M1", body=(2, 44), gnd="B:-6", vcc="B:+8", sig="B:j9", rotate=0)
d.wire("B:f9", "B:e9")                     # servo signal row -> D18
gnd_b(d)
v5_b(d)
d.schematic.module("M1", left=[("SIG", 18)], top=[("+5V", "5V")], bottom=[("GND", "GND")], title="SG90 servo")
