"""Lesson 14 circuits: servo on 18, then the joystick (VRx 34, VRy 35, SW 14)."""
from circuits import Circuit
from circuits.kit import gnd_a, gnd_b, v33_a, v5_b

c = Circuit("L14_servo", "Servo: signal on 18, power from VIN (5 V)", sketches=["L14_Sweep"])
gnd_b(c)
v5_b(c)
c.servo("M1", body=(20, 44), gnd="B:-15", vcc="B:+16", sig="B:j9", rotate=0)
c.wire("B:f9", "B:e9")                        # servo signal row -> D18
c.schematic.module("M1", left=[("SIG", 18)], top=[("+5V", "5V")], bottom=[("GND", "GND")],
                   title="SG90 servo", note="orange = signal, red = +5V, brown = GND")

j = c.copy("L14_joystick", "Joystick: VRx 34, VRy 35, SW 14, + to 3V3 (not 5V!)",
           sketches=["L14_Joystick", "L14_Pointer"])
gnd_a(j)
v33_a(j)                                       # A's + rail is 3V3
j.module("U1", "joystick", (22, -1.5))         # pins GND 22, +5V 23, VRx 24, VRy 25, SW 26
j.wire("U1.GND", "A:-21")
j.wire("U1.+5V", "A:+23")                     # + goes to 3V3, not 5V!
j.wire("U1.VRx", "A:g12")                     # VRx -> 34
j.wire("U1.VRy", "A:h11")                     # VRy -> 35
j.wire("U1.SW", "A:i5", via=[(26.6, 14.55), (5.0, 14.55)])   # SW -> 14, round the other wires
j.schematic.module("U1", left=[("VRx", 34), ("VRy", 35), ("SW", 14)], top=[("+5V", "3V3")],
                   bottom=[("GND", "GND")], title="Joystick")
