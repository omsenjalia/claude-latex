#!/usr/bin/env python3
"""Compile a .tex file with whatever TeX engine is installed.

  build.py OUT.tex [--engine pdflatex|xelatex|lualatex] [--keep-aux]

Order of preference: latexmk -> <engine> run twice -> tectonic.
claudelatex.sty is copied next to the .tex if missing or older than the skill's copy.
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


TEX_DIRS = [  # used when the TeX bin dir is not on PATH (e.g. freshly installed MiKTeX)
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64"),
    r"C:\Program Files\MiKTeX\miktex\bin\x64",
    "/Library/TeX/texbin", "/usr/local/texlive/bin/x86_64-linux",
]


def find(tool):
    hit = shutil.which(tool)
    if hit:
        return hit
    for d in TEX_DIRS:
        hit = shutil.which(tool, path=d)
        if hit:
            return hit
    return None


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
    local_sty = os.path.join(cwd, "claudelatex.sty")
    if os.path.exists(STY) and (not os.path.exists(local_sty)
                                or os.path.getmtime(STY) > os.path.getmtime(local_sty)):
        shutil.copy2(STY, cwd)
        print("copied latest claudelatex.sty next to", name)

    flags = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error"]
    engine = find(a.engine)
    if engine and "miktex" in engine.lower():
        flags.append("--enable-installer")  # MiKTeX: fetch missing packages on the fly
    code, out = None, ""
    latexmk = find("latexmk")
    if latexmk and (shutil.which("perl") or "miktex" not in latexmk.lower()):
        mode = {"pdflatex": "-pdf", "xelatex": "-xelatex", "lualatex": "-lualatex"}[a.engine]
        code, out = run([latexmk, mode, *flags, name], cwd)
    if (code is None or code) and engine:  # no/failed latexmk -> run the engine directly
        for _ in range(2):
            code, out = run([engine, *flags, name], cwd)
            if code:
                break
    elif code is None and find("tectonic"):
        code, out = run([find("tectonic"), "--keep-logs", name], cwd)
    if code is None:
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
