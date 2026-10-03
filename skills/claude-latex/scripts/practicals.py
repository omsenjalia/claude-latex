#!/usr/bin/env python3
"""Build a lab/practical-file document: one program per page, sized to fill the page.

  practicals.py SPEC.json OUT.tex

SPEC.json:
{
  "heading": "4\\quad Looping Statements",          // optional, printed on the first page
  "pdftitle": "Looping Statements",                 // optional
  "labels": {"solution": "Solution:", "output": "Output:"},   // optional
  "practicals": [
    {
      "number": "4.1",
      "statement": "Write a C program to ...",       // LaTeX, copied from the source
      "parts": [                                      // one page per part
        {"label": null, "code": "src/4_1.c", "language": "C",
         "output": "Enter the value of N: 10\\n..."}  // or "output_file": "out/4_1.txt"
      ]
    },
    {
      "number": "4.9",
      "statement": "Write a C program to evaluate ...",
      "parts": [
        {"label": "(i)",  "extra": "$\\displaystyle 1+\\frac12+\\cdots+\\frac1n$", "code": "...", "output": "..."},
        {"label": "(ii)", "extra": "...", "code": "...", "output": "..."}
      ]
    }
  ]
}

Optional flowchart page per part: add "flowchart": "fc/4_1.tex" (a bare tikzpicture using
the fc/* styles from claudelatex.sty) to a part; it is scaled to fill the page. Add a
top-level "flowchart_note": "..." to print a note at the bottom of every flowchart page
(only when the user asks for one).

Each part gets its own page. Page 1 of a practical shows "number statement"; later
parts repeat "number label". Font size and line spacing of the code/output are chosen
from the number of lines and the longest line so the page is filled but never overflows:
  - code font 9-12 pt, line spacing 1.2-1.6x, leftover height spread as gaps.
Paths in the spec are relative to the spec file.
"""
import json
import os
import sys

TEXT_HEIGHT = 680.0   # pt, A4 with claudelatex.sty margins (2.5cm top, 2.8cm bottom)
TEXT_WIDTH = 455.0    # pt, A4 with 2.5cm side margins
TT_CHAR = 0.525       # cmtt glyph width in em
STATEMENT_CHARS_PER_LINE = 80


def est_statement_height(text, extra, first):
    lines = max(1, -(-len(text) // STATEMENT_CHARS_PER_LINE)) if first else 1
    h = lines * 15.0
    if extra:
        h += 34.0 * extra.count("\\item") if "\\item" in extra else 34.0
    return h


def fit(code_lines, out_lines, longest, stmt_h, heading):
    overhead = 2 * 22.0 + 4 * 6.0 + stmt_h + (40.0 if heading else 0.0)
    avail = TEXT_HEIGHT * 0.94 - overhead
    n = code_lines + out_lines
    f_width = (TEXT_WIDTH - 16) / (TT_CHAR * max(longest, 1))
    f = min(12.0, f_width)
    s = avail / (n * f)
    if s < 1.2:                       # too long: shrink the font at 1.2x spacing
        f = max(8.5, avail / (n * 1.2))
        s = 1.2
    s = min(s, 1.6)
    used = n * f * s + overhead
    gap = max(6.0, min(36.0, (TEXT_HEIGHT * 0.94 - used) / 3))
    return round(f, 2), round(f * s, 2), round(gap, 1)


def main():
    spec_path, out_path = sys.argv[1], sys.argv[2]
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    lab = {"solution": "Solution:", "output": "Output:", "flowchart": "Flowchart",
           **spec.get("labels", {})}
    has_fc = any(part.get("flowchart") for p in spec["practicals"] for part in p["parts"])
    fc_note = spec.get("flowchart_note")

    o = [r"\documentclass[12pt]{article}",
         r"\usepackage[code%s]{claudelatex}" % (",flowcharts" if has_fc else ""),
         r"\usepackage{adjustbox}" if has_fc else "",
         r"\hypersetup{pdftitle={%s}}" % spec.get("pdftitle", ""),
         r"\pagestyle{plain}",
         r"\setlength{\parskip}{0pt}",
         r"\lstset{frame=single,framesep=6pt,aboveskip=4pt,belowskip=0pt}",
         "", r"\begin{document}", ""]
    first_page = True
    for p in spec["practicals"]:
        for k, part in enumerate(p["parts"]):
            code = open(os.path.join(base, part["code"]), encoding="utf-8").read().rstrip("\n")
            out = part.get("output")
            if out is None:
                out = open(os.path.join(base, part["output_file"]), encoding="utf-8").read()
            out = out.strip("\n")
            lines = code.split("\n") + out.split("\n")
            heading = spec.get("heading") if first_page else None
            stmt_h = est_statement_height(p["statement"], part.get("extra"), k == 0)
            f, b, gap = fit(len(code.split("\n")), len(out.split("\n")),
                            max(len(l.expandtabs(4)) for l in lines), stmt_h, heading)

            if not first_page:
                o.append(r"\clearpage")
            if heading:
                o += [r"\section*{%s}" % heading, ""]
            label = (" " + part["label"]) if part.get("label") else ""
            if k == 0:
                o.append(r"\noindent\textbf{%s} %s" % (p["number"], p["statement"]))
            else:
                o.append(r"\noindent\textbf{%s%s}" % (p["number"], label))
            if part.get("extra"):
                o.append(part["extra"])
            if k == 0 and label:
                o += [r"\par\vspace{%.1fpt}" % (gap / 2), r"\noindent\textbf{%s}" % part["label"].strip()]
            style = r"\fontsize{%s}{%s}\selectfont\ttfamily" % (f, b)
            o += [r"\par\vspace{%.1fpt}" % gap,
                  r"\noindent\textbf{%s}" % lab["solution"],
                  r"\begin{lstlisting}[language=%s,basicstyle=%s]" % (part.get("language", "C"), style),
                  code, r"\end{lstlisting}",
                  r"\vspace{%.1fpt}" % gap,
                  r"\noindent\textbf{%s}" % lab["output"],
                  r"\begin{lstlisting}[style=srcoutput,frame=single,framesep=6pt,basicstyle=%s]" % style,
                  out, r"\end{lstlisting}", ""]
            if part.get("flowchart"):
                fc = os.path.relpath(os.path.join(base, part["flowchart"]),
                                     os.path.dirname(os.path.abspath(out_path))).replace("\\", "/")
                o += [r"\clearpage",
                      r"\noindent\textbf{%s%s %s}" % (p["number"], label, lab["flowchart"]),
                      r"\par\vspace{12pt}",
                      r"\begin{center}",
                      r"\begin{adjustbox}{width=\textwidth,totalheight=0.84\textheight,keepaspectratio}",
                      r"\input{%s}" % fc,
                      r"\end{adjustbox}",
                      r"\end{center}",
                      r"\vfill"]
                if fc_note:
                    o.append(r"\noindent{\small\itshape %s}" % fc_note)
                o.append("")
            first_page = False
    o += [r"\end{document}", ""]
    open(out_path, "w", encoding="utf-8").write("\n".join(o))
    print("wrote", out_path)


if __name__ == "__main__":
    main()
