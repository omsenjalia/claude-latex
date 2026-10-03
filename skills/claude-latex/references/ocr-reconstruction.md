# OCR'd / Text-Extracted Sources

Use this when the source is an OCR'd Markdown/text file, or when a PDF's text layer is all
you have for part of a page. OCR damages notation in predictable ways. Repair what you are
confident about, transcribe the rest as written, and **report every repair in the chat
reply, never in the PDF.**

If the original page images exist, use them (`pdftool.py render`). The image is always the
ground truth, and these rules are only for when there is no image.

---

## 1. Symbol corruption (repair from context)

| OCR gave | Usually means | Notes |
|---|---|---|
| `x2`, `e x`, `a n` | x², eˣ, aⁿ | superscript lost its elevation |
| `xn`, `a1` in a sequence | xₙ, a₁ | subscript flattened |
| `ab` / `a b` where a ratio is expected | a/b as a stacked fraction | fraction bar dropped |
| `J`, `f` before `dx` | ∫ | integral sign |
| `E`, `Z` before an index range | Σ | summation |
| `TT`, `n` in a circle/trig context | π | pi |
| `x` between numbers | × | multiplication |
| `A` before a variable change | Δ | delta |
| `oo`, `00` as a limit | ∞ | infinity |
| `->`, `<=`, `>=`, `!=`, `m̸ =` | →, ≤, ≥, ≠ | arrows and relations |
| `lim x→0 f(x)` on one line | `\lim_{x\to 0} f(x)` | limit subscript collapsed |
| `∞ ∑ n=0` on separate lines | `\sum_{n=0}^{\infty}` | operator bounds scattered |

Use the surrounding steps to decide. If both readings are plausible, choose the more
standard one and list it in chat: `p.3, line 4: OCR "x2-y" -> x^2 - y (could be x - y^2)`.

## 2. Structural misreads (repair only when clearly wrong)

OCR also scrambles structure: `(a+b)/c` becomes `a+b/c` (lost brackets), an exponent lands
on the wrong base, a coefficient swaps places with a variable, or `x_n` becomes `xn`.

- Correct it only when the expression is clearly wrong in context, e.g. the next line of
  the derivation only follows from the corrected form.
- Never "fix" something that is unusual but valid. That is the author's choice; keep it.
- List every correction in chat: `Math correction: [OCR] -> [used]`.

## 3. Broken graphs and diagrams

OCR turns a figure into scattered axis labels, numbers, or nothing at all.

- If the page image exists, crop it (`pdftool.py crop`) or redraw it exactly.
- If not, redraw only what the surviving labels and nearby text establish: axes, labelled
  points, the curve's described shape. Never invent values.
- If nothing can be recovered, leave the gap, tell the user in chat, and ask for the
  original page. **Don't put a "[graph placeholder]" note in the PDF.**
- Never silently drop a figure or a formula. Repair it as best you can, or report it.
