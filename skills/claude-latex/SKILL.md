---
name: claude-latex
description: Turn any source PDF or image (typed handouts, tutorials, question papers, handwritten notes, scanned pages, slides, pages with photos/figures, circuit diagrams, C/other programs, tables, graphs, flowcharts) into a clean, faithfully typeset LaTeX PDF that contains ONLY the source's own content — no AI remarks, no "reconstructed" labels, no added explanations. Use whenever the user asks to convert, retype, typeset, recreate, reconstruct, digitise or "make a LaTeX PDF of" a document or notes.
---

# claude-latex — Source-Faithful LaTeX PDF Builder

Converts a user-supplied document into a LaTeX-typeset A4 PDF that looks like
a professionally typeset academic handout (Computer Modern / Latin Modern
fonts, centred title block, numbered equations, ruled tables, clean footer).

The output is a **transcription in better typography**, never a rewrite.

---

## CONFIG — defaults for every run (user can override per request)

```
DEFAULT_MODE:    auto        # auto | replicate | notes
                             #  replicate = mirror the source's own layout (typed PDFs)
                             #  notes     = clean article layout (handwritten/scanned/messy sources)
                             #  auto      = replicate if the source is typed, notes otherwise
PAPER:           a4paper     # never US Letter unless the source is Letter
ENGINE:          pdflatex    # xelatex/lualatex only if the source needs Unicode scripts/fonts
FONT:            Computer Modern (pdflatex default) — matches the reference handouts
ONE_FILE_PER_SOURCE: true    # one .tex/.pdf per source file unless the user asks to merge
```

---

## THE PRIME DIRECTIVE — SOURCE CONTENT ONLY (read before anything else)

The PDF must contain **only what is in the source**, in the source's order.
Every visible character on the output page must be traceable to the source.
This rule overrides every other instinct to "help".

```
NEVER PUT ANY OF THIS IN THE PDF:
- Running headers/footers the source does not have
  ✗ "Reconstructed academic notes"   ✗ "AI-generated notes"   ✗ "Typeset by Claude"
- Colophons / closing footnotes about how the document was made
  ✗ "Reconstructed from the supplied handwritten academic source; original sequence,
     notation, methods, examples, and recorded results are retained, with mathematical
     typesetting and clarity improved."
- Meta-commentary that talks ABOUT the source
  ✗ "as in the source method"        ✗ "Applying L'Hospital's rule in the source's form"
  ✗ "The source does not state the domain/branch restrictions…"
  ✗ "The calculation below preserves the source's differentiation path."
  ✗ "This is an ∞/∞-type form in the source treatment."
- Disclaimers, caveats, uncertainty flags: ✗ "[illegible]" ✗ "(verify)" ✗ "unclear in original"
  ✗ "assumed" ✗ "Note:" / "Remark:" / "Tip:" / "Key takeaway" boxes the source does not have
- Added teaching: explanations, intuition, extra steps, extra examples, summaries,
  practice questions, answers the source does not give, "Hence"/"Therefore"/"Applying…"
  connective sentences the source does not write
- Invented structure: section numbers, "Definition 1.1"/"Example 1.2" numbering,
  subtitles, a title page, a table of contents — unless the source has them
- Dates (\today), PDF metadata naming an AI tool, watermarks
```

```
WHAT IS ALLOWED (typography only, never content):
- Typesetting: proper fractions, limits, matrices, aligned derivations, tables, code
  listings, vector redraws of diagrams — the same content rendered cleanly.
- Fixing pure transcription artefacts (OCR noise, smudges, a stray pen stroke) so the
  typeset text says what the author actually wrote.
- Layout decisions: page breaks, spacing, equation alignment, figure placement.
- Boxing a final answer ONLY if the source boxes/underlines/highlights it.
```

**Where uncertainty goes:** anything illegible, ambiguous, or apparently wrong in
the source is transcribed best-effort *as written* and reported to the user in the
chat reply (page + location + what you chose). It is **never** written into the PDF,
never into a LaTeX comment that could leak, and never "corrected" silently.
If the source contains a mathematical mistake, keep the source's version.

---

## SELF-LEARNING LOOP (every run)

This skill improves itself across sessions through `references/lessons.md`, its memory,
managed with `scripts/learn.py`.

**Before you start:** run `python scripts/learn.py list` and apply every active lesson.
They are rules that aren't in the main docs yet, and they override defaults.

**While working, notice learning signals:**
- **correction:** the user asks you to change something you produced (spacing, layout,
  naming, wording, a missing element). This is the strongest signal; always record it.
- **check:** `check_fidelity.py`, the build, or your visual check caught a problem.
- **self:** you hit a non-obvious problem and found the fix (a TeX error, a tool quirk, a
  layout trick that worked).

**After delivering:** record each new general lesson:
```bash
python scripts/learn.py add --area layout --trigger correction \
  --lesson "One-sentence imperative rule" \
  --why "What went wrong or what the user asked for" \
  --apply "Exactly what to do next time"
```
- `add` recognises a lesson that's already recorded and raises its `seen` count instead of
  duplicating it.
- When a lesson reaches **seen ≥ 3**, or the user states it as a standing preference, promote
  it: write it into this file, the right reference, or the script that should enforce it
  automatically. Then run `python scripts/learn.py promote L<n> --to <file>`, and
  `python install.py` from the repo if you changed scripts.
- Lessons are saved to the installed skill and committed locally in the source repo
  (found through `.source_repo`). **Never push** unless the user asks.
- Never record document contents, personal data, names or paths from the user's files.
  Record only the reusable rule.
- Tell the user in one line what was learned (e.g. "Learned: keep pattern tables centred
  (L9)"). Don't put it in the PDF.

---

## WORKFLOW FOR CLAUDE

0. **Load lessons:** `python scripts/learn.py list`. Apply them.

1. **Inspect the source** with `scripts/pdftool.py` (needs `pip install pymupdf`):
   ```bash
   python scripts/pdftool.py info   SOURCE.pdf            # pages, size, fonts, text layer?, images
   python scripts/pdftool.py render SOURCE.pdf OUTDIR --dpi 110   # PNG per page → read each one
   python scripts/pdftool.py text   SOURCE.pdf            # text layer (typed PDFs only)
   ```
   - **Always look at every page image**, even when a text layer exists — the text layer
     scrambles fractions, limits, superscripts and tables (e.g. `x2` for x², `∞\n∑\nn=0`).
     The image is the ground truth; the text layer is only a spelling aid.
   - Images (.png/.jpg) of pages: read them directly.
   - Classify each page: typed / handwritten / scanned / slide; and list its content
     blocks (headings, prose, equations, tables, code, figures, circuits, graphs).

2. **Pick the mode** (CONFIG `auto` rule) and the template:
   - `templates/handout.tex` — replicate a typed institutional handout/tutorial/question
     paper (title block, footer with left text / page no. / right text).
   - `templates/notes.tex` — clean notes from handwritten/scanned material. Header and
     footer carry only the source's own title (or nothing) and the page number.
   - Both use `templates/claudelatex.sty`; copy it next to the `.tex` file.
   - Delete the template's instructional `%` comments and every unused `<...>` line in
     the output file — the delivered `.tex` must be as clean as the PDF.
   - Worked example of the finished result: `../../examples/maclaurin-tutorial-2.tex`
     (replicate) and `../../examples/lhospital-notes.tex` (notes).
   - Before typesetting, fill in `references/prompt-template.md` (block inventory) privately.

3. **Transcribe block by block, in source order.** Use the matching snippet from
   `templates/snippets/` and the rules in `references/content-types.md`:
   math → `derivation.tex`, tables → `table.tex`, C/other code → `code-c.tex`,
   circuits → `circuit.tex`, graphs → `graph.tex`, flowcharts → `flowchart.tex`,
   photos/irreproducible figures → `figure-from-source.tex`, question lists → `questions.tex`.

4. **Replicate layout faithfully** (`references/layout-replication.md`): same headings and
   their wording/capitalisation, same numbering scheme ((1), (I), Q-1, 1., a)…), same
   equation numbers, same marks/tags like `[A]`, `[E]`, `(CO : 1)`, same header/footer text,
   same column structure. Page breaks may differ from the source; content order may not.

5. **Build:** `python scripts/build.py OUTPUT.tex` (auto-detects latexmk / pdflatex /
   xelatex / tectonic; runs twice for references). Fix every error and every overfull
   box that visibly clips content.

6. **Verify — mandatory, before presenting:**
   ```bash
   python scripts/check_fidelity.py OUTPUT.tex --pdf OUTPUT.pdf [--source SOURCE.pdf]
   python scripts/pdftool.py render OUTPUT.pdf CHECKDIR --dpi 110
   ```
   - `check_fidelity.py` must report **0 forbidden phrases**. With `--source` (typed
     sources) it also lists output words that never occur in the source — every one must
     be a legitimate transcription (e.g. a word only present in a figure) or be removed.
   - Look at every rendered output page next to the matching source page and confirm:
     every number, sign, exponent, subscript, limit, table cell and code character
     matches; nothing is missing; nothing was added; no text overflows the margin.
   - Then run `references/checklist.md` end to end. Fix failures; do not hand them off.

7. **Deliver:** the `.pdf` (and the `.tex` + any extracted image assets). The chat
   reply may list illegible/ambiguous spots and choices made — the PDF may not.

8. **Learn:** record every correction, failed check or hard-won fix with
   `scripts/learn.py add`, and promote lessons that are ready (see SELF-LEARNING LOOP).
   Do this again whenever the user corrects a delivered file.

---

## SOLUTIONS / PRACTICAL FILES (user asks for programs, outputs, flowcharts)

When the user gives programming practicals and asks for **solutions**, follow
`references/practical-files.md`. In short:
- Format: `[number] statement` → `Solution:` (program) → `Output:` (real run).
- **One program per page, sized to fill the page** with `scripts/practicals.py`. Code and
  output never split across pages.
- Use the compiler style the user names (e.g. Turbo C: `conio.h`, `void main()`, `clrscr()`,
  `getch()`). Always use proper code spacing (`for (i = 1; i <= n; i++)`, `sum = sum + i`).
- **Compile and run every program**, and paste the real output with the typed input shown.
- If a statement has a typo, report it and ask. Fix it (statement and program) only once
  the user agrees.
- If asked, add flowcharts on a separate page after each program, scaled to fill the page.
  Build them with `scripts/flowgen.py` (loops, nested loops, if/else). Add notes (e.g. "for
  learning purposes only") only when the user asks, then run the checker with `--allow`.
- Save as `Practical <n> - <heading>.pdf`, with the sources in `sources/practical-<n>/`.

---

## SOURCE-TYPE PLAYBOOK (summary — details in `references/content-types.md`)

| Source content            | How to reproduce                                                                 |
|---------------------------|----------------------------------------------------------------------------------|
| Typed handout / tutorial  | `handout.tex`, replicate title block, footer, numbering, equation numbers        |
| Handwritten notes         | `notes.tex`; transcribe the author's words exactly; typeset the maths cleanly    |
| Scanned / photographed    | Same as handwritten; ignore paper texture, shadows, punch holes, margins         |
| Equations & derivations   | `amsmath` (`align*`, `\lim\limits`, `\dfrac`); keep the source's step order      |
| Tables                    | `tabular` with the source's rules (vertical lines only if the source has them)   |
| C / C++ / Java / Python   | `listings`, verbatim — identical whitespace, names, braces, comments, output     |
| Program output shown      | separate `verbatim`/`lstlisting` block styled as output, exact text              |
| Circuit diagrams          | Redraw with `circuitikz` (same components, values, labels, node names)           |
| Graphs / plots            | `pgfplots`/`tikz` redraw with the same axes, labels, ticks, curves               |
| Flowcharts / block diag.  | `tikz` shapes + arrows, same labels and branch text                              |
| Photos, screenshots, maps, complex art | crop from source with `pdftool.py crop`/`images` and `\includegraphics` |
| Chemistry structures      | `chemfig` / `mhchem`                                                             |
| Slides                    | one `\section*` (or frame-like block) per slide, slide titles verbatim           |

Redraw vector-style diagrams when you can reproduce them **exactly**; if a redraw would
lose or alter information (dense, artistic, photographic, or partly illegible), embed a
crop of the source instead. Never invent a label, value or component to complete a figure.

---

## FILES IN THIS SKILL

```
SKILL.md                         ← this file (rules + workflow)
references/fidelity-rules.md     ← the prime directive in depth, with right/wrong examples
references/content-types.md      ← per-content-type transcription rules
references/layout-replication.md ← how to mirror headers, footers, title blocks, numbering
references/prompt-template.md    ← fill-in brief Claude writes for itself before typesetting
references/checklist.md          ← self-verification checklist (mandatory)
references/lessons.md            ← the skill's memory: active + promoted lessons (read first)
references/practical-files.md    ← solutions to programming practicals: page-filling layout,
                                   Turbo C style, real outputs, flowchart pages
templates/claudelatex.sty        ← shared preamble (packages, footer/title helpers, code style)
templates/handout.tex            ← typed institutional handout layout
templates/notes.tex              ← clean notes layout for handwritten/scanned sources
templates/snippets/*.tex         ← ready blocks: derivation, table, code-c, circuit, graph,
                                   flowchart, figure-from-source, questions
scripts/pdftool.py               ← info / render / text / images / crop for source PDFs
scripts/build.py                 ← compile with whatever TeX engine is installed
scripts/check_fidelity.py        ← blocks AI remarks; diffs vocabulary against the source
scripts/learn.py                 ← list / add / seen / promote / stats lessons (self-learning)
scripts/practicals.py            ← JSON spec → one-program-per-page lab file (+ flowchart pages)
scripts/flowgen.py               ← block list (io/process/loop/if/ifelse) → TikZ flowchart
scripts/flowchart_examples.py    ← hand-written flowcharts for cases flowgen can't express (break)
```
