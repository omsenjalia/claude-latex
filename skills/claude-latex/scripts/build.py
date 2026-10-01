#!/usr/bin/env python3
"""Compile a .tex file with whatever TeX engine is installed.

  build.py OUT.tex [--engine pdflatex|xelatex|lualatex] [--keep-aux]

Order of preference: latexmk -> <engine> run twice -> tectonic.
claudelatex.sty is copied next to the .tex automatically if it is missing.
Exit code 0 only if a PDF was produced without fatal errors.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STY = os.path.join(HERE, "..", "templates", "claudelatex.sty")
AUX_EXT = (".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz", ".xdv")


def run(cmd, cwd):
    print("$", " ".join(cmd))
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace")
    return p.returncode, p.stdout + p.stderr


def report_log(log_path):
    if not os.path.exists(log_path):
        return
    with open(log_path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    issues = [l for l in lines if l.startswith("!") or "Overfull \\hbox" in l
              or "LaTeX Warning: Reference" in l or "not found" in l.lower()]
    if issues:
        print("\n--- issues from log ---")
        for l in issues[:40]:
            print(l)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--engine", default="pdflatex", choices=["pdflatex", "xelatex", "lualatex"])
    ap.add_argument("--keep-aux", action="store_true")
    a = ap.parse_args()

    tex = os.path.abspath(a.tex)
    cwd, name = os.path.split(tex)
    stem = os.path.splitext(name)[0]
    if not os.path.exists(os.path.join(cwd, "claudelatex.sty")) and os.path.exists(STY):
        shutil.copy(STY, cwd)
        print("copied claudelatex.sty next to", name)

    flags = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error"]
    code, out = None, ""
    if shutil.which("latexmk"):
        mode = {"pdflatex": "-pdf", "xelatex": "-xelatex", "lualatex": "-lualatex"}[a.engine]
        code, out = run(["latexmk", mode, *flags, name], cwd)
    elif shutil.which(a.engine):
        for _ in range(2):
            code, out = run([a.engine, *flags, name], cwd)
            if code:
                break
    elif shutil.which("tectonic"):
        code, out = run(["tectonic", "--keep-logs", name], cwd)
    else:
        sys.exit("No TeX engine found. Install one of: MiKTeX (winget install MiKTeX.MiKTeX), "
                 "TeX Live, or Tectonic (https://tectonic-typesetting.github.io).")

    report_log(os.path.join(cwd, stem + ".log"))
    pdf = os.path.join(cwd, stem + ".pdf")
    if code or not os.path.exists(pdf):
        print(out[-4000:])
        sys.exit(f"build failed (exit {code})")
    if not a.keep_aux:
        for ext in AUX_EXT:
            for f in glob.glob(os.path.join(cwd, stem + ext)):
                os.remove(f)
    print("PDF:", pdf)


if __name__ == "__main__":
    main()
