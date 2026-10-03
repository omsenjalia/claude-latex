#!/usr/bin/env python3
"""Install the claude-latex skill into ~/.claude/skills/claude-latex (overwrites).

Also writes .source_repo into the installed copy so the skill's learning script
(scripts/learn.py) can save new lessons back into this repository. The installed
copy's state/ folder (per-user series settings from scripts/series.py) is preserved.
"""
import os
import shutil
import tempfile

repo = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(repo, "skills", "claude-latex")
dst = os.path.join(os.path.expanduser("~"), ".claude", "skills", "claude-latex")

kept = None
if os.path.isdir(os.path.join(dst, "state")):
    kept = os.path.join(tempfile.mkdtemp(), "state")
    shutil.copytree(os.path.join(dst, "state"), kept)
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".source_repo", "state"))
if kept:
    shutil.copytree(kept, os.path.join(dst, "state"))
with open(os.path.join(dst, ".source_repo"), "w", encoding="utf-8") as f:
    f.write(repo)
print("installed ->", dst)
