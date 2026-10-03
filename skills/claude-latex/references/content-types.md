# Content-Type Rules

Each section: **what to preserve** → **how to typeset** → **pitfalls**.
Snippets live in `../templates/snippets/`.

---

## Prose / plain text
- Preserve: wording, spelling, capitalisation, punctuation, bold/italic/underline,
  list markers and their style (`1.`, `(i)`, `(a)`, `•`, `★`), indentation levels.
- Typeset: normal paragraphs; `enumerate` with `enumitem` labels matching the source
  (`label=(\roman*)`, `label=\alph*)`, `label=Q-\arabic*`); `\textbf`, `\emph`, `\underline`.
- Pitfalls: do not merge two source paragraphs or split one; do not convert a list
  into prose or prose into a list; do not "fix" grammar.

## Mathematics
- Preserve: every symbol, sign, exponent, subscript, bound, the order of steps, which
  steps are shown, equation numbers, labels like `(0/0 form)`, roman markers `(I)`.
- Typeset:
  - Display maths `\[ … \]`; multi-step chains `align*` aligned at `=`; numbered
    equations with `\tag{11}` when the source shows the number, so numbers match exactly.
  - Limits `\lim\limits_{x\to 0}`; fractions `\dfrac` in display, `\frac` inline (as the
    source shows it); `\sqrt[3]{}`; `\sum\limits_{n=0}^{\infty}`; `\log`, `\sin`,
    `\sinh`, `\tan^{-1}`; derivatives `f'`, `f''`, `f'''`, `f^{(n)}` exactly as written.
  - Side annotations the source writes beside a step: `\quad\text{(0/0 form)}`.
  - Boxed/underlined final answers only if the source boxes/underlines them (`\boxed{}`).
  - Matrices: `pmatrix`/`bmatrix`/`vmatrix` matching the bracket type in the source.
- Pitfalls: text-layer garbage (`x2` → x², `∞\n∑\nn=0`, `m̸ = 0` → m ≠ 0, `f n(0)` →
  f^{n}(0) as printed — keep the author's notation even if unconventional); missing
  minus signs; `log` vs `ln` (use what the source uses); degree signs `44^\circ`.

## Tables
- Preserve: number of rows/columns, header text, cell text, merged cells, rule
  placement (vertical lines only where the source has them), alignment.
- Typeset: `tabular` + `array`; `\multicolumn`/`\multirow` for merges; `\hline` /
  booktabs rules matching the source look; maths cells in `$…$`.
- Long tables: `longtable` (keeps the header on each page).
- Pitfalls: re-ordering rows "alphabetically"; adding a header row that is not there.

## Programs (C, C++, Java, Python, assembly, SQL, shell …)
- Preserve: **every character** — identifiers, indentation (spaces vs tabs as they look),
  blank lines, braces placement, comments, string literals, format specifiers (`%d`,
  `%.2f`, `\n`), `#include <stdio.h>`, `&`, `*`, `->`, semicolons, line numbers if shown.
- Typeset: `lstlisting` with `style=srccode` from `claudelatex.sty` (`language=C` etc.);
  sample output in a separate `lstlisting` with `style=srcoutput`.
- Pitfalls: do NOT fix bugs, rename variables, add `return 0;`, modernise `void main()`,
  add comments, or reflow long lines. If a line is too long, use `breaklines=true`
  (shows a continuation arrow) rather than editing it.
- Handwritten code: transcribe what is written; ambiguous characters (`l`/`1`, `O`/`0`,
  `;`/`:`) resolved by language syntax, and listed in the chat reply if still doubtful.

## Pseudocode (algorithm logic, not compilable code)
- Preserve: every line, keyword, capitalisation and **indentation depth** (indentation is
  how pseudocode shows nesting, so make each level a clear step), and line numbers only if
  the source numbers its lines.
- Typeset: `snippets/pseudocode.tex` (`style=pseudocode`): no frame, normal ink, bold
  control keywords (IF/THEN/ELSE, WHILE, FOR, REPEAT/UNTIL, RETURN, PROCEDURE/FUNCTION...).
  No language syntax colouring. It's read like a derivation, not run like code.
- If the source uses `algorithmic`-style layout with `←` arrows, keep `$\gets$`.

## Exam / provenance labels
- Labels the source attaches to a question or example, like `(Winter 2012)`, `GTU Dec-19`,
  `[GATE 2015]` or `(5 marks)`, are content. Copy them exactly, in the same place, with the
  same wording and format. Never standardise, add or remove them, and never add exam-
  relevance tags of your own.

## UI / UX / design sources
- Screenshots, mockups, colour swatches and real UI images: crop them from the source
  (`figure-from-source.tex`).
- Schematic wireframes, user-flow diagrams and component anatomy drawn in the source:
  redraw with `tikz` (rectangles, pill-shaped buttons, lines for text, arrows) only if it
  can be reproduced exactly; otherwise crop. Keep every annotation label verbatim.
- Typography scales and palettes: reproduce the listed values exactly (`#2D6CDF`,
  `H1 — 32px Bold`) as a table if the source tabulates them.

## Circuit diagrams
- Preserve: every component (R, C, L, sources, diodes, BJTs/MOSFETs, op-amps, gates,
  switches, ground, meters), its label and value (`R_1 = 10\,\text{k}\Omega`), node
  names, current/voltage arrows and polarities, the topology (what connects to what).
- Typeset: `circuitikz` (`\usepackage[circuits]{claudelatex}`), redraw on a grid that
  follows the source's geometry; logic gates via `circuitikz` IEEE/US shapes.
- Pitfalls: changing component orientation that changes meaning (diode direction,
  source polarity, transistor type); adding labels; "simplifying" topology.
  If any part is unreadable → embed a crop of the source instead of guessing.

## Graphs and plots
- Preserve: axes, axis labels, tick values, curves and their shapes/intercepts/asymptotes,
  marked points and their labels, shading, legends.
- Typeset: `pgfplots` when the function is given (plot the same function on the same
  domain); `tikz` for sketches (match key points, not invented precision).
- Pitfalls: adding a grid, legend, or title that the source doesn't have.

## Flowcharts / block diagrams / trees / state machines
- Preserve: every box, its shape (terminal, process, decision, I/O), text, arrow
  direction, branch labels (`Yes`/`No`, `T`/`F`), layout direction.
- Branch labels exactly as the source writes them (`Yes/No`, `True/False`, `T/F`);
  `flowgen.flowchart(..., branch=("True", "False"))`. No step numbers inside shapes unless
  the source has them. Long labels wrap inside the shape, never overflow.
- Typeset: `scripts/flowgen.py` for program-style charts; otherwise `tikz` with the
  `flowchart` styles from `snippets/flowchart.tex`;
  automata via `tikz` `automata` library; trees via `forest` or `tikz` trees.

## Images, photos, screenshots, hand sketches that can't be redrawn exactly
- `python scripts/pdftool.py images SOURCE.pdf OUTDIR` → embedded raster images.
- `python scripts/pdftool.py crop SOURCE.pdf PAGE x0 y0 x1 y1 OUT.png --dpi 300` →
  crop a region (coordinates in PDF points, origin top-left; read them off a render).
- Typeset with `snippets/figure-from-source.tex`; caption only if the source has one.
- For image-file sources (.jpg/.png), crop with Python/Pillow at full resolution.

## Chemistry
- `\ce{}` (mhchem) for formulas/reactions; `chemfig` for structures.

## Question papers / tutorials / assignments
- Preserve question numbers, sub-numbering, marks (`[5]`), tags (`[A]`, `[E]`, `CO 1`),
  "Do as directed", "OR" separators, instructions block.
- Use `snippets/questions.tex`. Never add answers or hints.

## Slides
- One block per slide; slide title verbatim as `\section*{}` or bold heading; bullets
  verbatim; slide images cropped. Do not add slide numbers unless the slides show them.

## Mixed languages / non-Latin scripts
- Switch `ENGINE` to xelatex and use `fontspec` + `polyglossia`/`babel` with a font
  that contains the script. Keep the text exactly as written.
