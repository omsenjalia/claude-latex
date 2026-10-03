# Colour Theme

`\usepackage[color]{claudelatex}` (on by default, see CONFIG in SKILL.md) gives every template
the same consistent colour language. Colour is **styling only**: it never adds words. The
same `.tex` without `color` prints cleanly in black and white, because every semantic
command falls back to plain text.

## What gets coloured automatically
| Element | Colour |
|---|---|
| Title block (`\TitleBlock`) | blue, with a light-blue rule under it |
| `\section*` | blue, with a light-blue underline rule |
| `\subsection*` | teal |
| `\subsubsection*` | purple |
| Code listings | syntax colours (mauve keywords, teal types, green strings, grey comments, magenta `#include`) on a faint grey background |
| Program output | pale green box |
| Labels in practical files (`\clLabel`: number, Solution:, Output:, Flowchart) | magenta, bold |
| Flowchart shapes | filled per type: Start/Stop green, input/output blue, process yellow, decision orange, connector violet |
| Table header row (`\TableHead` at the start of the row) | light blue |

## Semantic highlighting (you apply it, sparingly)
| Command / environment | Colour | Use it for |
|---|---|---|
| `\important{...}` | yellow highlighter | the key statement or result of a passage, or text the source itself stresses (underlined, starred, boxed, "Note", "Important") |
| `\definition{...}` | orange highlighter | the defining sentence of a term ("... is called ...", "... is defined as ...") |
| `\keyterm{...}` | bold dark orange | the term being defined, inside its definition |
| `formulabox` | light blue box | key formulas and standard results (rules, theorems, standard expansions) |
| `defbox` | orange left bar | a full definition paragraph (source labels it "Definition", or it clearly is one) |
| `keybox` | yellow left bar | a rule, theorem or important note as a block |
| `answerbox` | green box | a final answer or result (instead of `\boxed`) |

## Rules
1. **Never add text.** Boxes have no titles unless the source prints that heading. Don't
   write "Definition", "Important" or "Key formula" labels yourself.
2. **Same meaning, same colour, everywhere.** Yellow always means important, orange always
   means definition. Never colour by taste.
3. **Sparingly.** Use at most 3–4 highlights per page and never highlight whole paragraphs.
   If everything is highlighted, nothing is.
4. **Highlight what the source signals.** Its definitions, rules and theorems, the formulas
   it boxes or numbers, the result lines it states, and anything it underlines, stars or
   marks as important. Don't invent importance.
5. **Math inside highlighters goes in braces:** `\important{the area is {$\pi r^2$}}`. Put
   display maths in `formulabox` instead of `\important`.
6. **Print-friendly.** All fills are light. Never put white text on dark fills.
7. **Black and white on request.** If the user asks for black and white (or a faithful
   copy of a B/W handout's look), drop `color`. The highlight commands then print plain.

## Example
```latex
\begin{defbox}
\definition{An \keyterm{indeterminate form} is a limit of the type $\frac{0}{0}$ whose
value cannot be found by direct substitution.}
\end{defbox}

\begin{formulabox}
\[ \lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)} \]
\end{formulabox}

\begin{answerbox}
\[ \lim_{x\to 0}\frac{3x^{2}+6\cos x-6}{x^{4}}=\frac14 \]
\end{answerbox}
```
