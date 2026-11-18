"""Schematic view of a circuit, drawn with schemdraw from a few reusable patterns.

The ESP32 sits on the left with the GPIO pins it uses down its right side. Each
pattern adds a horizontal *band* to the right of the ESP32:

    s = circuit.schematic
    s.led(26, "R1", "D1")                     pin -> resistor -> LED -> GND
    s.chain(13, ["SW1"])                      pin -> any two-leg parts -> GND
    s.pot(34, "RV1")                          knob between 3V3 and GND, wiper to the pin
    s.divider(35, top="LDR1", bottom="R4")    3V3 -> top -> pin -> bottom -> GND
    s.rgb_led((25, 26, 27), ("R1", "R2", "R3"), "D1")
    s.module("U2", left=[("S", 4)], top=[("+", "3V3")], bottom=[("-", "GND")])
    s.bus("I2C", {"SDA": 21, "SCL": 22}, ["U2", "U3"], power={"VCC": "3V3", "GND": "GND"})

Every pattern also records which pins it joins, so the schematic can be checked
against the breadboard picture (see check.py).
"""
import schemdraw
schemdraw.use("svg")
import schemdraw.elements as elm
from schemdraw.elements import Element, Element2Term
from schemdraw.segments import Segment, SegmentArc, SegmentText

UNIT = 2.0        # length of a resistor, LED ...
PS = 1.2          # spacing of pins on a block
LEAD = 0.5        # pin lead length
CH = 0.155        # width of one character at FONT 10
FONT = 13
SMALL = 9.5

NET_LABELS = {"3V3": "3V3", "5V": "5V", "VM": "+5V ext", "GND": "GND"}
TWO_LEG = {
    # part kind -> (schemdraw element, first pin, second pin)
    "resistor": (elm.Resistor, "1", "2"),
    "led": (elm.LED, "A", "K"),
    "button": (elm.Button, "1", "2"),
    "tilt": (elm.Switch, "1", "2"),
    "ldr": (elm.Photoresistor, "1", "2"),
    "motor": (elm.Motor, "1", "2"),
}


def text_w(s, size=FONT):
    return len(s) * CH * size / 10


# ---------------------------------------------------------------- custom elements
class BuzzerSym(Element2Term):
    """A buzzer: a dome on a flat base, '+' on the left lead."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r = 0.45
        self.segments.append(Segment([(0, 0), (0.1, 0), (0.1, -0.1), (0.1 + 2 * r, -0.1), (0.1 + 2 * r, 0), (0.2 + 2 * r, 0)]))
        self.segments.append(SegmentArc((0.1 + r, -0.1), 2 * r, 2 * r, theta1=0, theta2=180))
        self.segments.append(Segment([(0.1 + r * 0.6, -0.1), (0.1 + r * 0.6, 0.0)]))
        self.segments.append(SegmentText((-0.05, 0.25), "+", fontsize=SMALL))
        self.elmparams["lblofst"] = 0.7


class Block(Element):
    """A rectangle with pins. pins: dicts with name, side ('L','R','T','B'), pos (distance
    from the top for L/R, from the left for T/B), optional num and anchor."""
    def __init__(self, w, h, pins, title="", ref="", title_pos=None, vertical_title=False, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (w, 0), (w, -h), (0, -h), (0, 0)]))
        for p in pins:
            side, pos = p["side"], p["pos"]
            if side == "L":
                inner, outer, lbl, al = (0, -pos), (-LEAD, -pos), (0.12, -pos), ("left", "center")
            elif side == "R":
                inner, outer, lbl, al = (w, -pos), (w + LEAD, -pos), (w - 0.12, -pos), ("right", "center")
            elif side == "T":
                inner, outer, lbl, al = (pos, 0), (pos, LEAD), (pos, -0.4), ("center", "center")
            else:
                inner, outer, lbl, al = (pos, -h), (pos, -h - LEAD), (pos, -h + 0.4), ("center", "center")
            self.segments.append(Segment([inner, outer]))
            if p.get("name"):
                self.segments.append(SegmentText(lbl, p["name"], align=al, fontsize=FONT - 1))
            if p.get("num") is not None:
                if side in "LR":
                    npos = ((inner[0] + outer[0]) / 2, -pos + 0.17)
                    nal = ("center", "bottom")
                else:
                    npos = (pos + 0.1, (inner[1] + outer[1]) / 2)
                    nal = ("left", "center")
                self.segments.append(SegmentText(npos, str(p["num"]), align=nal, fontsize=SMALL, color="#666"))
            self.anchors[p.get("anchor", p["name"])] = outer
        if title:
            if vertical_title:
                self.segments.append(SegmentText((0.45, -h / 2), title, align=("center", "center"),
                                                 rotation=90, fontsize=FONT + 1))
            else:
                tp = title_pos or (w / 2, -h / 2)
                txt = f"{ref}\n{title}" if ref else title
                self.segments.append(SegmentText(tp, txt, align=("center", "center"), fontsize=FONT))
        self.anchors["topleft"] = (0, 0)
        self.elmparams["drop"] = (0, 0)


# ---------------------------------------------------------------- the schematic
class Schematic:
    def __init__(self, circuit):
        self.circuit = circuit
        self.bands = []
        self.notes = []

    # ----- netlist bookkeeping (filled in while drawing)
    def _reset(self):
        self.terms = {}
        self.counter = 0

    def join(self, net, ref, pin):
        self.terms.setdefault(net, set()).add((ref, pin))

    def new_net(self):
        self.counter += 1
        return f"_n{self.counter}"

    def part(self, ref):
        try:
            return self.circuit.parts[ref]
        except KeyError:
            raise KeyError(f"{self.circuit.name}: the schematic uses {ref}, which is not on the breadboard")

    def remove(self, refs):
        self.bands = [b for b in self.bands if not (b.refs & refs)]

    # ----- patterns
    def chain(self, gpio, refs, end="GND"):
        self.bands.append(ChainBand(self, gpio, refs, end))

    def led(self, gpio, resistor, led):
        self.chain(gpio, [resistor, led])

    def pot(self, gpio, ref, ends=("3V3", "GND")):
        self.bands.append(PotBand(self, gpio, ref, ends))

    def divider(self, gpio, top, bottom, supply="3V3"):
        self.bands.append(DividerBand(self, gpio, top, bottom, supply))

    def rgb_led(self, gpios, resistors, ref):
        self.bands.append(RgbBand(self, gpios, resistors, ref))

    def module(self, ref, left=(), top=(), bottom=(), right=(), title=None, numbers=None, note=None):
        """left: (pin, gpio) or (pin, gpio, [via...]) with via = "R1" (in series) or
        ("shunt", "R2", "GND") (from the wire to a net). None leaves a gap.
        top/bottom: (pin, net). right: (pin, net), (pin, "chain", [refs], net) to a shared
        net line, (pin, "pair", pin2, ref) for a part between two right pins, or None."""
        self.bands.append(ModuleBand(self, ref, list(left), list(top), list(bottom), list(right), title,
                                     numbers or {}, note))

    def bus(self, name, lines, refs, power):
        self.bands.append(BusBand(self, name, lines, refs, power))

    def note(self, text):
        self.notes.append(text)

    # ----- drawing
    def render(self):
        self._reset()
        esp = self.circuit.esp32
        d = schemdraw.Drawing(show=False)
        d.config(unit=UNIT, fontsize=FONT, lw=1.3, font="sans-serif")
        XR = 3.4                                    # the ESP32 block's right edge
        x0 = XR + LEAD
        y = 0.0
        rows = []
        for band in self.bands:
            band.measure()
            for gpio, dy in band.rows:
                rows.append((gpio, y - dy))
            band.top = y
            y -= band.height + 0.6
        ybottom = min(y + 0.6, -3.0)
        # which ESP32 power pins are in use (anything in the band nets, or on the breadboard)
        for band in self.bands:
            band.draw(d, x0, band.top)
        used_power = [n for n in ("3V3", "5V") if n in self.terms]
        h = -ybottom + 1.2
        pins = []
        seen = set()
        for gpio, yy in rows:
            name = esp.resolve_pin(str(gpio))
            if name in seen:
                raise ValueError(f"{self.circuit.name}: GPIO {gpio} is used twice in the schematic")
            seen.add(name)
            pins.append(dict(name=name, side="R", pos=-(yy - 0.6), anchor=name))
            self.join(name, "ESP32", name)
        for i, n in enumerate(used_power):
            pins.append(dict(name="", side="T", pos=1.4 + i * 1.3, anchor=n))   # the supply symbol names it
            self.join(n, "ESP32", n)
        if "GND" in self.terms:
            pins.append(dict(name="GND", side="B", pos=1.7, anchor="GND"))
            self.join("GND", "ESP32", "GND")
        blk = d.add(Block(XR, h, pins, title="ESP32 DevKit V1", vertical_title=True).at((0, 0.6)).theta(0))
        for n in used_power:
            d.add(elm.Vdd().at(blk.absanchors[n]).theta(0).label(NET_LABELS[n], fontsize=FONT - 1))
        if "GND" in self.terms:
            d.add(elm.Ground().at(blk.absanchors["GND"]).theta(0))
        if self.notes:
            d.add(elm.Label().at((0, ybottom - 2.0)).label("\n".join(self.notes), loc="center", halign="left",
                                                             fontsize=FONT - 1))
        return d

    def svg(self):
        d = self.render()
        return d.get_imagedata("svg").decode()

    def nets(self):
        self.render()
        return [set(v) for v in self.terms.values()]


# ---------------------------------------------------------------- bands
class Band:
    refs = set()
    rows = []
    height = 1.0
    top = 0.0

    def measure(self):
        pass

    def draw(self, d, x0, top):
        raise NotImplementedError


def two_leg(s, ref, label_side="top"):
    part = s.part(ref)
    if part.kind == "buzzer":
        return BuzzerSym(), "+", "-", f"{ref}\n{'active' if part.active else 'passive'} buzzer"
    cls, p1, p2 = TWO_LEG[part.kind]
    if part.kind == "resistor":
        label = f"{ref}\n{part.value}"
    elif part.kind == "led":
        label = f"{ref}\n{part.color}"
    elif part.kind == "tilt":
        label = f"{ref}\ntilt switch"
    elif part.kind == "ldr":
        label = f"{ref}\nphotoresistor"
    elif part.kind == "motor":
        label = f"{ref}\nDC motor"
    else:
        label = ref
    return cls(), p1, p2, label


def end_symbol(d, s, at, net, direction="down"):
    if net == "GND":
        d.add(elm.Ground().at(at).theta(0))
    else:
        d.add(elm.Vdd().at(at).theta(0).label(NET_LABELS.get(net, net), fontsize=FONT - 1))


class ChainBand(Band):
    def __init__(self, s, gpio, refs, end):
        self.s, self.gpio, self.chain, self.end = s, gpio, list(refs), end
        self.refs = set(refs)

    def measure(self):
        self.rows = [(self.gpio, 1.0)]
        self.height = 2.4

    def draw(self, d, x0, top):
        s = self.s
        y = top - 1.0
        pin = s.circuit.esp32.resolve_pin(str(self.gpio))
        net = pin
        d.add(elm.Line().at((x0, y)).right().length(0.6))
        for ref in self.chain:
            e, p1, p2, label = two_leg(s, ref)
            el = d.add(e.right().label(label, fontsize=FONT - 1))
            s.join(net, ref, p1)
            net = s.new_net()
            s.join(net, ref, p2)
        if self.end == "GND":
            d.add(elm.Line().right().length(0.4))
            end_symbol(d, s, d.here, "GND")
        else:
            d.add(elm.Line().right().length(0.4))
            end_symbol(d, s, d.here, self.end)
        s.terms.setdefault(self.end, set()).update(s.terms.pop(net))


class PotBand(Band):
    def __init__(self, s, gpio, ref, ends):
        self.s, self.gpio, self.ref, self.ends = s, gpio, ref, ends
        self.refs = {ref}

    def measure(self):
        self.rows = [(self.gpio, 2.4)]
        self.height = 4.8

    def draw(self, d, x0, top):
        s = self.s
        y = top - 2.4
        pin = s.circuit.esp32.resolve_pin(str(self.gpio))
        d.add(elm.Line().at((x0, y)).right().length(1.6))
        pot = d.add(elm.Potentiometer().down().anchor("tap").at((x0 + 1.6, y)).flip()
                    .label(f"{self.ref}\n10 kΩ knob", loc="bottom", ofst=0.25, fontsize=FONT - 1))
        s.join(pin, self.ref, "W")
        # the supply is drawn on top, whichever leg it is on
        (p_top, top_net), (p_bot, bot_net) = ("1", self.ends[0]), ("2", self.ends[1])
        if top_net == "GND":
            (p_top, top_net), (p_bot, bot_net) = (p_bot, bot_net), (p_top, top_net)
        s.join(top_net, self.ref, p_top)
        s.join(bot_net, self.ref, p_bot)
        for net, a in ((top_net, pot.start), (bot_net, pot.end)):
            end_symbol(d, s, a, net)


class DividerBand(Band):
    def __init__(self, s, gpio, top, bottom, supply):
        self.s, self.gpio, self.topref, self.botref, self.supply = s, gpio, top, bottom, supply
        self.refs = {top, bottom}

    def measure(self):
        self.rows = [(self.gpio, 3.0)]
        self.height = 6.0

    def draw(self, d, x0, top):
        s = self.s
        y = top - 3.0
        pin = s.circuit.esp32.resolve_pin(str(self.gpio))
        d.add(elm.Line().at((x0, y)).right().length(1.6))
        d.add(elm.Dot())
        jx = x0 + 1.6
        e, p1, p2, label = two_leg(s, self.topref)
        el = d.add(e.at((jx, y)).up().label(label, loc="bottom", fontsize=FONT - 1))
        s.join(pin, self.topref, p1)
        s.join(self.supply, self.topref, p2)
        end_symbol(d, s, el.end, self.supply)
        e, p1, p2, label = two_leg(s, self.botref)
        el = d.add(e.at((jx, y)).down().label(label, loc="bottom", fontsize=FONT - 1))
        s.join(pin, self.botref, p1)
        s.join("GND", self.botref, p2)
        end_symbol(d, s, el.end, "GND")


class RgbBand(Band):
    def __init__(self, s, gpios, resistors, ref):
        self.s, self.gpios, self.res, self.ref = s, list(gpios), list(resistors), ref
        self.refs = set(resistors) | {ref}

    def measure(self):
        self.rows = [(g, 1.0 + i * 1.5) for i, g in enumerate(self.gpios)]
        self.height = 1.0 + 3 * 1.5 + 0.8

    def draw(self, d, x0, top):
        s = self.s
        xc = x0 + 0.5 + 2 * UNIT + 0.9
        for i, (g, r, color, pin) in enumerate(zip(self.gpios, self.res, ("red", "green", "blue"), "RGB")):
            y = top - 1.0 - i * 1.5
            gpin = s.circuit.esp32.resolve_pin(str(g))
            d.add(elm.Line().at((x0, y)).right().length(0.5))
            d.add(elm.Resistor().right().label(f"{r}  {s.part(r).value}", fontsize=FONT - 2, ofst=0.05))
            s.join(gpin, r, "1")
            n = s.new_net()
            s.join(n, r, "2")
            s.join(n, self.ref, pin)
            d.add(elm.LED().right().length(UNIT * 0.75).label(color, fontsize=FONT - 2, ofst=0.05))
            d.add(elm.Line().right().tox(xc))
            if i:
                d.add(elm.Dot())
        ytop, ybot = top - 1.0, top - 1.0 - 3.0
        d.add(elm.Line().at((xc, ytop)).down().toy(ybot - 0.6))
        end_symbol(d, s, d.here, "GND")
        s.join("GND", self.ref, "K")
        bx0 = x0 + 0.5 + UNIT + 0.2
        bx0 = x0 + 0.5 + UNIT + 0.2
        x1, y1, y2 = xc + 0.35, ytop + 0.75, ybot - 0.4
        for a, b in (((bx0, y1), (x1, y1)), ((x1, y1), (x1, y2)), ((x1, y2), (bx0, y2)), ((bx0, y2), (bx0, y1))):
            d.add(elm.Line(ls="--", lw=0.8).at(a).to(b))
        d.add(elm.Label().at((xc + 0.55, ytop - 1.5)).label(f"{self.ref}\nRGB LED\n(common –)", halign="left",
                                                           fontsize=FONT - 1))


class ModuleBand(Band):
    def __init__(self, s, ref, left, top, bottom, right, title, numbers, note):
        self.s, self.ref = s, ref
        self.left, self.top_pins, self.bottom, self.right = left, top, bottom, right
        self.title, self.numbers, self.note = title, numbers, note
        self.refs = {ref}
        for entry in left:
            if entry and len(entry) > 2:
                for v in entry[2]:
                    self.refs.add(v if isinstance(v, str) else v[1])
        for entry in right:
            if entry and len(entry) > 2 and entry[1] == "chain":
                self.refs.update(entry[2])
            if entry and len(entry) > 2 and entry[1] == "pair":
                self.refs.add(entry[3])

    def via_len(self, entry):
        n = 0.0
        for v in (entry[2] if entry and len(entry) > 2 else []):
            n += UNIT + 0.4 if isinstance(v, str) else 1.4
        return n

    def measure(self):
        n = max(len(self.left), len(self.right), 2)
        self.ps = 1.7 if any(e and len(e) > 2 and e[1] == "chain" for e in self.right) else PS
        PSb = self.ps
        has_top = bool(self.top_pins)
        self.p0 = 1.1 if has_top else 0.6               # first side pin, below the block's top edge
        self.y_first = 1.0 + self.p0 if has_top else 0.9
        self.rows = [(e[1], self.y_first + PSb * i) for i, e in enumerate(self.left) if e]
        self.block_h = self.p0 + PSb * (n - 1) + (1.1 if self.bottom else 0.6)
        self.height = self.y_first - 0.6 + self.block_h + (1.6 if self.bottom else 0.4)
        if any(e and len(e) > 2 and not isinstance(v, str) for e in self.left for v in (e[2] if e and len(e) > 2 else [])):
            self.height += 1.2

    def draw(self, d, x0, top):
        s = self.s
        part = s.part(self.ref)
        title = self.title or part.label
        nums = self.numbers
        gap = max([self.via_len(e) for e in self.left] + [0]) + 1.4
        lw = max([text_w(e[0]) for e in self.left if e] + [0])
        rw = max([text_w(e[0]) for e in self.right if e] + [0])
        tw = max(text_w(title), text_w(self.ref))
        tb = max(len(self.top_pins), len(self.bottom))
        sup = max([text_w(NET_LABELS.get(n, n), FONT - 1) for _, n in self.top_pins] + [0])
        w = max(lw + rw + tw + 0.9, tb * 1.4 + 0.6, (len(self.top_pins) + 1) * (sup + 0.2), 3.0)
        bx = x0 + gap + LEAD
        by = top - self.y_first + self.p0
        pins = []
        for i, e in enumerate(self.left):
            if e:
                pins.append(dict(name=e[0], side="L", pos=self.p0 + self.ps * i, num=nums.get(e[0]), anchor="L_" + e[0]))
        for i, e in enumerate(self.right):
            if e:
                pins.append(dict(name=e[0], side="R", pos=self.p0 + self.ps * i, num=nums.get(e[0]), anchor="R_" + e[0]))
        spread = lambda k, n: (w / (n + 1)) * (k + 1)
        for k, (p, net) in enumerate(self.top_pins):
            pins.append(dict(name=p, side="T", pos=spread(k, len(self.top_pins)), num=nums.get(p), anchor="T_" + p))
        for k, (p, net) in enumerate(self.bottom):
            pins.append(dict(name=p, side="B", pos=spread(k, len(self.bottom)), num=nums.get(p), anchor="B_" + p))
        tx = lw + 0.25 + (w - lw - rw - 0.5) / 2
        blk = d.add(Block(w, self.block_h, pins, title=title, ref=self.ref, title_pos=(tx, -self.block_h / 2))
                    .at((bx, by)).theta(0))
        A = blk.absanchors
        # left side: wires from the ESP32, with parts along the way
        for i, e in enumerate(self.left):
            if not e:
                continue
            pin, gpio = e[0], e[1]
            vias = e[2] if len(e) > 2 else []
            gpin = s.circuit.esp32.resolve_pin(str(gpio))
            y = A["L_" + pin][1]
            net = gpin
            d.add(elm.Line().at((x0, y)).right().length(0.5))
            for v in vias:
                if isinstance(v, str):
                    el, p1, p2, label = two_leg(s, v)
                    lbl = v if sum(isinstance(x, str) for x in vias) and len(self.left) > 4 else label
                    d.add(el.right().label(lbl, fontsize=FONT - 2, ofst=0.05))
                    s.join(net, v, p1)
                    net = s.new_net()
                    s.join(net, v, p2)
                else:
                    _, ref, to = v
                    d.add(elm.Line().right().length(0.7))
                    d.add(elm.Dot())
                    here = d.here
                    el, p1, p2, label = two_leg(s, ref)
                    e2 = d.add(el.at(here).down().length(UNIT * 0.8).label(label, loc="bottom", fontsize=FONT - 2))
                    s.join(net, ref, p1)
                    s.join(to, ref, p2)
                    end_symbol(d, s, e2.end, to)
                    d.add(elm.Line().at(here).right().length(0.7))
            d.add(elm.Line().right().tox(A["L_" + pin][0]))
            s.join(net, self.ref, pin)
        for p, net in self.top_pins:
            s.join(net, self.ref, p)
            end_symbol(d, s, A["T_" + p], net)
        for p, net in self.bottom:
            s.join(net, self.ref, p)
            end_symbol(d, s, A["B_" + p], net)
        # right side
        busx = None
        bus_rows = []
        for i, e in enumerate(self.right):
            if not e:
                continue
            pin = e[0]
            a = A["R_" + pin]
            if len(e) == 1:          # a pin drawn for reference only (the far end of a "pair")
                continue
            if len(e) == 2:
                s.join(e[1], self.ref, pin)
                d.add(elm.Line().at(a).right().length(0.5))
                end_symbol(d, s, d.here, e[1])
            elif e[1] == "chain":
                refs, endnet = e[2], e[3]
                net = s.new_net()
                s.join(net, self.ref, pin)
                d.add(elm.Line().at(a).right().length(0.3))
                for ref in refs:
                    el, p1, p2, label = two_leg(s, ref)
                    d.add(el.right().length(UNIT * 0.8).label(ref, fontsize=FONT - 2,
                                                             ofst=0.3 if s.part(ref).kind == "led" else 0.05))
                    s.join(net, ref, p1)
                    net = s.new_net()
                    s.join(net, ref, p2)
                s.terms.setdefault(endnet, set()).update(s.terms.pop(net))
                bus_rows.append((d.here, endnet))
            elif e[1] == "pair":
                pin2, ref = e[2], e[3]
                b = A["R_" + pin2]
                el, p1, p2, label = two_leg(s, ref)
                d.add(elm.Line().at(a).right().length(1.0))
                d.add(el.down().toy(b[1]).label(label, loc="bottom", fontsize=FONT - 1))
                d.add(elm.Line().left().tox(b[0]))
                n1, n2 = s.new_net(), s.new_net()
                s.join(n1, self.ref, pin)
                s.join(n1, ref, p1)
                s.join(n2, self.ref, pin2)
                s.join(n2, ref, p2)
        if bus_rows:
            busx = max(p[0] for p, _ in bus_rows) + 0.4
            for p, _ in bus_rows:
                d.add(elm.Line().at(p).right().tox(busx))
            ys = [p[1] for p, _ in bus_rows]
            for yy in ys[1:]:
                d.add(elm.Dot().at((busx, yy)))
            d.add(elm.Line().at((busx, max(ys))).down().toy(min(ys) - 0.8))
            end_symbol(d, s, d.here, bus_rows[0][1])
        if self.note:
            d.add(elm.Label().at((bx + w / 2, by - self.block_h - (1.5 if self.bottom else 0.5)))
                  .label(self.note, fontsize=FONT - 2, halign="center"))


class BusBand(Band):
    """I²C: two shared lines with modules hanging underneath."""
    def __init__(self, s, name, lines, refs, power):
        self.s, self.name, self.lines, self.mods, self.power = s, name, dict(lines), list(refs), dict(power)
        self.refs = set(refs)

    def measure(self):
        names = list(self.lines)
        self.rows = [(self.lines[n], 0.8 + 0.8 * i) for i, n in enumerate(names)]
        self.height = 0.8 + 0.8 * len(names) + 1.8 + 3.0 + 1.6

    def draw(self, d, x0, top):
        s = self.s
        names = list(self.lines)
        ys = {n: top - 0.8 - 0.8 * i for i, n in enumerate(names)}
        mod_top = top - 0.8 - 0.8 * len(names) - 1.8
        x = x0 + 2.2
        taps = []
        for ref in self.mods:
            part = s.part(ref)
            pw = [p for p in self.power]   # e.g. VCC, GND
            w = max(text_w(part.label) + 0.8, 1.4 * len(names) + 1.6, 3.6)
            h = 3.0
            pins = []
            for k, n in enumerate(names):
                pins.append(dict(name=n, side="T", pos=1.0 + 1.2 * k, anchor="T_" + n))
            vcc = [p for p, net in self.power.items() if net != "GND"]
            gnd = [p for p, net in self.power.items() if net == "GND"]
            for p in vcc:
                pins.append(dict(name=p, side="L", pos=h / 2, anchor="L_" + p))
            for p in gnd:
                pins.append(dict(name=p, side="B", pos=w / 2, anchor="B_" + p))
            blk = d.add(Block(w, h, pins, title=part.label, ref=ref, title_pos=(w / 2 + 0.3, -h / 2 - 0.25))
                        .at((x + 1.4, mod_top)).theta(0))
            A = blk.absanchors
            for n in names:
                a = A["T_" + n]
                d.add(elm.Line().at(a).up().toy(ys[n]))
                d.add(elm.Dot())
                taps.append(a[0])
                gpin = s.circuit.esp32.resolve_pin(str(self.lines[n]))
                s.join(gpin, ref, n)
            for p in vcc:
                d.add(elm.Line().at(A["L_" + p]).left().length(0.6))
                end_symbol(d, s, d.here, self.power[p])
                s.join(self.power[p], ref, p)
            for p in gnd:
                end_symbol(d, s, A["B_" + p], "GND")
                s.join("GND", ref, p)
            x += 1.4 + w + 1.6
        for n in names:
            d.add(elm.Line().at((x0, ys[n])).right().tox(max(taps) + 0.6))
            d.add(elm.Label().at((max(taps) + 0.7, ys[n])).label(n, halign="left", fontsize=FONT - 2))
