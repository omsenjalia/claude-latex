#!/usr/bin/env python3
"""Guard against AI remarks and added content in a reproduction.

  check_fidelity.py OUT.tex [--pdf OUT.pdf] [--source SRC.pdf | --source-text SRC.txt]

1. Forbidden phrases: scans the .tex (visible text and % comments) and the compiled
   PDF text for AI/meta remarks ("reconstructed", "the source", "illegible", ...).
   A phrase is allowed only if it also occurs in the source text.
2. Vocabulary diff (needs a typed source with a text layer, or --source-text):
   lists words that appear in the output PDF but never in the source. Each one must
   be a legitimate transcription or be removed.
3. Metadata: flags AI/tool names in PDF metadata.

Exit code 1 if any forbidden phrase or metadata problem is found.
"""
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

FORBIDDEN = [
    r"\bthe source\b", r"\bsource'?s\b", r"\bsource (?:method|form|treatment|text|document|material)\b",
    r"\boriginal (?:source|notes|document|sequence|text)\b",
    r"\breconstruct\w*", r"\btranscri(?:bed|ption|be)\b", r"\btypeset by\b",
    r"\b(?:ai|llm)[- ]generated\b", r"\bgenerated (?:by|with|using)\b",
    r"\bclaude\b", r"\bchatgpt\b", r"\bopenai\b", r"\banthropic\b", r"\blanguage model\b",
    r"\billegible\b", r"\bunclear\b", r"\bunreadable\b", r"\bverify\b", r"\bpresumably\b",
    r"\bappears to (?:be|read)\b", r"\bassum(?:ed|ing) (?:that )?the\b", r"\[sic\]",
    r"\bclarity improved\b", r"\bfor (?:clarity|completeness)\b", r"\bare retained\b",
    r"\bpreserves? the\b", r"\bkey takeaways?\b", r"\bacademic notes\b",
    r"\bnote:", r"\bremark:", r"\btip:",
    r"\bhandwritten\b",
]

STOP = set("a an the and or of to in on is are be by for with as at it its this that then "
           "if we let so from into than which where when hence thus".split())


def pdf_text(path):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz
    d = fitz.open(path)
    return "\n".join(p.get_text() for p in d), d.metadata


def tex_visible_text(tex):
    """Rough visible text of a .tex: drop preamble, maths and command names."""
    body = tex.split(r"\begin{document}", 1)[-1]
    body = re.sub(r"(?<!\\)%.*", " ", body)
    body = re.sub(r"\\begin\{(lstlisting|verbatim)\}.*?\\end\{\1\}", " ", body, flags=re.S)
    body = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]|\$.*?\$", " ", body, flags=re.S)
    body = re.sub(r"\\(?:begin|end)\{[^}]*\}", " ", body)
    body = re.sub(r"\\[a-zA-Z@]+\*?", " ", body)
    return body


def tex_comments(tex):
    return "\n".join(m.group(0) for m in re.finditer(r"(?<!\\)%.*", tex.split(r"\begin{document}", 1)[-1]))


def norm(s):
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)  # re-join words hyphenated across lines
    return re.sub(r"\s+", " ", s.replace("\u2019", "'")).lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--pdf")
    ap.add_argument("--source", help="source PDF (typed, with text layer)")
    ap.add_argument("--source-text", help="plain-text transcription of the source")
    a = ap.parse_args()

    tex = open(a.tex, encoding="utf-8", errors="replace").read()
    src = ""
    if a.source:
        src, _ = pdf_text(a.source)
    elif a.source_text:
        src = open(a.source_text, encoding="utf-8", errors="replace").read()
    src_n = norm(src)

    targets = {".tex visible text": tex_visible_text(tex), ".tex comments": tex_comments(tex)}
    meta = {}
    out_pdf_text = ""
    if a.pdf:
        out_pdf_text, meta = pdf_text(a.pdf)
        targets["PDF text"] = out_pdf_text

    bad = 0
    print("== forbidden phrases ==")
    for where, text in targets.items():
        t = norm(text)
        for pat in FORBIDDEN:
            for m in re.finditer(pat, t):
                if src_n and re.search(pat, src_n):
                    continue  # the source itself says it
                ctx = t[max(0, m.start() - 50):m.end() + 50]
                print(f"  [{where}] '{m.group(0)}'  …{ctx}…")
                bad += 1
    print(f"  {bad} found" if bad else "  none")

    print("== metadata ==")
    meta_bad = 0
    for k, v in (meta or {}).items():
        if v and re.search(r"claude|anthropic|chatgpt|openai|\bai\b|generated", str(v), re.I):
            print(f"  {k}: {v}")
            meta_bad += 1
    print("  ok" if not meta_bad else f"  {meta_bad} problem(s)")

    if src_n and out_pdf_text:
        print("== words in output that never occur in the source ==")
        src_words = set(re.findall(r"[a-z]{3,}", src_n))
        extra = sorted({w for w in re.findall(r"[a-z]{3,}", norm(out_pdf_text))
                        if w not in src_words and w not in STOP})
        print("  " + (", ".join(extra) if extra else "none"))
        if extra:
            print("  -> each must be a genuine transcription (e.g. text inside a figure); otherwise remove it")

    sys.exit(1 if (bad or meta_bad) else 0)


if __name__ == "__main__":
    main()
