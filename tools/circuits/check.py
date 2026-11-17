"""Check that a circuit's breadboard picture, its schematic and its sketches agree."""
import re
from pathlib import Path


def signature(circuit, nets):
    """Nets as a comparable multiset. Legs of symmetric parts (a resistor) are
    interchangeable, so they all count as pin '~'. Unconnected pins are ignored."""
    out = []
    for net in nets:
        terms = []
        for ref, pin in net:
            part = circuit.parts.get(ref)
            sym = part is not None and part.symmetric
            terms.append((ref, "~" if sym else pin))
        if len(set(terms)) >= 2 or len(net) >= 2:
            out.append(tuple(sorted(terms)))
    return sorted(out)


def describe(net):
    return ", ".join(f"{r}.{p}" for r, p in net)


def compare(circuit):
    """Problems found, as a list of strings (empty when everything matches)."""
    problems = []
    bb = signature(circuit, circuit.nets())
    sc = signature(circuit, circuit.schematic.nets())
    if bb != sc:
        bbs, scs = list(bb), list(sc)
        for n in bb:
            if n in scs:
                scs.remove(n)
                bbs.remove(n)
        for n in bbs:
            problems.append(f"breadboard joins  {describe(n)}  but the schematic doesn't")
        for n in scs:
            problems.append(f"schematic joins   {describe(n)}  but the breadboard doesn't")
    # every part on the breadboard should be in the schematic
    in_sc = {r for net in circuit.schematic.nets() for r, _ in net}
    for ref, part in circuit.parts.items():
        if ref not in in_sc and part.kind != "esp32":
            problems.append(f"{ref} is on the breadboard but not in the schematic")
    return problems


def sketch_pins(lesson_dir, names):
    """GPIO numbers that a lesson's sketches put on pins (const ints and pin arrays)."""
    pins = set()
    for name in names:
        hits = list(Path(lesson_dir).rglob(f"{name}/{name}.ino"))
        if not hits:
            raise FileNotFoundError(f"{lesson_dir}: sketch {name} not found")
        src = hits[0].read_text()
        for m in re.finditer(r"const\s+int\s+(\w+)\s*=\s*(\d+)\s*;", src):
            if re.search(r"PIN|LED|BUTTON|BTN|BUZZER|RED|GREEN|BLUE|YELLOW|KNOB|SENSOR|TILT|IR_", m.group(1)):
                pins.add(int(m.group(2)))
        for m in re.finditer(r"(?:const\s+)?(?:int|byte)\s+(\w*(?:[Pp]ins?|leds|keys|PINS)\w*)\s*\[[^\]]*\]\s*=\s*\{([^}]*)\}", src):
            pins.update(int(v) for v in re.findall(r"\d+", m.group(2)))
        for m in re.finditer(r"DHT\s+\w+\(\s*(\d+)\s*,", src):
            pins.add(int(m.group(1)))
        for m in re.finditer(r"byte\s+(rowPins|colPins)\s*\[[^\]]*\]\s*=\s*\{([^}]*)\}", src):
            pins.update(int(v) for v in re.findall(r"\d+", m.group(2)))
    return pins


def circuit_gpios(circuit):
    used = set()
    for net in circuit.nets():
        if len(net) < 2:
            continue
        for ref, pin in net:
            if ref == "ESP32" and pin.startswith("GPIO"):
                used.add(int(pin[4:]))
    return used


def check_sketches(circuit, lesson_dir):
    """Every pin a sketch drives must be wired up. (Wired pins that this sketch doesn't
    use are fine: lessons keep earlier parts on the board.)"""
    if not circuit.sketches:
        return []
    wired = circuit_gpios(circuit)
    # I2C and SPI pins are used by libraries, not named in the sketch
    problems = []
    for name in circuit.sketches:
        want = sketch_pins(lesson_dir, [name])
        missing = sorted(want - wired)
        if missing:
            problems.append(f"sketch {name} uses pin(s) {', '.join(map(str, missing))}, which are not wired")
    return problems
