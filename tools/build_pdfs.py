#!/usr/bin/env python3
"""Builds the printable student handouts (one PDF per lesson) from lessons/*/lesson.md.

Each lesson.md starts with YAML front matter (title, parts, plan, ...) followed by
Markdown. A line containing only `@sketch NAME` is replaced by the exact contents
of the sketch NAME/NAME.ino from that lesson folder, so the handout always shows
the same code that the compile check builds.

Usage:
  .venv/bin/python tools/build_pdfs.py            # all lessons + combined book
  .venv/bin/python tools/build_pdfs.py L03 L04    # only matching lessons
  .venv/bin/python tools/build_pdfs.py --html     # also keep the HTML (for debugging)
  .venv/bin/python tools/build_pdfs.py --paper a4
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
import yaml
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

ROOT = Path(__file__).resolve().parent.parent
LESSONS = ROOT / "lessons"
OUT = ROOT / "handouts"
CSS = ROOT / "tools" / "handout.css"
MAX_CODE_LINE = 72  # longer lines wrap on paper and are hard to copy

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chromium-browser", "msedge",
]

FORMATTER = HtmlFormatter(style="arduino", nowrap=True)
LEXER = get_lexer_by_name("arduino")
BOX = '<span class="box"></span>'


def find_chrome():
    for c in CHROME_CANDIDATES:
        p = shutil.which(c) or (c if Path(c).exists() else None)
        if p:
            return p
    sys.exit("Could not find Chrome/Chromium/Edge to print PDFs.")


def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("lesson.md must start with --- front matter ---")
    return yaml.safe_load(m.group(1)), text[m.end():]


def code_block(source, name):
    warnings = [
        f"{name}: line {i} is {len(line)} chars (max {MAX_CODE_LINE})"
        for i, line in enumerate(source.splitlines(), 1) if len(line) > MAX_CODE_LINE
    ]
    body = highlight(source.rstrip("\n") + "\n", LEXER, FORMATTER)
    n = source.rstrip("\n").count("\n") + 1
    cls = "sketch keep" if n <= 45 else "sketch"
    return (
        f'<div class="{cls}"><div class="sketch-head">'
        f'<span>Type this in &rarr; save it as <b>{html.escape(name)}</b></span>'
        f'<span class="lines">{n} lines</span></div>'
        f'<pre class="code">{body}</pre></div>'
    ), warnings


def expand_sketches(md, lesson_dir):
    warnings = []

    def repl(m):
        name = m.group(1)
        hits = list(lesson_dir.rglob(f"{name}/{name}.ino"))
        if len(hits) != 1:
            raise FileNotFoundError(f"{lesson_dir.name}: sketch {name} not found (or ambiguous)")
        block, w = code_block(hits[0].read_text(), name)
        warnings.extend(w)
        # Raw HTML blocks must be separated by blank lines for Markdown to leave them alone.
        return f"\n\n{block}\n\n"

    md = re.sub(r"^@sketch\s+(\S+)\s*$", repl, md, flags=re.M)
    # "@lines 3" (may be indented, e.g. inside a callout) -> 3 ruled lines to write on.
    md = re.sub(r"^(\s*)@lines\s+(\d+)\s*$",
                lambda m: m.group(1) + '<span class="answer"></span>' * int(m.group(2)), md, flags=re.M)
    return md, warnings


def render_md(md):
    out = markdown.markdown(
        md,
        extensions=["tables", "fenced_code", "codehilite", "admonition", "attr_list", "md_in_html", "sane_lists"],
        extension_configs={"codehilite": {"css_class": "code", "pygments_style": "arduino", "guess_lang": False}},
    )
    # Checkboxes: "[ ]" anywhere (lists, table cells) becomes a printable tick box.
    return out.replace("[ ]", BOX)


def inline(text):
    return markdown.markdown(str(text)).removeprefix("<p>").removesuffix("</p>")


def cover(fm):
    num = int(fm["lesson"])
    parts = "".join(f"<li>{BOX}{inline(p)}</li>" for p in fm.get("parts", []))
    learn = "".join(f"<li>{inline(x)}</li>" for x in fm.get("learn", []))
    plan = "".join(
        f"<tr><td class='t'>{html.escape(str(p['time']))}</td><td>{inline(p['do'])}</td></tr>"
        for p in fm.get("plan", [])
    )
    return f"""
<header class="cover">
  <div class="badge"><small>LESSON</small>{num}</div>
  <div class="titles">
    <div class="kit">ESP32 Super Starter Kit &middot; 2-hour session</div>
    <h1>{html.escape(fm['title'])}</h1>
    <p class="tagline">{inline(fm.get('tagline', ''))}</p>
  </div>
</header>
<div class="namebar"><span>Name: ______________________________</span><span>Date: _______________</span></div>
<section class="overview">
  <div class="col"><h3>Today you will learn</h3><ul class="learn">{learn}</ul>
    <h3>Session plan</h3><table class="plan">{plan}</table></div>
  <div class="col"><h3>Parts to collect</h3><ul class="parts">{parts}</ul></div>
</section>
"""


def lesson_html(lesson_dir):
    fm, body = split_front_matter((lesson_dir / "lesson.md").read_text())
    body, warnings = expand_sketches(body, lesson_dir)
    footer = f"Lesson {int(fm['lesson'])}: {fm['title']}"
    article = f'<article class="lesson" data-footer="{html.escape(footer)}">{cover(fm)}{render_md(body)}</article>'
    return fm, article, warnings


def page(title, articles, paper, footer):
    css = CSS.read_text().replace("__PAPER__", paper).replace("__FOOTER__", footer.replace('"', "'"))
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{css}</style></head><body>{''.join(articles)}</body></html>"""


def print_pdf(chrome, html_text, pdf_path, keep_html):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "page.html"
        src.write_text(html_text)
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={tmp}/profile",
             "--virtual-time-budget=2000", f"--print-to-pdf={pdf_path}", src.as_uri()],
            check=True, capture_output=True,
        )
        if keep_html:
            shutil.copy(src, pdf_path.with_suffix(".html"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filters", nargs="*", help="only build lessons whose folder contains one of these")
    ap.add_argument("--paper", default="letter", choices=["letter", "a4"])
    ap.add_argument("--html", action="store_true", help="keep the generated HTML next to each PDF")
    args = ap.parse_args()

    chrome = find_chrome()
    OUT.mkdir(exist_ok=True)
    dirs = sorted(d for d in LESSONS.iterdir() if (d / "lesson.md").exists())
    if args.filters:
        dirs = [d for d in dirs if any(f in d.name for f in args.filters)]

    articles, all_warnings = [], []
    for d in dirs:
        fm, article, warnings = lesson_html(d)
        all_warnings += warnings
        articles.append(article)
        pdf = OUT / f"{d.name}.pdf"
        footer = f"Lesson {int(fm['lesson'])}: {fm['title']}"
        print_pdf(chrome, page(fm["title"], [article], args.paper, footer), pdf, args.html)
        print(f"wrote {pdf.relative_to(ROOT)}")

    if not args.filters and articles:
        book = OUT / "ESP32-Curriculum-All-Lessons.pdf"
        print_pdf(chrome, page("ESP32 Curriculum", articles, args.paper, "ESP32 Super Starter Kit Curriculum"), book, args.html)
        print(f"wrote {book.relative_to(ROOT)}")

    for w in all_warnings:
        print("warning:", w)


if __name__ == "__main__":
    main()
