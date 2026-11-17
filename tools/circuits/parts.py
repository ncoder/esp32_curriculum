"""The parts in the kit: where their legs go on the breadboard, and how to draw them.

Every part has a reference (R1, D1, U2 ...) and a set of *legs*. Each leg sits in
a breadboard hole or, for parts that hang off the board, at a point. Legs map to
logical *pins*; several legs can share one pin when they are joined inside the
part (the ESP32's GND pins, a push button's leg pairs).
"""
import math

from .board import BOARD_Y0, ROW_Y, Hole, Point

# ---------------------------------------------------------------- colours
LED_COLORS = {
    "red": "#ef3b3b", "yellow": "#ffd43b", "green": "#37b24d", "blue": "#228be6",
    "white": "#f8f9fa", "orange": "#ff922b",
}
BAND = {0: "#111", 1: "#8b4a1c", 2: "#e03131", 3: "#f76707", 4: "#fcc419", 5: "#2f9e44",
        6: "#1c7ed6", 7: "#7048e8", 8: "#868e96", 9: "#ffffff"}
LEG = "#a5abb3"
PCB_BLUE = "#1f4e9c"


def parse_ohms(value):
    v = value.replace("Ω", "").replace("ohm", "").strip().lower()
    mult = 1
    if v.endswith("k"):
        mult, v = 1000, v[:-1]
    elif v.endswith("m"):
        mult, v = 1_000_000, v[:-1]
    return round(float(v) * mult)


def resistor_bands(value):
    ohms = parse_ohms(value)
    digits = str(ohms)
    if len(digits) < 2:
        return [BAND[0], BAND[int(digits)], BAND[0]]
    return [BAND[int(digits[0])], BAND[int(digits[1])], BAND[len(digits) - 2]]


def _xy(loc):
    return loc.xy


def _angle(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def _mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


# ================================================================ base class
class Part:
    kind = "part"
    symmetric = False       # True when swapping the two legs makes no difference (resistor)
    schematic_pins = None   # pins that matter electrically (default: all)

    def __init__(self, ref, label=""):
        self.ref = ref
        self.label = label
        self.legs = {}      # leg name -> Hole or Point
        self.leg_pin = {}   # leg name -> logical pin name

    def add_leg(self, leg, loc, pin=None):
        self.legs[leg] = loc
        self.leg_pin[leg] = pin if pin is not None else leg

    def pins(self):
        return sorted(set(self.leg_pin.values()))

    def legs_of(self, pin):
        return [leg for leg, p in self.leg_pin.items() if p == pin]

    def draw(self, svg):
        raise NotImplementedError

    def label_xy(self):
        pts = [_xy(l) for l in self.legs.values()]
        x = sum(p[0] for p in pts) / len(pts)
        y = min(p[1] for p in pts)
        return (x, y - 1.2)

    def draw_leg(self, svg, a, b, color=LEG, sw=0.16):
        svg.line(a[0], a[1], b[0], b[1], stroke=color, sw=sw)
        self.draw_foot(svg, a)

    @staticmethod
    def draw_foot(svg, p):
        svg.rect(p[0] - 0.17, p[1] - 0.17, 0.34, 0.34, fill="#6c737c", rx=0.05)


# ================================================================ the ESP32
# 38-pin ESP32-WROOM-32 DevKit, lying across the two boards with USB on the left.
# Top row (board A, row j), columns 1-19:
ESP32_TOP = ["5V", "CMD", "SD3", "SD2", "13", "GND", "12", "14", "27", "26",
             "25", "33", "32", "35", "34", "VN", "VP", "EN", "3V3"]
# Bottom row (board B, row a), columns 1-19:
ESP32_BOTTOM = ["CLK", "SD0", "SD1", "15", "2", "0", "4", "16", "17", "5",
                "18", "19", "GND", "21", "RX", "TX", "22", "23", "GND"]
ESP32_ALIASES = {"VIN": "5V", "VP": "36", "VN": "39", "RX": "3", "TX": "1"}
POWER_PINS = ("GND", "3V3", "5V")


def esp32_pin_name(label):
    """'26' -> 'GPIO26', 'GND' -> 'GND', 'VP' -> 'GPIO36'."""
    label = ESP32_ALIASES.get(label, label)
    return f"GPIO{label}" if label.isdigit() else label


class Esp32(Part):
    kind = "esp32"

    def __init__(self, ref="ESP32"):
        super().__init__(ref, "ESP32 DevKit")
        for i, name in enumerate(ESP32_TOP, 1):
            self.add_leg(f"T{i}", Hole("A", "j", i), esp32_pin_name(name))
        for i, name in enumerate(ESP32_BOTTOM, 1):
            self.add_leg(f"B{i}", Hole("B", "a", i), esp32_pin_name(name))

    def resolve_pin(self, text):
        """'26', 'GPIO26', 'GND', '3V3', '5V', 'VIN' -> logical pin name."""
        t = text.upper().replace("GPIO", "").replace("IO", "")
        t = {"VIN": "5V", "3.3V": "3V3"}.get(t, t)
        name = f"GPIO{t}" if t.isdigit() else t
        if name not in self.leg_pin.values():
            raise ValueError(f"the ESP32 has no pin {text!r}")
        return name

    def label_xy(self):
        return (13.0, 19.0)

    def draw(self, svg):
        ytop = BOARD_Y0["A"] + ROW_Y["j"]
        ybot = BOARD_Y0["B"] + ROW_Y["a"]
        y0, y1 = ytop - 0.75, ybot + 0.75
        # USB-C socket overhangs the left edge
        svg.rect(-1.9, (y0 + y1) / 2 - 1.15, 2.3, 2.3, fill="#c3c8ce", stroke="#7d848c", sw=0.08, rx=0.35)
        svg.rect(-1.75, (y0 + y1) / 2 - 0.45, 1.0, 0.9, fill="#5f666e", rx=0.3)
        # board
        svg.rect(-0.55, y0, 22.3, y1 - y0, fill="#20242a", stroke="#0b0d10", sw=0.1, rx=0.45)
        # header pins and their printed labels
        for i, name in enumerate(ESP32_TOP, 1):
            svg.rect(i - 0.38, ytop - 0.38, 0.76, 0.76, fill="#30353c")
            svg.circle(i, ytop, 0.2, fill="#d4af37")
            svg.text(i, ytop + 1.25, name, size=0.52, fill="#f1f3f5", rotate=-90, weight="bold")
        for i, name in enumerate(ESP32_BOTTOM, 1):
            svg.rect(i - 0.38, ybot - 0.38, 0.76, 0.76, fill="#30353c")
            svg.circle(i, ybot, 0.2, fill="#d4af37")
            svg.text(i, ybot - 1.25, name, size=0.52, fill="#f1f3f5", rotate=-90, weight="bold")
        ym = (y0 + y1) / 2
        # EN and BOOT buttons, USB chip, power LED
        for by, lbl in ((ym - 1.3, "EN"), (ym + 1.3, "BOOT")):
            svg.rect(1.0, by - 0.55, 1.1, 1.1, fill="#c3c8ce", rx=0.15)
            svg.circle(1.55, by, 0.33, fill="#495057")
            svg.text(2.75, by, lbl, size=0.42, fill="#ced4da", anchor="start")
        svg.rect(4.6, ym - 0.75, 1.5, 1.5, fill="#0b0d10", stroke="#495057", sw=0.05)
        svg.circle(7.0, ym + 1.5, 0.22, fill="#ff6b6b")
        # WROOM module: metal can + antenna
        svg.rect(8.2, ym - 2.15, 13.2, 4.3, fill="#1a1d21", rx=0.2)
        svg.rect(8.4, ym - 1.95, 9.6, 3.9, fill="#c9cdd2", stroke="#9aa1a9", sw=0.06, rx=0.15)
        svg.text(13.2, ym - 0.45, "ESP32", size=0.95, fill="#495057", weight="bold")
        svg.text(13.2, ym + 0.75, "WROOM-32", size=0.55, fill="#6c757d")
        zig = [(18.5, ym + 1.4)]
        for k in range(6):
            x = 18.75 + k * 0.42
            zig += [(x, ym + 1.4), (x, ym - 1.4)] if k % 2 == 0 else [(x, ym - 1.4), (x, ym + 1.4)]
        svg.poly(zig, closed=False, stroke="#d4af37", sw=0.14)


# ================================================================ two-leg parts
class TwoLeg(Part):
    def __init__(self, ref, label, a, b, pins=("1", "2")):
        super().__init__(ref, label)
        self.add_leg(pins[0], a)
        self.add_leg(pins[1], b)
        self.ends = pins

    def ab(self):
        return _xy(self.legs[self.ends[0]]), _xy(self.legs[self.ends[1]])

    def label_xy(self):
        a, b = self.ab()
        m = _mid(a, b)
        if abs(a[1] - b[1]) > abs(a[0] - b[0]):      # vertical part: label to the side
            return (m[0] + 1.1, m[1])
        return (m[0], m[1] - 1.05)


class Resistor(TwoLeg):
    kind = "resistor"
    symmetric = True

    def __init__(self, ref, value, a, b):
        super().__init__(ref, value, a, b)
        self.value = value

    def label_xy(self):
        a, b = self.ab()
        m = _mid(a, b)
        if abs(a[1] - b[1]) > abs(a[0] - b[0]):
            return (m[0] + 1.0, m[1])
        return (m[0], m[1] - 0.95)

    def draw(self, svg):
        a, b = self.ab()
        d = math.dist(a, b)
        body = min(2.3, max(1.2, d - 0.9))
        m = _mid(a, b)
        self.draw_leg(svg, a, m)
        self.draw_leg(svg, b, m)
        with svg.g(m, _angle(a, b)):
            svg.rect(-body / 2, -0.36, body, 0.72, fill="#e8d3a6", stroke="#b89b62", sw=0.06, rx=0.32)
            bands = resistor_bands(self.value) + ["#c9a227"]
            xs = [-body * 0.28, -body * 0.12, body * 0.04, body * 0.3]
            for x, c in zip(xs, bands):
                svg.rect(x - 0.08, -0.36, 0.16, 0.72, fill=c)


class Led(TwoLeg):
    kind = "led"

    def __init__(self, ref, color, a, k):
        super().__init__(ref, f"{color} LED", a, k, pins=("A", "K"))
        self.color = color

    def draw(self, svg):
        a, k = self.ab()
        m = _mid(a, k)
        ang = _angle(a, k)
        # the long (+) leg has a little kink so you can tell it apart
        with svg.g(a, ang):
            d = math.dist(a, k) / 2
            svg.poly([(0, 0), (d * 0.35, 0), (d * 0.45, -0.25), (d * 0.55, 0.25), (d * 0.65, 0), (d, 0)],
                     closed=False, stroke=LEG, sw=0.16)
        self.draw_foot(svg, a)
        self.draw_leg(svg, k, m)
        fill = LED_COLORS.get(self.color, self.color)
        with svg.g(m, ang):
            svg.circle(0, 0, 0.82, fill=fill, stroke="#00000055", sw=0.08, opacity=0.95)
            svg.line(0.62, -0.55, 0.62, 0.55, stroke="#00000066", sw=0.1)  # flat edge = short (-) leg
            svg.circle(-0.25, -0.25, 0.22, fill="#ffffffaa")


class Ldr(TwoLeg):
    kind = "ldr"
    symmetric = True

    def draw(self, svg):
        a, b = self.ab()
        m = _mid(a, b)
        self.draw_leg(svg, a, m)
        self.draw_leg(svg, b, m)
        with svg.g(m, _angle(a, b)):
            svg.circle(0, 0, 0.75, fill="#f4e3c1", stroke="#c9a46a", sw=0.07)
            svg.poly([(-0.45, -0.3), (-0.2, -0.3), (-0.2, 0.3), (0.05, 0.3), (0.05, -0.3), (0.3, -0.3), (0.3, 0.3)],
                     closed=False, stroke="#c0392b", sw=0.09)


class Tilt(TwoLeg):
    kind = "tilt"
    symmetric = True

    def draw(self, svg):
        a, b = self.ab()
        m = _mid(a, b)
        self.draw_leg(svg, a, m)
        self.draw_leg(svg, b, m)
        with svg.g(m, _angle(a, b) + 90):
            svg.rect(-0.55, -1.0, 1.1, 2.0, fill="#2b2f33", stroke="#000", sw=0.06, rx=0.45)
            svg.circle(0, 0.35, 0.28, fill="#adb5bd")


class Buzzer(TwoLeg):
    kind = "buzzer"

    def __init__(self, ref, plus, minus, active=True):
        super().__init__(ref, "active buzzer" if active else "passive buzzer", plus, minus, pins=("+", "-"))
        self.active = active

    def label_xy(self):
        a, b = self.ab()
        m = _mid(a, b)
        return (m[0], m[1] - 2.85)

    def draw(self, svg):
        a, b = self.ab()
        m = _mid(a, b)
        self.draw_foot(svg, a)
        self.draw_foot(svg, b)
        svg.circle(m[0], m[1], 2.25, fill="#1d1f22", stroke="#000", sw=0.08)
        if self.active:
            svg.circle(m[0], m[1], 1.45, fill="#f1f3f5")
            svg.circle(m[0], m[1], 0.3, fill="#1d1f22")
        else:
            svg.circle(m[0], m[1], 1.55, fill="#2b2f33", stroke="#3d4248", sw=0.06)
            svg.circle(m[0], m[1], 0.35, fill="#0b0d10")
        with svg.g(a, 0):
            svg.text(0, 0, "+", size=1.0, fill="#ffffff", weight="bold")


class Button(Part):
    """6 mm push button across the middle gap: legs at e/f of col and col+width."""
    kind = "button"

    def __init__(self, ref, top_left, width=2):
        super().__init__(ref, "push button")
        if top_left.row != "e":
            raise ValueError(f"{ref}: put a button across the middle gap, with its top legs in row e")
        b, c = top_left.board, top_left.col
        # Legs on the same side of the gap are joined inside: pressing joins left to right.
        self.add_leg("1a", Hole(b, "e", c), "1")
        self.add_leg("1b", Hole(b, "f", c), "1")
        self.add_leg("2a", Hole(b, "e", c + width), "2")
        self.add_leg("2b", Hole(b, "f", c + width), "2")
        self.w = width

    symmetric = True

    def label_xy(self):
        x, y = _xy(self.legs["1a"])
        return (x + self.w / 2, y - 1.2)

    def draw(self, svg):
        x0, y0 = _xy(self.legs["1a"])
        x1, y1 = _xy(self.legs["2b"])
        for leg in self.legs.values():
            self.draw_foot(svg, _xy(leg))
        svg.rect(x0 - 0.45, y0 - 0.1, x1 - x0 + 0.9, y1 - y0 + 0.2, fill="#2b2f33", stroke="#000", sw=0.06, rx=0.2)
        svg.circle((x0 + x1) / 2, (y0 + y1) / 2, min(x1 - x0, y1 - y0) * 0.36, fill="#495057", stroke="#111", sw=0.06)


class Pot(Part):
    """Potentiometer: three legs (left '1', middle 'W', right '2'), knob drawn above or below."""
    kind = "pot"

    def __init__(self, ref, holes, side="up"):
        super().__init__(ref, "10 kΩ potentiometer")
        for leg, h in zip(("1", "W", "2"), holes):
            self.add_leg(leg, h)
        self.side = side

    def label_xy(self):
        x, y = _xy(self.legs["W"])
        return (x + 2.4, y - 1.6 if self.side == "up" else y + 1.6)

    def draw(self, svg):
        pts = [_xy(self.legs[k]) for k in ("1", "W", "2")]
        for p in pts:
            self.draw_foot(svg, p)
        x, y = pts[1]
        span = max(abs(pts[2][0] - pts[0][0]), 2) + 1.2
        cy = y - 1.5 if self.side == "up" else y + 1.5
        svg.rect(x - span / 2, cy - 1.6, span, 3.2, fill="#1c5aa6", stroke="#0f3a70", sw=0.08, rx=0.3)
        svg.circle(x, cy, 1.25, fill="#e9ecef", stroke="#868e96", sw=0.08)
        svg.line(x, cy, x + 0.7, cy - 0.7, stroke="#343a40", sw=0.2)


class RgbLed(Part):
    """Common-cathode RGB LED: four legs in a line, in the order R, K (longest), G, B."""
    kind = "rgbled"

    def __init__(self, ref, holes):
        super().__init__(ref, "RGB LED")
        for leg, h in zip(("R", "K", "G", "B"), holes):
            self.add_leg(leg, h)

    def label_xy(self):
        pts = [_xy(l) for l in self.legs.values()]
        return (pts[0][0] - 1.6, (pts[0][1] + pts[-1][1]) / 2 - 1.5)

    def draw(self, svg):
        pts = [_xy(self.legs[k]) for k in ("R", "K", "G", "B")]
        cx = sum(p[0] for p in pts) / 4
        cy = sum(p[1] for p in pts) / 4
        horizontal = abs(pts[3][0] - pts[0][0]) >= abs(pts[3][1] - pts[0][1])
        bx, by = (cx, cy - 1.6) if horizontal else (cx - 1.6, cy)
        for p in pts:
            self.draw_leg(svg, p, (bx, by), sw=0.14)
        svg.circle(bx, by, 1.05, fill="#f8f9fa", stroke="#adb5bd", sw=0.08, opacity=0.95)
        for dx, c in ((-0.35, "#ef3b3b"), (0.0, "#37b24d"), (0.35, "#228be6")):
            svg.circle(bx + dx, by + 0.1, 0.22, fill=c, opacity=0.8)


# ================================================================ chips and displays
CHIPS = {
    # pin number -> pin name. Pins with the same name are joined inside the chip.
    "74HC595": {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4", 5: "Q5", 6: "Q6", 7: "Q7", 8: "GND",
                9: "Q7'", 10: "MR", 11: "CLOCK", 12: "LATCH", 13: "OE", 14: "DATA", 15: "Q0", 16: "VCC"},
    "L293D": {1: "EN1", 2: "IN1", 3: "OUT1", 4: "GND", 5: "GND", 6: "OUT2", 7: "IN2", 8: "VS",
              9: "EN2", 10: "IN3", 11: "OUT3", 12: "GND", 13: "GND", 14: "OUT4", 15: "IN4", 16: "VCC"},
}


class Dip(Part):
    """A 16-leg chip across the middle gap, notch to the left: pin 1 is bottom-left (row f)."""
    kind = "dip"

    def __init__(self, ref, chip, pin1):
        super().__init__(ref, chip)
        if pin1.row != "f":
            raise ValueError(f"{ref}: put pin 1 in row f, with the chip across the middle gap")
        self.chip = chip
        names = CHIPS[chip]
        n = len(names) // 2
        b, c = pin1.board, pin1.col
        for k in range(1, n + 1):
            self.add_leg(str(k), Hole(b, "f", c + k - 1), names[k])
            self.add_leg(str(2 * n + 1 - k), Hole(b, "e", c + k - 1), names[2 * n + 1 - k])
        self.n = n
        self.c = c
        self.b = b

    def label_xy(self):
        x, y = _xy(self.legs["1"])
        return (x - 1.6, y - 1.5)

    def draw(self, svg):
        x0, yf = _xy(self.legs["1"])
        _, ye = _xy(self.legs[str(2 * self.n)])
        for leg in self.legs.values():
            p = _xy(leg)
            svg.rect(p[0] - 0.22, p[1] - 0.3 if p[1] > ye else p[1] - 0.05, 0.44, 0.35, fill="#c0c4c9")
        w = self.n - 1 + 1.0
        svg.rect(x0 - 0.5, ye + 0.3, w, yf - ye - 0.6, fill="#25282c", stroke="#000", sw=0.06, rx=0.12)
        ym = (ye + yf) / 2
        svg.circle(x0 - 0.5, ym, 0.42, fill="#5c636a")   # the notch
        svg.circle(x0 + 0.05, yf - 0.75, 0.16, fill="#5c636a")
        svg.text(x0 + w / 2 - 0.3, ym, self.chip, size=0.75, fill="#e9ecef", weight="bold")


SEG7 = {
    1: {1: "e", 2: "d", 3: "COM", 4: "c", 5: "dp", 6: "b", 7: "a", 8: "COM", 9: "f", 10: "g"},
    4: {1: "e", 2: "d", 3: "dp", 4: "c", 5: "g", 6: "D4", 7: "b", 8: "D3", 9: "D2", 10: "f", 11: "a", 12: "D1"},
}


class SevenSeg(Part):
    """1- or 4-digit common-cathode display across the gap, decimal point at the bottom.
    The two rows of pins are 0.6" apart: pin 1 in row f, g, h or i puts the top pins
    in row b, c, d or e."""
    kind = "seg7"
    TOP_ROW = {"f": "b", "g": "c", "h": "d", "i": "e"}

    def __init__(self, ref, pin1, digits=1):
        super().__init__(ref, f"{digits}-digit display")
        if pin1.row not in self.TOP_ROW:
            raise ValueError(f"{ref}: put pin 1 in row f, g, h or i (the display straddles the gap)")
        names = SEG7[digits]
        n = len(names) // 2
        b, c = pin1.board, pin1.col
        top = self.TOP_ROW[pin1.row]
        for k in range(1, n + 1):
            self.add_leg(str(k), Hole(b, pin1.row, c + k - 1), names[k])
            self.add_leg(str(2 * n + 1 - k), Hole(b, top, c + k - 1), names[2 * n + 1 - k])
        self.n, self.digits = n, digits

    def label_xy(self):
        x, y = _xy(self.legs["1"])
        w = 5.0 if self.digits == 1 else 19.8
        return (x + (self.n - 1) / 2 - w / 2 - 1.3, y - 3.0)

    def draw(self, svg):
        x0, yb = _xy(self.legs["1"])
        _, yt = _xy(self.legs[str(2 * self.n)])
        cx = x0 + (self.n - 1) / 2
        cy = (yt + yb) / 2
        w, h = (5.0, 7.5) if self.digits == 1 else (19.8, 7.5)
        for leg in self.legs.values():
            self.draw_foot(svg, _xy(leg))
        svg.rect(cx - w / 2, cy - h / 2, w, h, fill="#2a2d31", stroke="#000", sw=0.08, rx=0.15)
        dw = 2.6
        starts = [cx - dw / 2 - 0.2] if self.digits == 1 else [cx - 7.6 + i * 4.6 for i in range(4)]
        for sx in starts:
            self._digit(svg, sx, cy, dw)

    @staticmethod
    def _digit(svg, x, cy, dw):
        seg = "#5b3a3a"
        t = 0.38
        top, mid, bot = cy - 2.6, cy, cy + 2.6
        for y in (top, mid, bot):
            svg.rect(x + 0.25, y - t / 2, dw - 0.5, t, fill=seg, rx=0.12)
        for xx in (x, x + dw - t):
            for y0 in (top, mid):
                svg.rect(xx, y0 + 0.25, t, 2.6 - 0.5, fill=seg, rx=0.12)
        svg.circle(x + dw + 0.45, bot, 0.26, fill=seg)


# ================================================================ modules
# Each module: its pins (in header order), size of the board around them, and a drawing.
# Pins are 1 pitch apart along local x, at y = 0; the board extends to negative y.
MODULES = {
    "oled":     dict(pins=["GND", "VCC", "SCL", "SDA"], w=10.6, h=10.6, title="OLED 0.96\""),
    "dht11":    dict(pins=["S", "+", "-"], w=6.0, h=8.6, title="DHT11"),
    "ir_rx":    dict(pins=["-", "+", "S"], w=5.6, h=6.0, title="IR receiver"),
    "gy6500":   dict(pins=["VCC", "GND", "SCL", "SDA", "EDA", "ECL", "AD0", "INT", "NCS", "FSYNC"],
                     w=10.6, h=6.4, title="GY-6500"),
    "hcsr04":   dict(pins=["VCC", "Trig", "Echo", "GND"], w=17.7, h=8.0, title="HC-SR04"),
    "pir":      dict(pins=["VCC", "OUT", "GND"], w=12.6, h=12.6, title="PIR HC-SR501"),
    "joystick": dict(pins=["GND", "+5V", "VRx", "VRy", "SW"], w=10.4, h=13.4, title="Joystick"),
    "rc522":    dict(pins=["SDA", "SCK", "MOSI", "MISO", "IRQ", "GND", "RST", "3.3V"], w=15.8, h=23.6,
                     title="RC522 RFID"),
    "keypad":   dict(pins=["R1", "R2", "R3", "R4", "C1", "C2", "C3", "C4"], w=20.0, h=23.0, title="4×4 keypad"),
    "uln2003":  dict(pins=["IN1", "IN2", "IN3", "IN4", "-", "+"], w=13.8, h=12.6, title="ULN2003"),
}


class Module(Part):
    """A board with a row of header pins. `at` is pin 1's hole (plugged in) or a Point
    (hanging off the breadboard, joined with jumper wires). `rotate` turns the module
    about pin 1: 0 = board above the pins, 180 = below (the pins then run right to left)."""
    kind = "module"

    def __init__(self, ref, kind, at, rotate=0, label=None):
        spec = MODULES[kind]
        super().__init__(ref, label or spec["title"])
        self.mkind = kind
        self.spec = spec
        self.rotate = rotate
        self.origin = _xy(at)
        r = math.radians(rotate)
        for i, name in enumerate(spec["pins"]):
            x = self.origin[0] + i * math.cos(r)
            y = self.origin[1] + i * math.sin(r)
            if isinstance(at, Hole):
                if rotate % 180:
                    raise ValueError(f"{ref}: a plugged-in module must lie along a row (rotate 0 or 180)")
                step = 1 if rotate == 0 else -1
                self.add_leg(name, Hole(at.board, at.row, at.col + i * step))
            else:
                self.add_leg(name, Point(round(x, 3), round(y, 3)))
        self.plugged = isinstance(at, Hole)

    def label_xy(self):
        return None   # modules print their own name

    def draw(self, svg):
        s = self.spec
        n = len(s["pins"])
        old_up = svg.upright
        svg.upright = -self.rotate if self.rotate % 360 == 180 else 0
        with svg.g(self.origin, self.rotate):
            px = (n - 1) / 2
            draw = getattr(self, f"_draw_{self.mkind}")
            draw(svg, px, s["w"], s["h"])
            # header pins and labels
            for i, name in enumerate(s["pins"]):
                svg.rect(i - 0.4, -0.4, 0.8, 0.8, fill="#1d1f22")
                svg.circle(i, 0, 0.2, fill="#d4af37")
                lbl_color = "#ffffff" if self.mkind not in ("keypad",) else "#343a40"
                svg.text(i, -1.05, name, size=0.45, fill=lbl_color, rotate=-90 if len(name) > 2 else 0,
                         weight="bold")
        svg.upright = old_up

    # --- individual module drawings (local frame: pins along x at y=0, body towards -y)
    def _board(self, svg, px, w, h, color=PCB_BLUE, below=0.7):
        svg.rect(px - w / 2, -h + below, w, h, fill=color, stroke="#00000066", sw=0.08, rx=0.4)

    def _title(self, svg, x, y, text, color="#ffffff", size=0.7):
        svg.text(x, y, text, size=size, fill=color, weight="bold")

    def _draw_oled(self, svg, px, w, h):
        self._board(svg, px, w, h, "#16376e")
        svg.rect(px - w / 2 + 0.6, -h + 1.4, w - 1.2, h - 4.2, fill="#0b0d10", rx=0.15)
        for k, ww in enumerate((5.5, 7.0, 4.0)):
            svg.rect(px - w / 2 + 1.3, -h + 2.4 + k * 1.3, ww, 0.5, fill="#7fd3ff", opacity=0.75)
        self._title(svg, px, -1.9, self.label, size=0.55)

    def _draw_dht11(self, svg, px, w, h):
        self._board(svg, px, w, h, "#1d1f22")
        svg.rect(px - 2.2, -h + 1.2, 4.4, 5.0, fill="#4dabf7", stroke="#1c7ed6", sw=0.08, rx=0.25)
        for k in range(4):
            svg.rect(px - 1.6, -h + 1.8 + k * 1.1, 3.2, 0.5, fill="#1c7ed6", rx=0.2)
        self._title(svg, px, -1.9, "DHT11", size=0.6)

    def _draw_ir_rx(self, svg, px, w, h):
        self._board(svg, px, w, h, "#1d1f22")
        svg.rect(px - 1.2, -h + 0.9, 2.4, 2.6, fill="#111", rx=0.3)
        svg.circle(px, -h + 2.0, 0.85, fill="#2b2f33", stroke="#555", sw=0.06)
        self._title(svg, px, -1.9, "IR", size=0.6)

    def _draw_gy6500(self, svg, px, w, h):
        self._board(svg, px, w, h, "#5f3dc4")
        svg.rect(px - 1.1, -h + 1.4, 2.2, 2.2, fill="#111", rx=0.1)
        svg.circle(px - 0.7, -h + 1.8, 0.12, fill="#666")
        self._title(svg, px + 3.0, -h + 2.5, "GY-6500", size=0.6)
        # tilt arrows
        svg.text(px - 3.6, -h + 2.5, "x→", size=0.55, fill="#e5dbff")

    def _draw_hcsr04(self, svg, px, w, h):
        self._board(svg, px, w, h, PCB_BLUE)
        for dx, t in ((-4.6, "T"), (4.6, "R")):
            svg.circle(px + dx, -h / 2 + 0.3, 3.1, fill="#c9cdd2", stroke="#868e96", sw=0.1)
            svg.circle(px + dx, -h / 2 + 0.3, 2.3, fill="#495057")
            svg.circle(px + dx, -h / 2 + 0.3, 2.3, fill="none", stroke="#adb5bd", sw=0.05, dash=(0.15, 0.15))
            svg.text(px + dx, -h / 2 + 0.3, t, size=0.9, fill="#e9ecef", weight="bold")
        self._title(svg, px, -h / 2 + 0.3, "HC-SR04", size=0.5)

    def _draw_pir(self, svg, px, w, h):
        svg.circle(px, -h / 2 + 0.8, w / 2, fill="#2f9e44", stroke="#1b5e20", sw=0.08)
        svg.circle(px, -h / 2 + 0.8, w / 2 - 1.6, fill="#f8f9fa", stroke="#ced4da", sw=0.08)
        for k in range(-2, 3):
            svg.line(px + k * 1.2, -h / 2 + 0.8 - 3.6, px + k * 1.2, -h / 2 + 0.8 + 3.6, stroke="#dee2e6", sw=0.06)
        svg.text(px, -h + 1.15, "PIR", size=0.55, fill="#ffffff", weight="bold")

    def _draw_joystick(self, svg, px, w, h):
        self._board(svg, px, w, h, "#1d1f22")
        svg.circle(px, -h / 2 + 0.2, 4.0, fill="#343a40", stroke="#111", sw=0.08)
        svg.circle(px, -h / 2 + 0.2, 2.4, fill="#212529", stroke="#495057", sw=0.15)
        svg.text(px, -h / 2 + 0.2, "↕↔", size=0.7, fill="#adb5bd")

    def _draw_rc522(self, svg, px, w, h):
        self._board(svg, px, w, h, PCB_BLUE)
        for k in range(4):
            inset = 1.2 + k * 0.55
            svg.rect(px - w / 2 + inset, -h + 0.7 + inset, w - 2 * inset, h - 6.5 - 2 * inset,
                     stroke="#d4af37", sw=0.12, rx=0.6)
        svg.rect(px - 1.4, -4.7, 2.8, 2.8, fill="#111")
        self._title(svg, px, -h / 2 - 1.5, "RFID-RC522", size=0.7)

    def _draw_keypad(self, svg, px, w, h):
        # ribbon + connector (the header pins drawn by draw()) and the membrane above it
        svg.rect(px - 4.4, -0.75, 8.8, 1.5, fill="#212529", rx=0.2)
        svg.rect(px - 3.6, -7.0, 7.2, 6.4, fill="#d0d4d9", stroke="#adb5bd", sw=0.06)
        top = -7.0 - 22.0
        svg.rect(px - w / 2, top, w, 22.0, fill="#1d1f22", rx=0.5)
        keys = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"]
        for i, k in enumerate(keys):
            r, c = divmod(i, 4)
            kx = px - w / 2 + 1.6 + c * 4.5
            ky = top + 1.5 + r * 5.0
            fill = "#e03131" if c == 3 else "#f1f3f5"
            svg.rect(kx, ky, 3.6, 4.0, fill=fill, rx=0.4)
            svg.text(kx + 1.8, ky + 2.0, k, size=1.3, fill="#212529", weight="bold")

    def _draw_uln2003(self, svg, px, w, h):
        self._board(svg, px + 1.5, w, h, "#2f9e44")
        svg.rect(px - 2.0, -9.0, 6.0, 2.2, fill="#111", rx=0.1)   # ULN2003 chip
        svg.text(px + 1.0, -7.9, "ULN2003", size=0.55, fill="#dee2e6")
        for k in range(4):
            svg.circle(px - 1.5 + k * 1.6, -5.0, 0.45, fill="#ff6b6b", stroke="#c92a2a", sw=0.05)
        # white socket for the stepper's plug, on the far side
        svg.rect(px + 4.2, -12.2, 4.2, 1.7, fill="#f8f9fa", stroke="#adb5bd", sw=0.06)
        # 28BYJ-48 stepper motor and its cable
        svg.path([("M", px + 6.3, -12.2), ("Q", px + 6.3, -15.0, px + 2.0, -16.5)], stroke="#ffd43b", sw=0.55)
        svg.circle(px - 2.0, -19.5, 5.6, fill="#adb5bd", stroke="#495057", sw=0.1)
        svg.rect(px - 7.4, -20.5, 10.8, 2.0, fill="#adb5bd")
        svg.circle(px - 2.0, -19.5, 4.4, fill="#ced4da")
        svg.circle(px - 2.0, -21.3, 0.9, fill="#868e96")
        svg.circle(px - 2.0, -21.3, 0.35, fill="#f8f9fa")
        svg.text(px - 2.0, -17.6, "stepper", size=0.65, fill="#343a40", weight="bold")


class Leaded(Part):
    """A part that sits off the board with flexible wire leads going into holes:
    the servo (brown/red/orange wires) and the DC motor."""
    kind = "leaded"

    LEADS = {
        "servo": [("GND", "#7a4b23"), ("+5V", "#e03131"), ("SIG", "#f59f00")],
        "motor": [("1", "#e03131"), ("2", "#1d1f22")],
    }

    def __init__(self, ref, kind, body, holes, rotate=0):
        super().__init__(ref, {"servo": "SG90 servo", "motor": "DC motor"}[kind])
        self.lkind = kind
        self.kind = kind          # "servo" or "motor"
        self.body = body
        self.rotate = rotate
        for (name, _), h in zip(self.LEADS[kind], holes):
            self.add_leg(name, h)
        self.symmetric = kind == "motor"

    def label_xy(self):
        return None

    def draw(self, svg):
        bx, by = self.body.xy
        exits = []
        with svg.g((bx, by), self.rotate):
            if self.lkind == "servo":
                svg.rect(-4.6, -2.3, 9.2, 4.6, fill="#1c7ed6", stroke="#1864ab", sw=0.1, rx=0.3)
                svg.rect(-6.2, -0.6, 12.4, 1.2, fill="#1c7ed6", stroke="#1864ab", sw=0.08, rx=0.3)
                svg.circle(-2.4, 0, 1.6, fill="#ffffff", stroke="#adb5bd", sw=0.08)
                svg.path([("M", -2.4, -0.5), ("L", -2.4 - 5.5, -0.25), ("L", -2.4 - 5.5, 0.25), ("L", -2.4, 0.5), ("Z",)],
                         fill="#ffffff", stroke="#adb5bd", sw=0.06)
                svg.text(1.8, 0, "SG90", size=0.8, fill="#e7f5ff", weight="bold")
                local_exit = [(4.6, -0.5), (4.6, 0), (4.6, 0.5)]
            else:
                svg.rect(-3.2, -2.0, 6.4, 4.0, fill="#adb5bd", stroke="#495057", sw=0.1, rx=0.6)
                svg.rect(-4.2, -0.25, 1.0, 0.5, fill="#495057")
                svg.ellipse(-4.6, 0, 0.8, 3.6, fill="#ffffff", stroke="#868e96", sw=0.08)
                svg.text(0.2, 0, "M", size=1.3, fill="#495057", weight="bold")
                local_exit = [(3.2, -0.6), (3.2, 0.6)]
            r = math.radians(self.rotate)
            for lx, ly in local_exit:
                exits.append((bx + lx * math.cos(r) - ly * math.sin(r), by + lx * math.sin(r) + ly * math.cos(r)))
        for (name, color), e in zip(self.LEADS[self.lkind], exits):
            h = _xy(self.legs[name])
            mx = (e[0] + h[0]) / 2
            svg.path([("M", *e), ("C", mx, e[1], mx, h[1], *h)], stroke="#00000055", sw=0.42, cap="round")
            svg.path([("M", *e), ("C", mx, e[1], mx, h[1], *h)], stroke=color, sw=0.3, cap="round")
            self.draw_foot(svg, h)


class PowerModule(Part):
    """MB102 breadboard power supply plugged into the right-hand end of a board:
    its pins sit in both rail pairs at column `col`, the rest hangs off the end."""
    kind = "power"

    def __init__(self, ref, board="B", col=29):
        super().__init__(ref, "power supply module")
        for row, pin in (("tp", "+"), ("tn", "-"), ("bn", "-"), ("bp", "+")):
            self.add_leg(row, Hole(board, row, col), pin)
        self.board, self.col = board, col

    def label_xy(self):
        return None

    def draw(self, svg):
        y0 = BOARD_Y0[self.board]
        x = self.col - 0.9
        svg.rect(x, y0 + 0.2, 12.5, 18.6, fill="#2b2f33", stroke="#000", sw=0.1, rx=0.5)
        for leg in self.legs.values():
            p = _xy(leg)
            svg.rect(p[0] - 0.35, p[1] - 0.35, 0.7, 0.7, fill="#d4af37")
        # barrel jack, USB, switch, jumpers
        svg.rect(x + 8.0, y0 + 6.0, 5.0, 4.0, fill="#111", stroke="#555", sw=0.08, rx=0.3)
        svg.circle(x + 12.0, y0 + 8.0, 1.0, fill="#555")
        svg.rect(x + 9.4, y0 + 11.6, 3.4, 2.4, fill="#c3c8ce", rx=0.2)
        svg.rect(x + 4.6, y0 + 2.2, 2.4, 1.6, fill="#ffffff", stroke="#868e96", sw=0.06, rx=0.2)
        for yy in (y0 + 4.6, y0 + 14.4):
            svg.rect(x + 2.2, yy - 0.6, 2.6, 1.2, fill="#fcc419", rx=0.2)
            svg.text(x + 3.5, yy + 1.2, "5V", size=0.55, fill="#ffffff", weight="bold")
        svg.text(x + 5.0, y0 + 9.0, "POWER", size=0.8, fill="#e9ecef", weight="bold", rotate=-90)
        # 9 V battery clip lead
        svg.path([("M", x + 13.0, y0 + 8.0), ("Q", x + 16.5, y0 + 8.0, x + 16.5, y0 + 11.5)],
                 stroke="#e03131", sw=0.35)
        svg.rect(x + 14.5, y0 + 11.5, 4.0, 6.5, fill="#1d1f22", stroke="#000", sw=0.08, rx=0.3)
        svg.text(x + 16.5, y0 + 14.8, "9V", size=1.0, fill="#ffd43b", weight="bold")
