# claude-latex

A Claude skill that turns any source document into a clean, LaTeX-typeset PDF that
contains **only the source's own content**: no AI remarks, no "reconstructed"
labels, no added explanations.

It works with typed handouts, tutorials and question papers, handwritten or scanned
notes, slides, and pages that contain images, circuit diagrams, C (or other) programs,
tables, graphs, flowcharts or chemistry.

## Layout

```
skills/claude-latex/
  SKILL.md                      rules + step-by-step workflow (entry point)
  references/
    fidelity-rules.md           source-content-only rule, with real failures to avoid
    content-types.md            maths, tables, code, circuits, graphs, flowcharts, images…
    layout-replication.md       title blocks, headers/footers, numbering
    prompt-template.md          block-inventory brief Claude fills in before typesetting
    checklist.md                mandatory self-verification
  templates/
    claudelatex.sty             shared preamble (\TitleBlock, \SetFooter, code/circuit styles)
    handout.tex                 typed institutional handout layout
    notes.tex                   handwritten/scanned notes layout
    snippets/                   derivation, table, code-c, circuit, graph, flowchart,
                                figure-from-source, questions
  scripts/
    pdftool.py                  info / render / text / images / crop for source PDFs
    build.py                    compile with latexmk / pdflatex / xelatex / tectonic
    check_fidelity.py           flags AI remarks + words not present in the source
examples/
  maclaurin-tutorial-2.tex      replicate mode (typed tutorial)
  lhospital-notes.tex           notes mode (no header label, no colophon, no invented numbering)
```

## Install the skill

Claude Code (personal skills folder):

```bash
python install.py
```

This copies `skills/claude-latex` to `~/.claude/skills/claude-latex`. Run it again after
you change the skill. On claude.ai, zip the `skills/claude-latex` folder and upload it under
Settings → Capabilities → Skills.

## Requirements

- Python 3 with PyMuPDF: `pip install pymupdf`
- A TeX distribution: MiKTeX, TeX Live, or Tectonic. On Windows, MiKTeX installs
  missing packages automatically.

## Use

Ask Claude something like *"Convert this PDF to LaTeX"* or *"Typeset these handwritten
notes"* and attach the file. The skill:

1. Renders and reads every source page.
2. Picks a layout: **replicate** for typed sources, **notes** for handwritten or scanned ones.
3. Copies every block in the source's order.
4. Compiles the PDF and runs `check_fidelity.py`.
5. Compares each output page with the matching source page.

If part of the source is illegible or ambiguous, Claude says so in the chat. Nothing about
it is written into the PDF.

## Check any PDF for AI remarks

```bash
python skills/claude-latex/scripts/check_fidelity.py out.tex --pdf out.pdf --source source.pdf
```
