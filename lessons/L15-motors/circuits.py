"""Lesson 15 circuits: the power module, an L293D driving the fan motor, then the stepper."""
from circuits import Circuit
from circuits.kit import gnd_b

c = Circuit("L15_fan", "Fan motor: L293D with EN 25, IN1 26, IN2 27; motor power from the power module",
            sketches=["L15_Fan"])
c.power_module("PS1", board="B", col=30)   # feeds both rail pairs of board B with 5 V
gnd_b(c)                                    # shared GND: ESP32 GND -> the module's - rail
c.chip("U1", "L293D", "B:f21")              # notch left: legs 1-8 along row f (cols 21-28)
c.wire("B:b21", "B:tp22")                   # leg 16 (chip power) -> + rail
c.wire("B:j28", "B:+28")                    # leg 8 (motor power) -> + rail
c.wire("B:j24", "B:-24")                    # legs 4 and 5 -> - rail
c.wire("B:j25", "B:-26")
# ESP32 -> chip: three wires round the antenna end of the ESP32, in nested lanes
c.wire("A:i11", "B:g21", via=[(20.0, 14.0), (20.0, 31.0)])   # leg 1 (EN)  <- 25
c.wire("A:h10", "B:h22", via=[(20.35, 13.0), (20.35, 32.0)])  # leg 2 (IN1) <- 26
c.wire("A:g9", "B:i27", via=[(20.7, 12.0), (20.7, 33.0)])     # leg 7 (IN2) <- 27
c.motor("M1", body=(24.5, 44.0), a="B:j23", b="B:j26", rotate=-90)   # legs 3 and 6
c.schematic.module("PS1", right=[("+", "VM"), ("-", "GND")], title="power module (5 V)")
c.schematic.module("U1", left=[("EN1", 25), ("IN1", 26), ("IN2", 27)], top=[("VCC", "VM"), ("VS", "VM")],
                   bottom=[("GND", "GND")], right=[("OUT1", "pair", "OUT2", "M1"), None, ("OUT2",)],
                   title="L293D", numbers={"EN1": 1, "IN1": 2, "IN2": 7, "VCC": 16, "VS": 8, "GND": 4,
                                           "OUT1": 3, "OUT2": 6})

s = Circuit("L15_stepper", "Stepper: ULN2003 board IN1-IN4 on 16, 17, 18, 19; power from the module",
            sketches=["L15_Stepper"])
s.power_module("PS1", board="B", col=30)
gnd_b(s)
s.module("U2", "uln2003", (24, 41.5), rotate=180)   # pins right to left: IN1 24 ... + 19
# Each IN wire runs straight up, then left along its own row to the ESP32 pin: no crossings.
for k, (hole, y) in enumerate((("B:b8", 24), ("B:c9", 25), ("B:d11", 26), ("B:e12", 27))):
    s.wire(f"U2.IN{k + 1}", hole, via=[(24 - k, y)])
s.wire("U2.-", "B:-20")
s.wire("U2.+", "B:+18")
s.schematic.module("PS1", right=[("+", "VM"), ("-", "GND")], title="power module (5 V)")
s.schematic.module("U2", left=[("IN1", 16), ("IN2", 17), ("IN3", 18), ("IN4", 19)], top=[("+", "VM")],
                   bottom=[("-", "GND")], title="ULN2003 + stepper")
