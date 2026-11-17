"""Standard builds that come back lesson after lesson, always in the same place.

Keeping a part in the same holes from lesson to lesson means the pictures match
what students already have on their boards.
"""


def gnd_a(c):
    """ESP32 GND (top row) -> board A's - rail."""
    c.wire("ESP32.GND", "A:-", tag="gnd_a")


def gnd_b(c):
    """ESP32 GND (bottom row) -> board B's - rail."""
    c.wire("B:e13", "B:-", tag="gnd_b")


def v33_a(c):
    """ESP32 3V3 -> board A's + rail."""
    c.wire("A:f19", "A:+20", bend=-0.12, tag="v33_a")


def traffic_leds(c, schematic=True):
    """Lesson 2's LEDs: red on 25, yellow on 26, green on 27, short legs in A's - rail.
    The LEDs are 2 columns apart (too fat to sit side by side), so the outer
    resistors lean across from their pin's column."""
    for n, pin_col, led_col, color in ((1, 11, 12, "red"), (2, 10, 10, "yellow"), (3, 9, 8, "green")):
        c.resistor(f"R{n}", "220Ω", f"A:f{pin_col}", f"A:e{led_col}")
        c.led(f"D{n}", color, a=f"A:a{led_col}", k=f"A:-{led_col}")
    if schematic:
        for gpio, n in ((25, 1), (26, 2), (27, 3)):
            c.schematic.led(gpio, f"R{n}", f"D{n}")


def buzzer33(c, ref="BZ1", active=False, schematic=True):
    """Buzzer across board A's gap: + leg in pin 33's row, - leg wired to A's - rail."""
    c.buzzer(ref, plus="A:f12", minus="A:e12", active=active)
    c.wire(f"{ref}.-", "A:-")
    if schematic:
        c.schematic.chain(33, [ref])


def button(c, ref, gpio, top_left, to=None, rail=None, schematic=True, **wire):
    """Push button across a gap. One leg wired to the ESP32 pin, the diagonally
    opposite leg to a - rail. `to` picks the hole for the ESP32 wire's far end."""
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


def v5_a(c):
    """ESP32 5V (next to the USB socket) -> board A's + rail. The + rail is then 5 V!"""
    c.wire("A:f1", "A:+2", tag="v5_a")


def v5_b(c):
    """ESP32 5V -> board B's + rail, round the USB end of the ESP32."""
    c.wire("A:i1", "B:+2", via=[(-2.6, 14.0), (-2.6, 37.0)], tag="v5_b")


def buzzer_side(c, ref="BZ1", active=False, schematic=True):
    """Buzzer on the right of board A, when pin 33's own row is too crowded:
    a jumper from pin 33, + leg below the gap, - leg above it, wired to A's - rail."""
    c.buzzer(ref, plus="A:f27", minus="A:e27", active=active)
    c.wire("A:h12", "A:h27", bend=0, tag=ref)
    c.wire(f"{ref}.-", "A:-")
    if schematic:
        c.schematic.chain(33, [ref])


def led_a(c, rref, dref, color, pin_col, led_col, schematic_gpio=None):
    """LED on board A like Lesson 1: resistor across the gap from the pin's row,
    short leg straight into A's - rail."""
    c.resistor(rref, "220Ω", f"A:f{pin_col}", f"A:e{led_col}")
    c.led(dref, color, a=f"A:a{led_col}", k=f"A:-{led_col}")
    if schematic_gpio is not None:
        c.schematic.led(schematic_gpio, rref, dref)


def led_b(c, rref, dref, color, col, schematic_gpio=None):
    """LED on board B: resistor across B's gap from the pin's row, LED from row j
    with its short leg in B's - rail."""
    c.resistor(rref, "220Ω", f"B:e{col}", f"B:f{col}")
    c.led(dref, color, a=f"B:j{col}", k=f"B:-{col}")
    if schematic_gpio is not None:
        c.schematic.led(schematic_gpio, rref, dref)


def oled_b(c, ref="U1"):
    """OLED plugged into board B right of the ESP32, screen hanging down over the board.
    SDA <- 21, SCL <- 22, GND <- GND, VCC <- 3V3 (a jumper over the ESP32's antenna end)."""
    c.module(ref, "oled", "B:e27", rotate=180)       # GND e27, VCC e26, SCL e25, SDA e24
    c.wire("B:b14", "B:b24", bend=0)                 # SDA <- 21
    c.wire("B:c17", "B:c25", bend=0)                 # SCL <- 22
    c.wire("B:d19", "B:d27", bend=0)                 # GND
    c.wire("A:g19", "B:a26", bend=-0.1)              # VCC <- 3V3


def dht_b(c, ref="U2"):
    """DHT11 module plugged into board B's lower half, below pin 4."""
    c.module(ref, "dht11", "B:j8", rotate=180)       # S j8, + j7, - j6
    c.wire("B:e7", "B:f8")                           # S <- 4
    c.wire("B:e13", "B:g6", bend=-0.1)               # - <- GND
    c.wire("A:h19", "B:h7", via=[(19.6, 13.0), (19.6, 28.9), (7.0, 28.9)])   # + <- 3V3
