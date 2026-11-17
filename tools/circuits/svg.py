"""A tiny SVG writer that works in breadboard pitches and tracks the drawing's size."""
import math
from contextlib import contextmanager
from html import escape

FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"


def _f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Svg:
    def __init__(self, scale=10.0):
        self.s = scale            # SVG user units per pitch
        self.out = []
        self.stack = [(1, 0, 0, 1, 0, 0)]   # affine transforms, for size tracking
        self.box = [math.inf, math.inf, -math.inf, -math.inf]
        self.upright = 0.0        # extra text rotation that keeps labels readable in turned parts

    # ---------- size tracking ----------
    def _grow(self, x, y):
        a, b, c, d, e, f = self.stack[-1]
        X, Y = a * x + c * y + e, b * x + d * y + f
        self.box = [min(self.box[0], X), min(self.box[1], Y), max(self.box[2], X), max(self.box[3], Y)]

    def _grow_rect(self, x, y, w, h):
        for px, py in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
            self._grow(px, py)

    @contextmanager
    def g(self, translate=(0, 0), rotate=0.0, opacity=None):
        tx, ty = translate
        r = math.radians(rotate)
        cos, sin = math.cos(r), math.sin(r)
        a, b, c, d, e, f = self.stack[-1]
        # current * translate * rotate
        e2, f2 = a * tx + c * ty + e, b * tx + d * ty + f
        a2, b2 = a * cos + c * sin, b * cos + d * sin
        c2, d2 = -a * sin + c * cos, -b * sin + d * cos
        self.stack.append((a2, b2, c2, d2, e2, f2))
        attrs = f' transform="translate({_f(tx * self.s)},{_f(ty * self.s)}) rotate({_f(rotate)})"'
        if opacity is not None:
            attrs += f' opacity="{opacity}"'
        self.out.append(f"<g{attrs}>")
        try:
            yield
        finally:
            self.out.append("</g>")
            self.stack.pop()

    # ---------- shapes (all in pitches) ----------
    def _style(self, fill="none", stroke=None, sw=0.1, opacity=None, dash=None, cap=None, join=None):
        st = f' fill="{fill}"'
        if stroke:
            st += f' stroke="{stroke}" stroke-width="{_f(sw * self.s)}"'
        if opacity is not None:
            st += f' opacity="{opacity}"'
        if dash:
            st += f' stroke-dasharray="{" ".join(_f(v * self.s) for v in dash)}"'
        if cap:
            st += f' stroke-linecap="{cap}"'
        if join:
            st += f' stroke-linejoin="{join}"'
        return st

    def rect(self, x, y, w, h, fill="none", rx=0.0, **kw):
        self._grow_rect(x, y, w, h)
        s = self.s
        self.out.append(
            f'<rect x="{_f(x * s)}" y="{_f(y * s)}" width="{_f(w * s)}" height="{_f(h * s)}" '
            f'rx="{_f(rx * s)}"{self._style(fill, **kw)}/>')

    def circle(self, cx, cy, r, fill="none", **kw):
        self._grow_rect(cx - r, cy - r, 2 * r, 2 * r)
        s = self.s
        self.out.append(f'<circle cx="{_f(cx * s)}" cy="{_f(cy * s)}" r="{_f(r * s)}"{self._style(fill, **kw)}/>')

    def ellipse(self, cx, cy, rx, ry, fill="none", **kw):
        self._grow_rect(cx - rx, cy - ry, 2 * rx, 2 * ry)
        s = self.s
        self.out.append(
            f'<ellipse cx="{_f(cx * s)}" cy="{_f(cy * s)}" rx="{_f(rx * s)}" ry="{_f(ry * s)}"{self._style(fill, **kw)}/>')

    def line(self, x1, y1, x2, y2, stroke="#000", sw=0.1, cap="round", **kw):
        self._grow(x1, y1)
        self._grow(x2, y2)
        s = self.s
        self.out.append(
            f'<line x1="{_f(x1 * s)}" y1="{_f(y1 * s)}" x2="{_f(x2 * s)}" y2="{_f(y2 * s)}"'
            f'{self._style("none", stroke=stroke, sw=sw, cap=cap, **kw)}/>')

    def poly(self, pts, fill="none", closed=True, **kw):
        for x, y in pts:
            self._grow(x, y)
        tag = "polygon" if closed else "polyline"
        p = " ".join(f"{_f(x * self.s)},{_f(y * self.s)}" for x, y in pts)
        self.out.append(f'<{tag} points="{p}"{self._style(fill, **kw)}/>')

    def path(self, cmds, fill="none", **kw):
        """cmds: list like [("M", x, y), ("Q", cx, cy, x, y), ("L", x, y), ("Z",)] in pitches."""
        parts = []
        for cmd in cmds:
            op, nums = cmd[0], cmd[1:]
            for i in range(0, len(nums), 2):
                self._grow(nums[i], nums[i + 1])
            parts.append(op + " ".join(_f(n * self.s) for n in nums))
        self.out.append(f'<path d="{" ".join(parts)}"{self._style(fill, **kw)}/>')

    def text(self, x, y, s, size=0.7, fill="#222", anchor="middle", weight="normal", rotate=0, family=FONT,
             baseline="central", style="normal"):
        w = 0.55 * size * len(str(s))
        if rotate in (90, -90, 270):
            self._grow_rect(x - size / 2, y - w / 2, size, w)
        else:
            x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
            self._grow_rect(x0, y - size / 2, w, size)
        k = self.s
        rotate = (rotate + self.upright) % 360
        if rotate > 180:
            rotate -= 360
        rot = f' transform="rotate({_f(rotate)} {_f(x * k)} {_f(y * k)})"' if rotate else ""
        self.out.append(
            f'<text x="{_f(x * k)}" y="{_f(y * k)}" font-family="{family}" font-size="{_f(size * k)}" '
            f'font-weight="{weight}" font-style="{style}" fill="{fill}" text-anchor="{anchor}" '
            f'dominant-baseline="{baseline}"{rot}>{escape(str(s))}</text>')

    def raw(self, text):
        self.out.append(text)

    # ---------- output ----------
    def render(self, margin=1.0, title=None):
        x0, y0, x1, y1 = self.box
        x0, y0, x1, y1 = x0 - margin, y0 - margin, x1 + margin, y1 + margin
        s = self.s
        vb = f"{_f(x0 * s)} {_f(y0 * s)} {_f((x1 - x0) * s)} {_f((y1 - y0) * s)}"
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
                f'width="{_f((x1 - x0) * s)}" height="{_f((y1 - y0) * s)}">')
        if title:
            head += f"<title>{escape(title)}</title>"
        return head + "".join(self.out) + "</svg>\n"
