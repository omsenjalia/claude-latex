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
      "statement_lines": 6,                           // optional: height of a table/pattern statement
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
the fc/* styles from claudelatex.sty) to a part; it is scaled to fill the page. For programs
with user-defined functions give a list, drawn side by side with titles:
  "flowchart": [{"title": "main()", "file": "fc/8_1_main.tex"},
                {"title": "oddEven(n)", "file": "fc/8_1_fn.tex"}]
Programs too long to share a page with their output at >= 9.5 pt get the output on the
next page ("<number> Output:"). Add a
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
SPLIT_BELOW_PT = 8.6  # if code+output would need the minimum font, output goes to the next page
MAX_CHART_SCALE = 1.5  # flowcharts fill the page but are never enlarged beyond this


def est_statement_height(text, extra, first, lines_hint=None):
    """lines_hint: rendered statement height in text lines (set "statement_lines" in the
    spec for tables/patterns/figures, whose LaTeX length says nothing about their height)."""
    if lines_hint and first:
        return lines_hint * 16.0 + (34.0 if extra else 0.0)
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
            stmt_h = est_statement_height(p["statement"], part.get("extra"), k == 0,
                                          p.get("statement_lines"))
            longest = max(len(l.expandtabs(4)) for l in lines)
            n_code, n_out = len(code.split("\n")), len(out.split("\n"))
            f, b, gap = fit(n_code, n_out, longest, stmt_h, heading)
            # Long program: keep the code on its page and move the output to the next page
            # instead of shrinking everything below a comfortable reading size.
            split_out = f < SPLIT_BELOW_PT and n_out > 2
            if split_out:
                f, b, gap = fit(n_code, 0, longest, stmt_h, heading)
                fo, bo, gapo = fit(0, n_out, longest, 0.0, None)

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
                  code, r"\end{lstlisting}"]
            if split_out:
                style = r"\fontsize{%s}{%s}\selectfont\ttfamily" % (fo, bo)
                o += [r"\clearpage", r"\noindent\textbf{%s%s %s}" % (p["number"], label, lab["output"]),
                      r"\par\vspace{6pt}"]
            else:
                o += [r"\vspace{%.1fpt}" % gap, r"\noindent\textbf{%s}" % lab["output"]]
            o += [r"\begin{lstlisting}[style=srcoutput,frame=single,framesep=6pt,basicstyle=%s]" % style,
                  out, r"\end{lstlisting}", ""]
            if part.get("flowchart"):
                rel = lambda pth: os.path.relpath(os.path.join(base, pth), os.path.dirname(
                    os.path.abspath(out_path))).replace("\\", "/")
                charts = part["flowchart"]
                o += [r"\clearpage",
                      r"\noindent\textbf{%s%s %s}" % (p["number"], label, lab["flowchart"]),
                      r"\par\vspace{12pt}",
                      r"\begin{center}"]
                if isinstance(charts, str):
                    # fill the page, but never blow a small chart up beyond 1.5x
                    o += [r"\sbox0{\input{%s}}%%" % rel(charts),
                          r"\pgfmathsetmacro\clSa{min(%s, \textwidth/\wd0, 0.84*\textheight/(\ht0+\dp0))}%%"
                          % MAX_CHART_SCALE,
                          r"\scalebox{\clSa}{\usebox0}"]
                else:
                    # several charts (main() + functions): TeX measures side-by-side and stacked
                    # layouts and keeps whichever can be drawn larger on the page
                    cells = [r"\begin{tabular}[t]{@{}c@{}}\textbf{\Large %s}\\[8pt]\input{%s}\end{tabular}"
                             % (c["title"], rel(c["file"])) for c in charts]
                    side = r"\begin{tabular}{@{}%s@{}}" % (r"c@{\hspace{1.5cm}}" * (len(cells) - 1) + "c") \
                        + " &\n".join(cells) + r"\end{tabular}"
                    stack = r"\begin{tabular}{@{}c@{}}" + r" \\[1cm]" "\n".join(cells) + r"\end{tabular}"
                    o += [r"\sbox0{%s}%%" % side,
                          r"\sbox2{%s}%%" % stack,
                          r"\pgfmathsetmacro\clSa{min(%s, \textwidth/\wd0, 0.84*\textheight/(\ht0+\dp0))}%%"
                          % MAX_CHART_SCALE,
                          r"\pgfmathsetmacro\clSb{min(%s, \textwidth/\wd2, 0.84*\textheight/(\ht2+\dp2))}%%"
                          % MAX_CHART_SCALE,
                          r"\ifdim\clSa pt>\clSb pt\scalebox{\clSa}{\usebox0}\else\scalebox{\clSb}{\usebox2}\fi"]
                o += [r"\end{center}",
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
