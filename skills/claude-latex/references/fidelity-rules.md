# Fidelity Rules — Source Content Only

The single most important property of the output: **a reader holding the source
and the PDF side by side finds the same content, nothing more, nothing less.**
The PDF is the source in better typography.

---

## 1. The test for every line you write

Before writing any visible text, ask: *"Where on which source page is this?"*

- If you can point to it → write it, in the source's wording.
- If you cannot → it does not go in the PDF. Mention it in chat if relevant.

This applies to headings, connective words ("Hence", "Therefore", "Applying…"),
labels ("Example 1.3"), captions, footers, and PDF metadata.

---

## 2. Real failures this skill exists to prevent

These all appeared in a previous AI-made PDF ("limits_lhospital_reconstructed.pdf").
None of them were in the handwritten source. **Never produce anything like them.**

| What appeared in the PDF | Why it is wrong |
|---|---|
| Running header: `Limits and L'Hospital's Rule … Reconstructed academic notes` | The source has no such header; "Reconstructed" is an AI remark |
| Final footnote: `Reconstructed from the supplied handwritten academic source; original sequence, notation, methods, examples, and recorded results are retained, with mathematical typesetting and clarity improved.` | A colophon about the AI's own process |
| `The source does not state the domain/branch restrictions needed to interpret this iterated-log expression over the reals.` | Commentary on the source |
| `The calculation below preserves the source's differentiation path.` | Commentary on the source |
| `Applying L'Hospital's rule repeatedly, as in the source method,` | Refers to "the source" |
| `Applying L'Hospital's rule in the source's form,` | Refers to "the source" |
| `This is an ∞/∞-type form in the source treatment.` | Refers to "the source" |
| `Definition 1.1`, `Example 1.2 … Example 1.21` | Numbering invented — only use numbering the source shows |
| Page footer `1 / 9` | "X / Y" counter not in the source — use the source's page-number style |

### Right vs wrong

Source (handwritten):  `lim x→0 (1−cos x) cot x  =  lim (1−cos x)/sin x · cos x = 0`

✗ Wrong:
```latex
\textbf{Example 1.11} Evaluate $\lim_{x\to0}(1-\cos x)\cot x$.
Rewrite ... Since $1-\cos x\to0$, $\sin x\sim x$, and $\cos x\to1$, ...
Hence, \boxed{0}.
```
✓ Right:
```latex
\[
\lim_{x\to 0}(1-\cos x)\cot x=\lim_{x\to 0}\frac{1-\cos x}{\sin x}\cdot\cos x=0
\]
```

---

## 3. Words that must never appear in the PDF (unless literally in the source)

`source`, `original`, `reconstructed`, `reconstruction`, `transcribed`, `transcription`,
`typeset by`, `generated`, `AI`, `Claude`, `ChatGPT`, `LLM`, `model`, `illegible`,
`unclear`, `verify`, `assumed`, `presumably`, `appears to`, `likely`, `[sic]`,
`note:`, `remark:`, `tip:`, `key takeaway`, `summary`, `clarity improved`,
`for completeness`, `for clarity`, `we preserve`, `retained`.

`scripts/check_fidelity.py` scans the `.tex` and the compiled PDF for these.
A hit is allowed only when the exact phrase occurs in the source itself
(e.g. the source genuinely says "Note:") — pass `--source` so the checker knows.

---

## 4. Handling problems in the source — always outside the PDF

| Situation | In the PDF | In the chat reply |
|---|---|---|
| Illegible word/symbol | Best-effort reading, typeset normally | "p.3, line 5: read as `cosh`, could be `cos h`" |
| Ambiguous notation | The most standard reading | Say which reading you chose |
| Apparent maths error by the author | Keep exactly as written | Point it out, offer a corrected version only if asked |
| Missing step the author skipped | Leave it skipped | Nothing (unless the user asks for explanations) |
| Unreadable figure region | Embed a crop of the source region | Mention it |
| Crossed-out text | Omit (author deleted it) | Mention only if it looked meaningful |
| Margin scribbles / doodles | Include only if they are content (a formula, a label) | — |

Do **not** write LaTeX `%` comments containing doubts either — the `.tex` is often
shared too. Keep the `.tex` as clean as the PDF.

---

## 5. Metadata

```latex
\hypersetup{pdftitle={<source title or empty>}, pdfauthor={<source author or empty>},
            pdfcreator={}, pdfproducer={}}
```
Never `\date{\today}`; never a title page unless the source has one.

---

## 6. Only if the user explicitly asks for additions

If the user explicitly asks for explanations, solutions, or extra material, add exactly
what they asked for — still never labelled as AI-made, and still without remarks about
"the source". Default is always: source content only.
