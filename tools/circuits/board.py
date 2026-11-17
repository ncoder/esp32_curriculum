"""Geometry of the classroom breadboard setup.

Two 400-point breadboards are clipped together along their long edges: board
**A** on top, board **B** below. The ESP32 lies across the join with its USB
socket to the left: its top row of pins sits in row **j** of board A and its
bottom row in row **a** of board B, in columns 1-19 (see docs/hardware-notes.md).

All coordinates are in breadboard pitches (0.1 inch). x grows to the right,
y grows downwards. Column c of either board is at x = c.

Hole names
----------
``A:c12``   board A, row c, column 12 (rows a-j, columns 1-30)
``A:+12``   board A's outer **+** rail (the top edge), next to column 12
``A:-12``   board A's outer **-** rail
``B:+12``   board B's outer **+** rail (the bottom edge)
``B:-12``   board B's outer **-** rail
``A:bp12``  explicit rail names: tp/tn = top +/- , bn/bp = bottom -/+ .
            A's bottom rails and B's top rails lie under the ESP32 in columns
            1-19, but are free in columns 20-30.

A rail name without a column (``A:-``) in a wire means "the nearest free hole
on that rail".
"""
import re
from dataclasses import dataclass

ROWS_AE = "abcde"
ROWS_FJ = "fghij"
ROW_Y = {
    "tp": 1.0, "tn": 2.0,
    "a": 4.0, "b": 5.0, "c": 6.0, "d": 7.0, "e": 8.0,
    "f": 11.0, "g": 12.0, "h": 13.0, "i": 14.0, "j": 15.0,
    "bn": 17.0, "bp": 18.0,
}
RAILS = ("tp", "tn", "bn", "bp")
BOARD_H = 19.0
BOARD_Y0 = {"A": 0.0, "B": BOARD_H}
NCOLS = 30
BOARD_X0, BOARD_X1 = -0.6, NCOLS + 1.6
# Rail holes come in groups of 5, with a gap at columns 1, 7, 13, 19 and 25.
RAIL_COLS = [c for c in range(1, NCOLS + 1) if (c - 1) % 6 != 0]
SHORTHAND = {("A", "+"): "tp", ("A", "-"): "tn", ("B", "+"): "bp", ("B", "-"): "bn"}


@dataclass(frozen=True)
class Hole:
    board: str
    row: str
    col: int

    @property
    def xy(self):
        return (float(self.col), BOARD_Y0[self.board] + ROW_Y[self.row])

    @property
    def is_rail(self):
        return self.row in RAILS

    @property
    def strip(self):
        """Holes with the same strip are joined by the metal clip inside the board."""
        if self.is_rail:
            return ("rail", self.board, self.row)
        half = "ae" if self.row in ROWS_AE else "fj"
        return ("strip", self.board, half, self.col)

    def __str__(self):
        return f"{self.board}:{self.row}{self.col}"


@dataclass(frozen=True)
class Point:
    """A spot off the breadboard (a module's pin, a wire bend), in pitches."""
    x: float
    y: float

    @property
    def xy(self):
        return (self.x, self.y)


@dataclass(frozen=True)
class RailRef:
    """`A:-` with no column: resolved to the nearest free hole on that rail."""
    board: str
    row: str


HOLE_RE = re.compile(r"^([AB]):(tp|tn|bn|bp|[a-j]|[+-])(\d+)?$")


def parse_hole(text):
    m = HOLE_RE.match(text.replace("–", "-").replace("−", "-"))
    if not m:
        raise ValueError(f"not a hole name: {text!r}")
    board, row, col = m.group(1), m.group(2), m.group(3)
    row = SHORTHAND.get((board, row), row)
    if col is None:
        if row not in RAILS:
            raise ValueError(f"{text!r}: rows a-j need a column number")
        return RailRef(board, row)
    col = int(col)
    if not 1 <= col <= NCOLS:
        raise ValueError(f"{text!r}: columns are 1-{NCOLS}")
    if row in RAILS and col not in RAIL_COLS:
        raise ValueError(f"{text!r}: the rails have no hole at column {col} (gaps at 1, 7, 13, 19, 25)")
    return Hole(board, row, col)


def strip_holes(strip):
    kind = strip[0]
    if kind == "rail":
        _, board, row = strip
        return [Hole(board, row, c) for c in RAIL_COLS]
    _, board, half, col = strip
    rows = ROWS_AE if half == "ae" else ROWS_FJ
    return [Hole(board, r, col) for r in rows]


def all_holes():
    for board in "AB":
        for row in ROW_Y:
            cols = RAIL_COLS if row in RAILS else range(1, NCOLS + 1)
            for c in cols:
                yield Hole(board, row, c)
