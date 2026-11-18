# Writing a lesson

Every lesson lives in `lessons/LNN-short-name/`:

```
lessons/L05-rainbow-colors/
  lesson.md                 student handout source (becomes handouts/L05-rainbow-colors.pdf)
  NOTES.md                  teacher notes: prep, common problems, quiz answers
  circuits.py               the lesson's circuits (see circuits.md)
  diagrams/                 schematic + breadboard pictures drawn from circuits.py
  L05_Fade/L05_Fade.ino     sketches students type (shown in the handout)
  L05_Mixer/L05_Mixer.ino
  solutions/L05_Disco/L05_Disco.ino   challenge solutions (repo only, not in the handout)
```

[L01-hello-esp32](../lessons/L01-hello-esp32) is the reference lesson; copy its style.

## lesson.md

The file starts with YAML front matter: `lesson`, `title`, `tagline`, `learn`
(3–5 bullets), `parts` (with quantities), and `plan` (a list of `{time, do}`
entries covering 0:00–2:00, with a short break around the 1-hour mark).

The body then has numbered `##` sections. Most lessons follow this shape:
idea → wiring → sketch → how it works → try it → next sketch → challenges →
quiz → tidy up.

Special syntax:

| Write | You get |
|---|---|
| `@sketch L05_Fade` on its own line | The full contents of `L05_Fade/L05_Fade.ino` in a "type this in" box |
| `@circuit L05_rgb` on its own line | The circuit diagram and breadboard picture of that circuit, side by side |
| `@lines 2` | Two ruled lines to write an answer on (can be indented inside a callout) |
| `[ ]` | A tick box, in lists or in table cells |
| `!!! tip "Title"` | Green box. Other kinds: `info` (big idea), `warning`, `challenge`, `question` |

Wiring goes in a table with a `✓` column of `[ ]` boxes and *From → To* columns,
followed by `@circuit NAME` for the pictures. Describe each circuit in the
lesson's `circuits.py`: see [circuits.md](circuits.md).

## Sketches students type

- Students type every line, so keep sketches **short**: aim for ≤ 45 lines,
  and never over 70. Lines must be **≤ 72 characters**; the PDF build warns
  otherwise.
- Use only a 2-line header comment and a few short inline comments. The
  explaining happens in the handout's "How it works" tables.
- Use simple Arduino C: `const int` pin names, `int`/`float`/`bool`/`String`,
  arrays, `if`, `for`, `while`, and small functions. Avoid pointers, classes,
  lambdas, `#define` constants and clever tricks.
- Use `Serial.begin(115200)`, 2-space indent, and the pins from
  [hardware-notes.md](hardware-notes.md).
- Folder name = file name = the name students save as (`L05_Fade`).
- Target the esp32 core 3.x: use `analogWrite`, `tone`/`noTone`, or
  `ledcAttach(pin, freq, bits)` + `ledcWrite(pin, duty)`. Never use
  `ledcSetup`/`ledcAttachPin`, which were removed in 3.x.
- Libraries must be in [libraries.txt](../libraries.txt). The handout tells
  students how to install them with **Tools → Manage Libraries…**.

## Check your work

```
make -j6 check LESSON=L05   # compile this lesson's sketches
make circuits LESSON=L05    # draw its circuits, and check them against each other and the sketches
make pdfs LESSON=L05        # build its handout
```

Open the PDF and check that the code boxes don't split awkwardly and that the
handout runs about 4–7 pages.

## Appendices

`appendix/A-wiring-guide/` follows the same layout as a lesson, with `appendix: A`
in the front matter instead of `lesson:` (no `learn`, `parts` or `plan`). It builds
to `handouts/A-wiring-guide.pdf` and comes after Lesson 21 in the combined book.

Appendix A lists every part in the kit and points to the lesson section that shows
it wired up. **When you add or move a lesson's wiring picture, update its table.**
A part that no lesson shows simply gets its own section there.
