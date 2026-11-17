"""Lesson 8 circuit: 74HC595 on 23/19/18 driving 8 LEDs, knob on 34."""
from circuits import Circuit
from circuits.kit import gnd_b

c = Circuit("L08_shift", "74HC595: DATA 23, LATCH 19, CLOCK 18; 8 LEDs; knob on 34",
            sketches=["L08_OneByOne", "L08_Binary", "L08_LightShow"])
c.chip("U1", "74HC595", "B:f22")   # notch left: pins 1-8 along row f, 16-9 along row e
# ESP32 -> chip, a staircase of wires along rows b, c, d
c.wire("B:b11", "B:b27", bend=0)   # CLOCK (pin 11) <- 18
c.wire("B:c12", "B:c26", bend=0)   # LATCH (pin 12) <- 19
c.wire("B:d18", "B:d24", bend=0)   # DATA  (pin 14) <- 23
# chip power: + and - rails at the top of board B (free right of the ESP32)
c.wire("B:a22", "B:tp23")          # VCC (16)
c.wire("B:a28", "B:tp28")          # MR (10) high = don't clear
c.wire("B:a25", "B:tn26")          # OE (13) low = outputs on
c.wire("B:j29", "B:-29")           # GND (8)
c.wire("B:e19", "B:tn22")          # ESP32 GND -> top - rail
c.wire("B:tn30", "B:-30", bend=0)  # join the two - rails
# 8 LEDs on the left of board B: Q7 (128) on the left ... Q0 (1) on the right.
# Short leg -> 220 Ω -> - rail; long leg -> a chip output.
outputs = [(28, 3.2), (27, 2.8), (26, 2.4), (25, 2.0), (24, 1.6), (23, 1.2), (22, 0.8)]  # Q7..Q1 columns
for k in range(1, 9):
    a, kk = 2 * k - 1, 2 * k
    c.led(f"D{k}", "red", a=f"B:h{a}", k=f"B:h{kk}")
    c.resistor(f"R{k}", "220Ω", f"B:j{kk}", f"B:-{kk}")
    if k <= 7:
        col, bulge = outputs[k - 1]
        c.wire(f"B:f{a}", f"B:g{col}", bulge=bulge)
c.wire("B:f15", "B:a23", bulge=1.5)   # D8 -> Q0 (pin 15, top row)
# knob on board A, powered straight from the 3V3 pin's row
c.pot("RV1", "A:g20", "A:g21", "A:g22", side="up")
c.wire("A:h19", "A:h20", bend=0)    # 3V3 -> knob left
c.wire("A:i15", "A:i21", bend=0)    # 34 <- knob middle
c.wire("A:j22", "B:tn24")           # knob right -> GND
c.wire("A:j20", "B:tp22")           # 3V3 -> top + rail of board B

leds = [("Q0", "chain", ["D8", "R8"], "GND")] + \
       [(f"Q{q}", "chain", [f"D{8 - q}", f"R{8 - q}"], "GND") for q in range(1, 8)]
c.schematic.module("U1", left=[("DATA", 23), ("LATCH", 19), ("CLOCK", 18)],
                   top=[("VCC", "3V3"), ("MR", "3V3")], bottom=[("OE", "GND"), ("GND", "GND")],
                   right=leds, title="74HC595",
                   numbers={"DATA": 14, "LATCH": 12, "CLOCK": 11, "VCC": 16, "MR": 10, "OE": 13, "GND": 8,
                            "Q0": 15, **{f"Q{q}": q for q in range(1, 8)}},
                   note="R1–R8: 220 Ω")
c.schematic.pot(34, "RV1")
