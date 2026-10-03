# Optional Extras (only when the user explicitly asks)

Everything here adds structure the source doesn't print, so none of it is used by default.
Use an extra only when the user asks for it by name (e.g. "add a cover page", "add a formula
sheet", "continue the page numbers from 9", "colour the code"). Even then, the rule
against new *content* still holds: extras rearrange or present the source's own material.
They never add explanations, tips, tags or practice questions unless the user asks for
exactly that.

---

## Cover page — `templates/snippets/cover.tex`
- Full A4 page, title at the true vertical and horizontal centre, no page number.
- Title text: the source's own topic/chapter title only. No lecture numbers, dates or
  "notes" labels unless the user gives them.
- Optional one-line subtitle, only if the user provides it or the source prints one.
- Typography only (large bold title). No decoration, sparkles or watermarks.
- The page numbering of the content starts after it (`\pagenumbering` handled by snippet).

## Formula / syntax quick-reference — `templates/snippets/quickref.tex`
- Title it as the user asks (default: `Formulas` or `Syntax`).
- List **every formula or syntax form that appears in the source**, including ones used
  quietly inside worked examples, each exactly as written in the source.
- Group them under the source's own section headings, in source order.
- No labels or descriptions that the source doesn't give. If the user wants a one-line
  meaning for each formula, that is a requested addition: write it plainly and accurately.
- Dense two-column layout (`multicols`) is fine; it's a scan-at-a-glance page.

## Continuous page numbering across a series — `scripts/series.py`
For a topic split over several source files (Lecture 1, 2, 3...), one output per source.
- **Page numbers continue across the series:** if the previous file ended at page 9, this
  one starts at 10 (`\setcounter{page}{10}`, or `"start_page": 10` in a practicals spec).
  Never print totals like "Page 4/12" or "X of Y".
- Content that repeats at the start of every lecture (a recap or intro) appears only in the
  first file of the series.
- Remember the series with `scripts/series.py set "<series>" --next-page N [--opt k=v ...]`
  and look it up with `series.py get "<series>"`, so the next run doesn't have to ask.
  State lives only in the user's installed skill and is never committed or pushed.
- In the chat reply, say which pages this file covers and where the next one starts.

## Colour syntax highlighting — `\usepackage[code,codecolor]{claudelatex}`
An editor-like palette tuned for printing on white paper:
- keywords: mauve
- types: teal
- strings and chars: green
- comments: grey italic
- preprocessor directives: magenta

Numbers stay in the body colour, because colouring digits would also recolour digits
inside names like `str1`. The default is black-and-white, which matches typed handouts. Use colour only when the
user wants it, or when the source's code is itself coloured.
