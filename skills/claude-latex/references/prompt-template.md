# Typesetting Brief — fill this in (privately) before writing any LaTeX

Write this brief in your scratch space (not in the PDF, not shown as part of the PDF).
It forces a full inventory of the source so nothing is dropped and nothing is added.
Do not leave any `{PLACEHOLDER}` unfilled.

---

## CONFIG

```
SOURCE FILE:   {file name}
PAGES:         {n}
SOURCE KIND:   {typed | handwritten | scanned | slides | mixed}
MODE:          {replicate | notes}            # from SKILL.md CONFIG
ENGINE:        {pdflatex | xelatex}
PACKAGE OPTS:  \usepackage[{code,circuits,plots,flowcharts,chem}]{claudelatex}
OUTPUT NAME:   {same base name as source}.tex / .pdf
```

## PAGE FURNITURE (copy exactly; write NONE if absent)

```
TITLE BLOCK LINES:  {line 1 | line 2 | ...}
HEADER:             left={...}  right={...}  rule={yes/no}
FOOTER:             left={...}  centre=page number style {1 | i | none}  right={...}
```

## BLOCK INVENTORY (one row per block, in source order)

```
P{page}.{k}  TYPE={heading|prose|list|math|derivation|table|code|output|circuit|
                   graph|flowchart|figure-crop|questions|chem}
             CONTENT={verbatim text / formula / description of figure}
             NUMBERING={source's own label or "none"}
             SNIPPET={snippets/....tex}
             DOUBTS={none | what is illegible/ambiguous → goes to chat reply only}
```

Example rows (from the Maclaurin tutorial):

```
P1.1  TYPE=heading     CONTENT="Maclaurin's Series"            NUMBERING=none
P1.2  TYPE=prose       CONTENT="Statement: If f(x) is a given function of x which can be
                       expanded in positive ascending powers of x then"
P1.3  TYPE=math        CONTENT=f(x)=f(0)+xf'(0)+x^2/2! f''(0)+...+x^n/n! f^n(0)+...
P1.5  TYPE=math        CONTENT=e^x = 1+x+x^2/2!+x^3/3!+... = Σ_{n=0}^∞ x^n/n!, (−∞,∞)
                       NUMBERING="(I)"
```

## ADDITIONS CHECK

```
Lines I am adding that are not in the source:  NONE      ← must be NONE
Numbering I am inventing:                      NONE      ← must be NONE
Header/footer text not in the source:          NONE      ← must be NONE
```

## DOUBTS FOR THE CHAT REPLY

```
- {page, location, what you read, alternatives}
```
