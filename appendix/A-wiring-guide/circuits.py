"""Appendix A circuits: one part on its own, for the parts that no lesson shows on their own.

Parts that a lesson already shows simply are not repeated here: the appendix
points to that lesson's picture instead.
"""
from circuits import Circuit
from circuits.kit import button, dht_b, gnd_a, gnd_b, pot_a, v33_a, v33_b, v5_a

# ---------------------------------------------------------------- inputs
b = Circuit("A_button", "Push button on pin 13 (other leg to GND)", sketches=["A_Button"])
gnd_a(b)
button(b, "SW1", 13, "A:e20", to=("A:i3", "A:i20"), bend=0)

t = Circuit("A_tilt", "Tilt switch on pin 14 (other leg to GND)", sketches=["A_Tilt"])
gnd_a(t)
t.tilt("S1", "A:f25", "A:e25")
t.wire("A:h5", "A:h25", bend=0)               # D14 -> tilt switch
t.wire("S1.2", "A:-")
t.schematic.chain(14, ["S1"])

k = Circuit("A_knob", "Potentiometer: outer legs to 3V3 and GND, middle leg to pin 34",
            sketches=["L04_ReadKnob"])
gnd_a(k)
v33_a(k)
pot_a(k)

l = Circuit("A_light", "Photoresistor from 3V3 to pin 35, 10 kΩ from pin 35 to GND",
            sketches=["A_Light"])
gnd_a(l)
v33_a(l)
l.ldr("LDR1", "A:a16", "A:+16")               # one leg straight into the + rail (3V3)
l.resistor("R1", "10kΩ", "A:b16", "A:-18")    # from the same row to the - rail
l.wire("ESP32.35", "LDR1.1")
l.schematic.divider(35, top="LDR1", bottom="R1")

th = Circuit("A_thermistor", "Thermistor: 10 kΩ from 3V3 to pin 34, thermistor from pin 34 to GND",
             sketches=["A_Thermistor"])
gnd_a(th)
v33_a(th)
th.resistor("R1", "10kΩ", "A:a16", "A:+16")   # one leg straight into the + rail (3V3)
th.thermistor("TH1", "A:b16", "A:-18")        # from the same row to the - rail
th.wire("ESP32.34", "R1.1")
th.schematic.divider(34, top="R1", bottom="TH1")

j = Circuit("A_joystick", "Joystick: VRx 34, VRy 35, SW 14, + to 3V3 (not 5V!)",
            sketches=["L14_Joystick"])
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

# ---------------------------------------------------------------- sensor modules
h = Circuit("A_dht11", "DHT11: S on pin 4, + to 3V3, - to GND", sketches=["L11_ReadDHT"])
gnd_b(h)
v33_b(h)
dht_b(h)
h.schematic.module("U2", left=[("S", 4)], top=[("+", "3V3")], bottom=[("-", "GND")], title="DHT11")

g = Circuit("A_gy6500", "GY-6500: SDA 21, SCL 22, VCC to 3V3", sketches=["L19_Tilt"])
g.module("U1", "gy6500", "B:j20", rotate=180)   # VCC j20, GND j19, SCL j18, SDA j17, ... FSYNC j11
# four wires in a staircase, one row each, so they don't cross
g.wire("B:b1", "B:g20", via=["B:b20"])           # VCC <- 3V3
g.wire("B:c2", "B:g19", via=["B:c19"])           # GND
g.wire("B:d14", "B:f18", via=["B:d18"])          # SCL <- 22
g.wire("B:e11", "B:f17", via=["B:e17"])          # SDA <- 21
g.schematic.bus("I2C", {"SDA": 21, "SCL": 22}, ["U1"], power={"VCC": "3V3", "GND": "GND"})

# ---------------------------------------------------------------- outputs
ir = Circuit("A_ir_tx", "IR transmitter: S on pin 4, + to 3V3, - to GND", sketches=["A_IRSend"])
gnd_b(ir)
v33_b(ir)
ir.module("U1", "ir_tx", "B:f24")               # - f24, + f25, S f26; the LED points up the board
ir.wire("U1.-", "B:-")
ir.wire("U1.+", "B:+")
ir.wire("ESP32.4", "U1.S")
ir.schematic.module("U1", left=[("S", 4)], top=[("+", "3V3")], bottom=[("-", "GND")],
                    title="IR transmitter")

r = Circuit("A_relay", "Relay board: S on pin 32, + to VIN (5 V); it switches a red LED",
            sketches=["A_Relay"])
gnd_a(r)
v5_a(r)                                        # A's + rail is 5 V here!
r.module("K1", "relay", (33.5, 2.0), rotate=90)   # off the board on the right, on female-to-male wires
r.wire("K1.S", "A:i10", via=[(31.6, 2.0), (31.6, 14.5), (10.0, 14.5)])   # S <- D32
r.wire("K1.+", "A:+30")                        # + <- 5 V
r.wire("K1.-", "A:-29")                        # - <- GND
# the switch side: COM gets 5 V, NO feeds the LED (jumper wires screwed into the terminals)
r.wire("K1.COM", "A:+27", via=[(49.5, 4.0), (49.5, -2.0), (27.0, -2.0)])
r.wire("K1.NO", "A:a22", via=[(47.5, 2.0), (47.5, -2.9), (22.0, -2.9)])
r.resistor("R1", "220Ω", "A:c22", "A:c20")
r.led("D1", "red", a="A:a20", k="A:-18")
r.schematic.module("K1", left=[("S", 32)], top=[("+", "5V")], bottom=[("-", "GND")],
                   right=[("COM", "5V"), ("NO", "chain", ["R1", "D1"], "GND"), ("NC",)],
                   title="relay module")
