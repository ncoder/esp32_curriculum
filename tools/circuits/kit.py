"""Standard builds that come back lesson after lesson, always in the same place.

Keeping a part in the same holes from lesson to lesson means the pictures match
what students already have on their boards.

Where the ESP32 DevKit V1's pins are (USB on the left):
  board A, row j, columns 1-15:  VIN GND D13 D12 D14 D27 D26 D25 D33 D32 D35 D34 VN VP EN
  board B, row a, columns 1-15:  3V3 GND D15 D2 D4 RX2 TX2 D5 D18 D19 D21 RX0 TX0 D22 D23
"""

# Column of each ESP32 pin, on its own board (A: top row, B: bottom row)
COL = {
    "VIN": ("A", 1), "GND_A": ("A", 2), 13: ("A", 3), 12: ("A", 4), 14: ("A", 5), 27: ("A", 6),
    26: ("A", 7), 25: ("A", 8), 33: ("A", 9), 32: ("A", 10), 35: ("A", 11), 34: ("A", 12),
    "3V3": ("B", 1), "GND_B": ("B", 2), 15: ("B", 3), 2: ("B", 4), 4: ("B", 5), 16: ("B", 6),
    17: ("B", 7), 5: ("B", 8), 18: ("B", 9), 19: ("B", 10), 21: ("B", 11), 22: ("B", 14), 23: ("B", 15),
}


def col(gpio):
    return COL[gpio][1]


def gnd_a(c):
    """ESP32 GND (top row) -> board A's - rail."""
    c.wire("A:f2", "A:-2", tag="gnd_a")


def gnd_b(c):
    """ESP32 GND (bottom row) -> board B's - rail."""
    c.wire("B:e2", "B:-3", tag="gnd_b")


def v33_b(c):
    """ESP32 3V3 (bottom row, next to the USB socket) -> board B's + rail."""
    c.wire("B:d1", "B:+2", tag="v33_b")


def v33_a(c):
    """ESP32 3V3 -> board A's + rail: the 3V3 pin is on the bottom row, so this wire
    goes round the USB end of the ESP32."""
    c.wire("B:c1", "A:+2", via=[(-3.4, 25.0), (-3.4, 0.2), (2.0, 0.2)], tag="v33_a")


def v5_a(c):
    """ESP32 VIN (5 V from USB, top row next to the USB socket) -> board A's + rail.
    The + rail is then 5 V!"""
    c.wire("A:f1", "A:+2", tag="v5_a")


def v5_b(c):
    """ESP32 VIN -> board B's + rail, round the USB end of the ESP32."""
    c.wire("A:i1", "B:+2", via=[(-2.7, 14.0), (-2.7, 37.8), (2.0, 37.8)], tag="v5_b")


def traffic_leds(c, schematic=True):
    """Lesson 2's LEDs: red on 25, yellow on 26, green on 27, short legs in A's - rail.
    The LEDs sit 2 columns apart (they are too fat to sit side by side), so their
    resistors lean across from the pin's column."""
    for n, gpio, led_col, color in ((1, 25, 10, "red"), (2, 26, 8, "yellow"), (3, 27, 6, "green")):
        c.resistor(f"R{n}", "220Ω", f"A:f{col(gpio)}", f"A:e{led_col}")
        c.led(f"D{n}", color, a=f"A:a{led_col}", k=f"A:-{led_col}")
    if schematic:
        for gpio, n in ((25, 1), (26, 2), (27, 3)):
            c.schematic.led(gpio, f"R{n}", f"D{n}")


def buzzer33(c, ref="BZ1", active=False, schematic=True):
    """Buzzer across board A's gap: + leg in pin 33's row, - leg wired to A's - rail."""
    c.buzzer(ref, plus="A:f9", minus="A:e9", active=active)
    c.wire(f"{ref}.-", "A:-")
    if schematic:
        c.schematic.chain(33, [ref])


def buzzer_side(c, ref="BZ1", active=False, schematic=True):
    """Buzzer on the right of board A, when pin 33's own row is crowded: a jumper
    from pin 33 along row h, + leg below the gap, - leg above it, wired to A's - rail."""
    c.buzzer(ref, plus="A:f27", minus="A:e27", active=active)
    c.wire("A:h9", "A:h27", bend=0, tag=ref)
    c.wire(f"{ref}.-", "A:-")
    if schematic:
        c.schematic.chain(33, [ref])


def button(c, ref, gpio, top_left, to=None, rail=None, schematic=True, **wire):
    """Push button across a gap. One leg wired to the ESP32 pin, the diagonally
    opposite leg to a - rail. `to` gives the two holes of the ESP32 wire."""
    sw = c.button(ref, top_left)
    board = top_left[0]
    if to:
        c.wire(to[0], to[1], tag=ref, **wire)
    else:
        c.wire(f"ESP32.{gpio}", f"{ref}.1", **wire)
    c.wire(f"{ref}.2", rail or f"{board}:-")
    if schematic:
        c.schematic.chain(gpio, [ref])
    return sw


def led_a(c, rref, dref, color, gpio, led_col, schematic=True):
    """LED on board A like Lesson 1: resistor across the gap from the pin's row,
    short leg straight into A's - rail."""
    c.resistor(rref, "220Ω", f"A:f{col(gpio)}", f"A:e{led_col}")
    c.led(dref, color, a=f"A:a{led_col}", k=f"A:-{led_col}")
    if schematic:
        c.schematic.led(gpio, rref, dref)


def led_b(c, rref, dref, color, gpio, led_col=None, schematic=True):
    """LED on board B: resistor across B's gap from the pin's row, LED from row j
    with its short leg in B's - rail."""
    led_col = led_col or col(gpio)
    c.resistor(rref, "220Ω", f"B:e{col(gpio)}", f"B:f{led_col}")
    c.led(dref, color, a=f"B:j{led_col}", k=f"B:-{led_col}")
    if schematic:
        c.schematic.led(gpio, rref, dref)


def pot_a(c, ref="RV1", gpio=34, left="+", right="-", schematic=True):
    """Knob on board A's right, legs in row e, knob over the gap. Left/right legs go to
    A's + and - rails (swap them with left="-", right="+")."""
    c.pot(ref, "A:e22", "A:e23", "A:e24", side="down")
    c.wire(f"{ref}.1", "A:+22" if left == "+" else "A:-22")
    c.wire(f"{ref}.2", "A:+24" if right == "+" else "A:-24")
    c.wire(f"ESP32.{gpio}", f"{ref}.W")
    if schematic:
        ends = ("3V3", "GND") if left == "+" else ("GND", "3V3")
        c.schematic.pot(gpio, ref, ends=ends)


def oled_b(c, ref="U1"):
    """OLED plugged into board B's row a, right of the ESP32, the screen standing up over
    the boards' join. Four straight wires along rows b-e, one per pin."""
    c.module(ref, "oled", "B:a24")                 # GND a24, VCC a25, SCL a26, SDA a27
    c.wire("B:b1", "B:b25", bend=0)                # VCC <- 3V3
    c.wire("B:c2", "B:c24", bend=0)                # GND
    c.wire("B:d11", "B:d27", bend=0)               # SDA <- 21
    c.wire("B:e14", "B:e26", bend=0)               # SCL <- 22


def dht_b(c, ref="U2"):
    """DHT11 module hanging below board B on female-to-male wires:
    S -> pin 4, + -> B's + rail (3V3), - -> B's - rail."""
    c.module(ref, "dht11", (7, 41.5), rotate=180)   # S 7, + 6, - 5
    c.wire(f"{ref}.-", "B:-5")
    c.wire(f"{ref}.+", "B:+6")
    c.wire(f"{ref}.S", "B:e5", bulge=-1.2)
