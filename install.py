#!/usr/bin/env python3
"""Install the claude-latex skill into ~/.claude/skills/claude-latex (overwrites)."""
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills", "claude-latex")
dst = os.path.join(os.path.expanduser("~"), ".claude", "skills", "claude-latex")
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
print("installed ->", dst)
