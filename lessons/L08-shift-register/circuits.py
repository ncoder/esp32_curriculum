"""Lesson 8 circuit: 74HC595 on 23/19/18 driving 8 LEDs, knob on 34."""
from circuits import Circuit
from circuits.kit import gnd_a, gnd_b, pot_a, v33_a, v33_b

c = Circuit("L08_shift", "74HC595: DATA 23, LATCH 19, CLOCK 18; 8 LEDs; knob on 34",
            sketches=["L08_OneByOne", "L08_Binary", "L08_LightShow"])
c.chip("U1", "74HC595", "B:f21")   # notch left: pins 1-8 along row f, 16-9 along row e
# ESP32 -> chip, a staircase of wires along rows b, c, d
c.wire("B:b9", "B:b26", bend=0)    # CLOCK (pin 11) <- 18
c.wire("B:c10", "B:c25", bend=0)   # LATCH (pin 12) <- 19
c.wire("B:d15", "B:d23", bend=0)   # DATA  (pin 14) <- 23
# chip power: the rails along the top of board B, joined to the bottom rails at the right
c.wire("B:a21", "B:tp22")          # VCC (16)
c.wire("B:a27", "B:tp27")          # MR (10) high = don't clear
c.wire("B:a24", "B:tn24")          # OE (13) low = outputs on
c.wire("B:j28", "B:-28")           # GND (8)
c.wire("B:bp30", "B:tp30", bend=0)
c.wire("B:bn29", "B:tn29", bend=0)
gnd_b(c)
v33_b(c)
# 8 LEDs on the left of board B: Q7 (128) on the left ... Q0 (1) on the right.
# Short leg -> 220 Ω -> - rail; long leg -> a chip output.
outputs = [(27, 2.6), (26, 2.2), (25, 1.8), (24, 1.4), (23, 1.0), (22, 0.7), (21, 0.4)]  # Q7..Q1
for k in range(1, 9):
    a, kk = 2 * k + 3, 2 * k + 4
    c.led(f"D{k}", "red", a=f"B:h{a}", k=f"B:h{kk}")
    c.resistor(f"R{k}", "220Ω", f"B:j{kk}", f"B:-{kk}")
    if k <= 7:
        q, bulge = outputs[k - 1]
        c.wire(f"B:f{a}", f"B:g{q}", bulge=bulge)
c.wire("B:f19", "B:a22", bulge=1.0)   # D8 -> Q0 (pin 15, top row)
# knob on board A
gnd_a(c)
v33_a(c)
pot_a(c, schematic=False)

leds = [("Q0", "chain", ["D8", "R8"], "GND")] + \
       [(f"Q{q}", "chain", [f"D{8 - q}", f"R{8 - q}"], "GND") for q in range(1, 8)]
c.schematic.module("U1", left=[("DATA", 23), ("LATCH", 19), ("CLOCK", 18)],
                   top=[("VCC", "3V3"), ("MR", "3V3")], bottom=[("OE", "GND"), ("GND", "GND")],
                   right=leds, title="74HC595",
                   numbers={"DATA": 14, "LATCH": 12, "CLOCK": 11, "VCC": 16, "MR": 10, "OE": 13, "GND": 8,
                            "Q0": 15, **{f"Q{q}": q for q in range(1, 8)}},
                   note="R1–R8: 220 Ω")
c.schematic.pot(34, "RV1")
