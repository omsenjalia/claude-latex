# Layout Replication

Goal: the output should feel like the same document, re-typeset. Use the source's
own page furniture — and nothing else.

---

## Reference look (from the typed BVM Mathematics-I tutorials)

These typed handouts are the visual target for `replicate` mode:

```
                Birla Vishvakarma Mahavidyalaya            ← \Large\bfseries
             (An Autonomous Engineering Institution)       ← \large, upright
                    AY: 2026–27 (Odd Semester)             ← \large
                    101BS: Mathematics - I                 ← \large\bfseries
                         Tutorial – 1                      ← \large\bfseries
      LIST OF FREQUENTLY USED SYMBOLS AND FORMULAE         ← \large\bfseries, all caps

Greek Alphabet                                              ← \section* (bold, \Large)
   [boxed tabular with vertical rules]

Polar Co-ordinates
                       x = r cos θ                          ← centred display maths
...
──────────────────────────────────────────────────────────── ← footer rule
AY2026–27 ODD SEMESTER          1           Dr. N C Sonara   ← footer: L / C / R
                                            Course Coordinator
```

- Paper A4, ~1 in side margins, Computer Modern at 12 pt (`\documentclass[12pt]{article}`).
- Section headings unnumbered (`\section*`) in bold; question headings like
  `Q-2 Do as directed: [A]` are also `\section*`.
- Equation numbers on the right in parentheses, only on the lines the source numbers.
- Some pages carry a thin rule at the very top (header rule, empty header text):
  `\SetHeaderRule{0.4pt}`.

`templates/handout.tex` reproduces this; change the strings to match each source.

---

## Rules

1. **Title block** — copy every line of the source's title block, same order, same
   wording, same capitalisation, same dash characters (– vs -). Use `\TitleBlock{...}`.
   Do not create a title block if the source has none.
2. **Headers/footers** — copy exactly what the source prints. Text that is merely cut
   off by the page edge or a bad scan (e.g. a footer clipped to `…ODD SEMESTE`) is a
   rendering artefact: use the full text the same footer shows on other pages.
   Use `\SetFooter{left}{right}` (centre is always the page number) and
   `\SetHeader{left}{right}`. A source with no header/footer → `\pagestyle{plain}`
   (page number only) for notes from handwriting, or `\pagestyle{empty}` if the source
   has no page numbers at all and the user doesn't want them.
3. **Page numbers** — style as the source: bare `1`, not `1 / 9`, not `Page 1`.
4. **Numbering** — reproduce the source's numbering exactly: `(I)…(VI)`, `(11)`,
   `Q-1`, `1.`, `(a)`. Use `\tag{}` and `enumitem` labels; never let LaTeX auto-number
   things the source didn't number.
5. **Headings** — same wording; same level hierarchy. Handwritten underlined headings →
   `\section*`/`\subsection*`; boxed headings → `\fbox` only if boxed in the source.
6. **Order** — never reorder content. Page breaks may move; content order may not.
7. **Columns** — two-column source → `multicols`; side-by-side formulas → `\qquad`
   spacing on one display line like the source.
8. **Emphasis** — bold/italic/underline/colour only where the source uses it. Colour in
   handwritten notes (red heading, blue text) may be kept with `xcolor` if the user wants
   a colour-faithful copy; default is black like the typed references.

## Notes mode (handwritten / scanned sources)

- `templates/notes.tex`: `article`, 11 or 12 pt, A4, footer = centred page number only.
- Title: the author's own title from the first page (if any), centred bold. No subtitle,
  no "notes" label, no date, no author unless written.
- Each worked problem: problem line as written (with the author's own label, e.g. `Ex.`,
  `Q.`, `①`), then the steps as displayed maths in the author's order.
- Ruled-paper lines, margins, page holes, doodles of no content → dropped.
