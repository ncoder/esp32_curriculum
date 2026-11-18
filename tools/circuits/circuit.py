"""Describe a lesson's circuit once; draw it as a breadboard picture and a schematic.

    from circuits import Circuit

    c = Circuit("L01_blink", "Lesson 1: one LED on pin 26", sketches=["L01_Blink"])
    c.resistor("R1", "220Ω", "A:f10", "A:e10")
    c.led("D1", "red", a="A:a10", k="A:-10")
    c.wire("ESP32.GND", "A:-")
    c.schematic.led(26, "R1", "D1")

Wire ends can be a hole ("A:c12"), a rail ("A:-": the nearest free hole on it),
or a part's pin ("ESP32.26", "R1.2", "OLED.SDA"): the nearest free hole in the
same breadboard strip, or the pin itself if the part hangs off the board.
"""
import copy
import math

from . import board as B
from .board import Hole, Point, RailRef, parse_hole
from .parts import (Button, Buzzer, Diode, Dip, Esp32, Led, Leaded, Ldr, Module, Pot, PowerModule,
                    Resistor, RgbLed, SevenSeg, Thermistor, Tilt, Transistor)
from .svg import Svg

WIRE_COLORS = {"gnd": "#2b2f33", "3v3": "#f76707", "5v": "#e03131"}
SIGNAL_COLORS = ["#fab005", "#37b24d", "#228be6", "#ae3ec9", "#15aabf", "#f06595",
                 "#ffffff", "#82c91e", "#7950f2", "#a0522d", "#868e96", "#ff8787"]


class CircuitError(Exception):
    pass


class Wire:
    def __init__(self, a, b, color=None, via=(), bend=None, tags=(), bulge=None):
        self.a, self.b = a, b
        self.bulge = bulge
        self.color = color
        self.via = list(via)
        self.bend = bend
        self.tags = set(tags)


class Circuit:
    registry = []

    def __init__(self, name, title, sketches=()):
        self.name = name
        self.title = title
        self.sketches = list(sketches)
        self.parts = {}
        self.wires = []
        self.used = {}           # Hole -> who is in it
        self.notes = []
        self.esp32 = self._add(Esp32())
        from .schematic import Schematic
        self.schematic = Schematic(self)
        Circuit.registry.append(self)

    # ------------------------------------------------------------ building blocks
    def copy(self, name, title, sketches=()):
        """Start the next step of a lesson from this circuit."""
        new = copy.deepcopy(self)
        new.name, new.title, new.sketches = name, title, list(sketches)
        Circuit.registry.append(new)
        return new

    def remove(self, *refs):
        """Take parts out again (and the wires and schematic pieces that belong to them)."""
        for ref in refs:
            part = self.parts.pop(ref)
            for leg, loc in part.legs.items():
                if isinstance(loc, Hole):
                    self.used.pop(loc, None)
        gone = set(refs)
        keep = []
        for w in self.wires:
            if w.tags & gone:
                for end in (w.a, w.b):
                    if isinstance(end, Hole):
                        self.used.pop(end, None)
            else:
                keep.append(w)
        self.wires = keep
        self.schematic.remove(gone)

    def _add(self, part):
        if part.ref in self.parts:
            raise CircuitError(f"{self.name}: there is already a part called {part.ref}")
        for leg, loc in part.legs.items():
            if isinstance(loc, Hole):
                self._take(loc, f"{part.ref}.{leg}")
        self.parts[part.ref] = part
        return part

    def _take(self, hole, who):
        if hole in self.used:
            raise CircuitError(f"{self.name}: {who} wants hole {hole}, but {self.used[hole]} is already in it")
        self.used[hole] = who

    @staticmethod
    def _hole(text):
        loc = parse_hole(text)
        if isinstance(loc, RailRef):
            raise CircuitError(f"{text!r}: give a column number for a part's leg")
        return loc

    # ------------------------------------------------------------ parts
    def resistor(self, ref, value, a, b):
        return self._add(Resistor(ref, value, self._hole(a), self._hole(b)))

    def led(self, ref, color, a, k):
        return self._add(Led(ref, color, self._hole(a), self._hole(k)))

    def ldr(self, ref, a, b):
        return self._add(Ldr(ref, "photoresistor", self._hole(a), self._hole(b)))

    def thermistor(self, ref, a, b):
        return self._add(Thermistor(ref, "thermistor", self._hole(a), self._hole(b)))

    def diode(self, ref, a, k):
        return self._add(Diode(ref, self._hole(a), self._hole(k)))

    def transistor(self, ref, e, b, c):
        return self._add(Transistor(ref, self._hole(e), self._hole(b), self._hole(c)))

    def tilt(self, ref, a, b):
        return self._add(Tilt(ref, "tilt switch", self._hole(a), self._hole(b)))

    def buzzer(self, ref, plus, minus, active=True):
        return self._add(Buzzer(ref, self._hole(plus), self._hole(minus), active))

    def button(self, ref, top_left, width=2):
        return self._add(Button(ref, self._hole(top_left), width))

    def pot(self, ref, left, middle, right, side="up"):
        return self._add(Pot(ref, [self._hole(h) for h in (left, middle, right)], side))

    def rgb_led(self, ref, r, k, g, b):
        return self._add(RgbLed(ref, [self._hole(h) for h in (r, k, g, b)]))

    def chip(self, ref, chip, pin1):
        return self._add(Dip(ref, chip, self._hole(pin1)))

    def display(self, ref, pin1, digits=1):
        return self._add(SevenSeg(ref, self._hole(pin1), digits))

    def module(self, ref, kind, at, rotate=0, label=None):
        loc = self._hole(at) if isinstance(at, str) else Point(*at)
        return self._add(Module(ref, kind, loc, rotate, label))

    def servo(self, ref, body, gnd, vcc, sig, rotate=0):
        return self._add(Leaded(ref, "servo", Point(*body), [self._hole(h) for h in (gnd, vcc, sig)], rotate))

    def motor(self, ref, body, a, b, rotate=0):
        return self._add(Leaded(ref, "motor", Point(*body), [self._hole(a), self._hole(b)], rotate))

    def power_module(self, ref, board="B", col=29):
        return self._add(PowerModule(ref, board, col))

    def note(self, text):
        """A short line printed under the breadboard picture."""
        self.notes.append(text)

    # ------------------------------------------------------------ wires
    def _candidates(self, spec):
        """Possible places for one end of a wire, plus the tag of the part it belongs to."""
        if isinstance(spec, tuple):
            return [Point(*spec)], None
        if "." in spec and ":" not in spec:
            ref, pin = spec.split(".", 1)
            if ref not in self.parts:
                raise CircuitError(f"{self.name}: wire to {spec}: no part called {ref}")
            part = self.parts[ref]
            if part is self.esp32:
                pin = part.resolve_pin(pin)
            legs = part.legs_of(pin) or ([pin] if pin in part.legs else [])
            if not legs:
                raise CircuitError(f"{self.name}: {ref} has no pin {pin!r} (it has {', '.join(part.pins())})")
            out = []
            for leg in legs:
                loc = part.legs[leg]
                if isinstance(loc, Point):
                    out.append(loc)
                else:
                    out += [h for h in B.strip_holes(loc.strip) if h not in self.used]
            if not out:
                raise CircuitError(f"{self.name}: no free hole left next to {spec}")
            return out, (None if part is self.esp32 else ref)
        loc = parse_hole(spec)
        if isinstance(loc, RailRef):
            free = [h for h in B.strip_holes(("rail", loc.board, loc.row)) if h not in self.used]
            return free, None
        return [loc], None

    def wire(self, a, b, color=None, via=(), bend=None, tag=None, bulge=None):
        """Add a jumper wire. `via` lists bend points (x, y) or hole names to route around parts;
        `bend` sets how much a plain wire curves (0 = straight, negative = the other way);
        `bulge` sets the curve's height in pitches instead."""
        ca, ta = self._candidates(a)
        cb, tb = self._candidates(b)
        best = min(((math.dist(p.xy, q.xy), i, j) for i, p in enumerate(ca) for j, q in enumerate(cb)))
        pa, pb = ca[best[1]], cb[best[2]]
        for p, spec in ((pa, a), (pb, b)):
            if isinstance(p, Hole):
                self._take(p, f"wire {a} → {b}")
        vias = [parse_hole(v).xy if isinstance(v, str) else v for v in via]
        tags = {t for t in (ta, tb, tag) if t}
        w = Wire(pa, pb, color, vias, bend, tags, bulge)
        self.wires.append(w)
        return w

    # ------------------------------------------------------------ connectivity
    def nets(self):
        """The circuit's nets as the breadboard makes them: a list of sets of (ref, pin)."""
        parent = {}

        def find(k):
            parent.setdefault(k, k)
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k

        def union(a, b):
            parent[find(a)] = find(b)

        def key(loc):
            return loc.strip if isinstance(loc, Hole) else ("pt", round(loc.x, 2), round(loc.y, 2))

        for part in self.parts.values():
            for leg, loc in part.legs.items():
                union(("T", part.ref, part.leg_pin[leg]), key(loc))
        for w in self.wires:
            union(key(w.a), key(w.b))
        groups = {}
        for k in list(parent):
            if k[0] == "T":
                groups.setdefault(find(k), set()).add((k[1], k[2]))
        return list(groups.values())

    def net_kind(self, net):
        if ("ESP32", "GND") in net or any(p == "-" and self.parts[r].kind == "power" for r, p in net):
            return "gnd"
        if ("ESP32", "3V3") in net:
            return "3v3"
        if ("ESP32", "5V") in net or any(p == "+" and self.parts[r].kind == "power" for r, p in net):
            return "5v"
        return "signal"

    # ------------------------------------------------------------ drawing
    def _wire_colors(self):
        nets = self.nets()
        loc_net = {}
        for i, net in enumerate(nets):
            for ref, pin in net:
                for leg in self.parts[ref].legs_of(pin):
                    loc = self.parts[ref].legs[leg]
                    loc_net[loc.strip if isinstance(loc, Hole) else ("pt", round(loc.x, 2), round(loc.y, 2))] = i
        # ESP32 pins give a signal its colour; number the signal nets in pin order
        palette = {}
        out = []
        for w in self.wires:
            if w.color:
                out.append(w.color)
                continue
            k = w.a.strip if isinstance(w.a, Hole) else ("pt", round(w.a.x, 2), round(w.a.y, 2))
            i = loc_net.get(k)
            if i is None:
                k = w.b.strip if isinstance(w.b, Hole) else ("pt", round(w.b.x, 2), round(w.b.y, 2))
                i = loc_net.get(k)
            kind = self.net_kind(nets[i]) if i is not None else "signal"
            if kind != "signal":
                out.append(WIRE_COLORS[kind])
            else:
                if i not in palette:
                    palette[i] = SIGNAL_COLORS[len(palette) % len(SIGNAL_COLORS)]
                out.append(palette[i])
        return out

    def breadboard_svg(self):
        svg = Svg(scale=10)
        for b in "AB":
            draw_board(svg, b)
        parts = list(self.parts.values())
        # parts that hang off the board first, so their wires lie on top of the board
        order = [p for p in parts if p.kind in ("power",)] + [self.esp32] + \
                [p for p in parts if p.kind not in ("esp32", "power")]
        for p in order:
            p.draw(svg)
        for w, color in zip(self.wires, self._wire_colors()):
            draw_wire(svg, w, color)
        place_labels(svg, parts)
        y = 2 * B.BOARD_H + 1.4
        for n in self.notes:
            svg.text(B.BOARD_X0, y, n, size=0.85, fill="#495057", anchor="start")
            y += 1.3
        return svg.render(margin=0.8, title=self.title)


# ---------------------------------------------------------------- labels
def _overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def place_labels(svg, parts):
    """Put each part's reference (R1, D2 ...) next to it, avoiding parts and other labels."""
    boxes = {}
    for p in parts:
        tmp = Svg()
        p.draw(tmp)
        boxes[p.ref] = tuple(tmp.box)
    placed = []
    size = 0.8
    for p in parts:
        if p.kind == "esp32" or p.label_xy() is None:
            continue
        x0, y0, x1, y1 = boxes[p.ref]
        w = 0.5 * size * len(p.ref) + 0.3
        h = size + 0.1
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        pref = p.label_xy()
        cands = [pref, (cx, y0 - h / 2 - 0.05), (cx, y1 + h / 2 + 0.05), (x1 + w / 2 + 0.1, cy),
                 (x0 - w / 2 - 0.1, cy), (x1 + w / 2 + 0.1, y0), (x0 - w / 2 - 0.1, y0),
                 (x1 + w / 2 + 0.1, y1), (x0 - w / 2 - 0.1, y1), (cx, y0 - h * 1.6), (cx, y1 + h * 1.6)]
        best = None
        for i, (lx, ly) in enumerate(cands):
            box = (lx - w / 2, ly - h / 2, lx + w / 2, ly + h / 2)
            cost = sum(_overlap(box, b) for b in placed) * 3
            cost += sum(_overlap(box, b) for r, b in boxes.items() if r != p.ref and r != "ESP32")
            cost += _overlap(box, boxes["ESP32"]) * 2 + i * 0.01
            if best is None or cost < best[0]:
                best = (cost, lx, ly, box)
        _, lx, ly, box = best
        placed.append(box)
        svg.raw('<g paint-order="stroke" stroke="#ffffff" stroke-width="3" stroke-linejoin="round">')
        svg.text(lx, ly, p.ref, size=size, fill="#343a40", weight="bold")
        svg.raw("</g>")


# ---------------------------------------------------------------- board and wire drawing
def draw_board(svg, board):
    y0 = B.BOARD_Y0[board]
    svg.rect(B.BOARD_X0, y0 + 0.08, B.BOARD_X1 - B.BOARD_X0, B.BOARD_H - 0.16, fill="#f4f2ed",
             stroke="#d6d1c4", sw=0.12, rx=0.5)
    svg.rect(B.BOARD_X0 + 0.2, y0 + B.ROW_Y["e"] + 0.85, B.BOARD_X1 - B.BOARD_X0 - 0.4, 1.3, fill="#e6e1d5", rx=0.3)
    # rail stripes: red next to +, blue next to -
    for row, dy, color in (("tp", -0.6, "#e03131"), ("tn", 0.6, "#1c7ed6"), ("bn", -0.6, "#1c7ed6"), ("bp", 0.6, "#e03131")):
        y = y0 + B.ROW_Y[row] + dy
        svg.line(1.3, y, 30.7, y, stroke=color, sw=0.12)
    for row, sign in (("tp", "+"), ("tn", "−"), ("bn", "−"), ("bp", "+")):
        y = y0 + B.ROW_Y[row]
        color = "#e03131" if sign == "+" else "#1c7ed6"
        for x in (0.45, 31.0):
            svg.text(x, y, sign, size=0.9, fill=color, weight="bold")
    for h in B.all_holes():
        if h.board != board:
            continue
        x, y = h.xy
        svg.rect(x - 0.18, y - 0.18, 0.36, 0.36, fill="#5c5f63", rx=0.06)
    for r in "abcdefghij":
        y = y0 + B.ROW_Y[r]
        svg.text(-0.05, y, r, size=0.55, fill="#9a9384")
        svg.text(31.0, y, r, size=0.55, fill="#9a9384")
    for c in (1, 5, 10, 15, 20, 25, 30):
        svg.text(c, y0 + 3.0, str(c), size=0.55, fill="#9a9384")
        svg.text(c, y0 + 16.0, str(c), size=0.55, fill="#9a9384")
    svg.text(B.BOARD_X0 + 0.2, y0 - 0.55 if board == "A" else y0 + B.BOARD_H + 0.55,
             f"breadboard {board}", size=0.6, fill="#9a9384", anchor="start", style="italic")


def draw_wire(svg, w, color):
    a, b = w.a.xy, w.b.xy
    pts = [a] + list(w.via) + [b]
    cmds = [("M", *a)]
    if len(pts) == 2:
        d = math.dist(a, b)
        bend = 0.16 if w.bend is None else w.bend
        if (d < 2.2 or bend == 0) and not w.bulge:
            cmds.append(("L", *b))
        else:
            off = max(min(bend * d, 2.2), -2.2)    # negative bend bulges down / right
            if w.bulge is not None:
                off = w.bulge
            nx, ny = -(b[1] - a[1]) / d, (b[0] - a[0]) / d
            if ny > 0 or (ny == 0 and nx > 0):      # normally bulge up / to the left
                nx, ny = -nx, -ny
            cx, cy = (a[0] + b[0]) / 2 + nx * off, (a[1] + b[1]) / 2 + ny * off
            cmds.append(("Q", cx, cy, *b))
    else:
        # straight runs with rounded corners through the via points
        for i in range(1, len(pts) - 1):
            p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
            r = min(0.8, math.dist(p0, p1) / 2, math.dist(p1, p2) / 2)
            u = ((p1[0] - p0[0]) / math.dist(p0, p1), (p1[1] - p0[1]) / math.dist(p0, p1))
            v = ((p2[0] - p1[0]) / math.dist(p1, p2), (p2[1] - p1[1]) / math.dist(p1, p2))
            cmds.append(("L", p1[0] - u[0] * r, p1[1] - u[1] * r))
            cmds.append(("Q", p1[0], p1[1], p1[0] + v[0] * r, p1[1] + v[1] * r))
        cmds.append(("L", *b))
    light = color.lower() in ("#ffffff", "#fff", "white")
    svg.path(cmds, stroke="#868e96" if light else "#00000066", sw=0.56, cap="round", join="round")
    svg.path(cmds, stroke=color, sw=0.4, cap="round", join="round")
    for p in (w.a, w.b):
        if isinstance(p, Hole):
            x, y = p.xy
            svg.rect(x - 0.2, y - 0.2, 0.4, 0.4, fill="#adb5bd", stroke="#495057", sw=0.05, rx=0.05)
