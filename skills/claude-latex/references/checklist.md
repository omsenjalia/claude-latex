# Self-Verification Checklist (mandatory before delivering)

Run every item. Fix failures yourself — do not present a PDF with a known failure.

## A. Automated
- [ ] `python scripts/build.py OUT.tex` → exit 0, PDF produced, no `Undefined control sequence`,
      no missing figures, no `??` references.
- [ ] `python scripts/check_fidelity.py OUT.tex --pdf OUT.pdf [--source SRC.pdf]` →
      **0 forbidden phrases**; every "word not in source" explained or removed.
- [ ] Rendered every output page (`pdftool.py render OUT.pdf DIR`) and looked at each one.

## B. Nothing added
- [ ] No header/footer text the source doesn't print.
- [ ] No closing note, colophon, footnote, watermark, date, or "generated/reconstructed" label.
- [ ] No sentence mentions "the source", "original", "handwritten", "as written", etc.
- [ ] No explanations, connective sentences, extra steps, extra examples, summaries, hints,
      answers that the source doesn't contain.
- [ ] No invented numbering (Definition 1.1, Example 1.2, section numbers, equation numbers).
- [ ] No `%` comments in the .tex expressing doubts or describing the process.
- [ ] No absolute paths in the .tex (`\input`, `\includegraphics`). Use paths relative to the
      .tex, because machine paths can leak user/tool names.
- [ ] Notes or extra text appear only when the user asked for them, worded as they asked.
- [ ] PDF metadata (title/author/creator/producer) contains no AI/tool names.

## C. Nothing lost
- [ ] Block count per page matches the brief's inventory; every block present, in order.
- [ ] Every title-block line, heading, question, sub-question, tag (`[A]`, `[E]`, `(CO : 1)`) present.
- [ ] Every equation present with all terms; equation numbers identical.
- [ ] Every table: same rows × columns, every cell identical.
- [ ] Every program: character-for-character identical (compare line by line).
- [ ] Every figure/circuit/graph present (redrawn exactly or cropped).

## D. Exactness spot-checks (do at least these)
- [ ] Signs (±, −) and exponents on every derivation line.
- [ ] Limit subscripts (`x→0`, `x→0+`, `x→π/2`, `x→∞`).
- [ ] Factorials, indices, summation bounds, intervals like `(−∞, ∞)`, `(−1, 1]`.
- [ ] Greek letters (ϵ vs ε, ϕ vs φ — match the source glyph), degree signs.
- [ ] Code: `&`, `*`, `%d`, `\n`, `;`, `{}`, `<>`, indentation.
- [ ] Circuit: component values, units, polarities, diode/transistor orientation.

## E. Colour (when COLOR is on)
- [ ] Highlights mean the same thing everywhere (yellow = important, orange = definition,
      blue box = formula, green box = answer); at most 3–4 highlights per page.
- [ ] No box or highlight carries a title or label the source doesn't print.
- [ ] Everything stays readable in greyscale (light fills only).

## F. Typography
- [ ] Nothing overflows the margins or is clipped; no overfull lines visible on the page.
- [ ] Display maths centred, multi-step derivations aligned at `=`.
- [ ] Fonts: Computer/Latin Modern throughout (unless xelatex was required).
- [ ] Page size A4 (unless source differs).

## G. Delivery
- [ ] Deliver PDF (+ .tex + assets).
- [ ] Chat reply lists doubts/illegible spots (or says there were none). The PDF does not.
