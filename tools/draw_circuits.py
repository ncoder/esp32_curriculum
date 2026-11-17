#!/usr/bin/env python3
"""Draws every lesson's circuit diagrams from lessons/*/circuits.py.

For each circuit it writes two pictures into the lesson's diagrams/ folder:
  NAME.schematic.svg    the formal circuit diagram
  NAME.breadboard.svg   what it looks like on the two breadboards
and checks that both pictures make the same connections, and that every pin the
lesson's sketches use is wired.

Usage:
  .venv/bin/python tools/draw_circuits.py           # all lessons
  .venv/bin/python tools/draw_circuits.py L05 L06   # only matching lessons
  .venv/bin/python tools/draw_circuits.py --check   # check only, write nothing
  .venv/bin/python tools/draw_circuits.py --list    # list the circuits and their parts
"""
import argparse
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from circuits import Circuit  # noqa: E402
from circuits.check import check_sketches, compare  # noqa: E402


def load(lesson_dir):
    Circuit.registry.clear()
    runpy.run_path(str(lesson_dir / "circuits.py"), run_name="circuits_" + lesson_dir.name.replace("-", "_"))
    return list(Circuit.registry)


def write_if_changed(path, text):
    if path.exists() and path.read_text() == text:
        return False
    path.write_text(text)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filters", nargs="*", help="only lessons whose folder contains one of these")
    ap.add_argument("--check", action="store_true", help="only check, don't write pictures")
    ap.add_argument("--list", action="store_true", help="list circuits and parts")
    args = ap.parse_args()

    lessons = sorted(p.parent for p in (ROOT / "lessons").glob("*/circuits.py"))
    if args.filters:
        lessons = [d for d in lessons if any(f in d.name for f in args.filters)]
    failed = 0
    names = set()
    for d in lessons:
        try:
            circuits = load(d)
        except Exception as e:  # show which lesson broke, then the error
            print(f"FAIL  {d.name}/circuits.py: {e}")
            failed += 1
            continue
        out = d / "diagrams"
        for c in circuits:
            if c.name in names:
                print(f"FAIL  {d.name}: two circuits are called {c.name}")
                failed += 1
            names.add(c.name)
            try:
                problems = compare(c) + check_sketches(c, d)
            except Exception as e:  # a schematic that can't be drawn
                problems = [f"{type(e).__name__}: {e}"]
            if args.list:
                parts = ", ".join(f"{p.ref} ({p.label})" for p in c.parts.values() if p.kind != "esp32")
                print(f"{c.name}: {c.title}\n    {parts}")
            if problems:
                failed += 1
                print(f"FAIL  {c.name}")
                for p in problems:
                    print("      " + p)
                continue
            if args.check:
                print(f"ok    {c.name}")
                continue
            out.mkdir(exist_ok=True)
            changed = write_if_changed(out / f"{c.name}.breadboard.svg", c.breadboard_svg())
            changed |= write_if_changed(out / f"{c.name}.schematic.svg", c.schematic.svg())
            print(f"{'wrote' if changed else 'ok   '} {c.name}")
    if failed:
        print(f"{failed} problem(s).")
        sys.exit(1)


if __name__ == "__main__":
    main()
