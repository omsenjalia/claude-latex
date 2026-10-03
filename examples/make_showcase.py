"""Generate the showcase flowchart with flowgen, then build both showcase PDFs."""
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
scripts = os.path.join(here, "..", "skills", "claude-latex", "scripts")
sys.path.insert(0, scripts)
from flowgen import flowchart  # noqa: E402

blocks = [
    ("io", "Read n"),
    ("process", "sum = 0"),
    ("loop", None, r"n $>$ 0 ?", [("process", r"r = n \% 10\\ sum = sum + r\\ n = n / 10")]),
    ("io", "Print sum"),
]
with open(os.path.join(here, "fc_showcase.tex"), "w", encoding="utf-8") as f:
    f.write(flowchart(blocks))

for name in ("showcase.tex", "showcase-bw.tex"):
    subprocess.run([sys.executable, os.path.join(scripts, "build.py"), os.path.join(here, name)], check=True)
