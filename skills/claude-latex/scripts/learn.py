#!/usr/bin/env python3
"""The skill's memory: record, review and promote lessons learned while using it.

  learn.py list                       show active lessons (read these before every run)
  learn.py add  --area AREA --lesson "..." --why "..." --apply "..." [--trigger correction|check|self]
  learn.py seen ID                    the same lesson came up again (raises its count)
  learn.py promote ID --to FILE       the lesson is now a rule in FILE (references/... or scripts/...)
  learn.py stats                      lessons per area, and which are ready to promote

Lessons live in references/lessons.md. Writes go to the installed skill AND to the source
repository named in .source_repo (written by install.py), and are committed there locally.
Nothing is pushed; push only when the user asks.

A lesson seen 3+ times (or one that a user explicitly asked for) should be promoted:
fold it into SKILL.md / a reference / a script, then run `learn.py promote`.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = os.path.join("references", "lessons.md")
AREAS = ["fidelity", "layout", "math", "code", "flowchart", "figures", "build", "workflow", "output"]
PROMOTE_AT = 3

HEADER = """# Lessons Learned

The skill's memory. **Read the active lessons before every run** and apply them. Add a
lesson after every run where the user corrected something, a check failed, or you hit and
fixed a non-obvious problem (`scripts/learn.py add`). Lessons seen {n}+ times get promoted
into the main rules or scripts (`scripts/learn.py promote`).

Never record personal data, document contents, names or file paths from the user's
documents. Record only the general, reusable lesson.

""".format(n=PROMOTE_AT)

ENTRY_RE = re.compile(r"^### (L\d+) \[(\w+)\] (.+?)$", re.M)


def targets():
    paths = [os.path.join(SKILL, REL)]
    marker = os.path.join(SKILL, ".source_repo")
    repo = None
    if os.path.exists(marker):
        repo = open(marker, encoding="utf-8").read().strip()
        rp = os.path.join(repo, "skills", "claude-latex", REL)
        if os.path.abspath(rp) != os.path.abspath(paths[0]) and os.path.isdir(os.path.dirname(rp)):
            paths.append(rp)
    elif os.path.basename(os.path.dirname(SKILL)) == "skills":       # running inside the repo
        repo = os.path.dirname(os.path.dirname(SKILL))
    return paths, repo


def load():
    path = targets()[0][0]
    if not os.path.exists(path):
        return HEADER, []
    text = open(path, encoding="utf-8").read()
    parts = ENTRY_RE.split(text)
    head, entries = parts[0].split("\n## Active lessons")[0].rstrip() + "\n", []
    for i in range(1, len(parts), 4):
        lid, status, title, body = parts[i], parts[i + 1], parts[i + 2], parts[i + 3]
        fields = dict(re.findall(r"^- \*\*(\w+):\*\* (.*)$", body, re.M))
        entries.append({"id": lid, "status": status, "title": title.strip(), **fields})
    return head if head.strip() else HEADER, entries


def render(head, entries):
    out = [head.rstrip() + "\n"]
    for status in ("active", "promoted"):
        group = sorted((e for e in entries if e["status"] == status), key=lambda e: int(e["id"][1:]))
        out.append("\n## %s\n" % ("Active lessons" if status == "active" else "Promoted (now part of the rules)"))
        if not group:
            out.append("\n_none_\n")
        for e in group:
            out.append("\n### %s [%s] %s\n" % (e["id"], e["status"], e["title"]))
            for key in ("area", "trigger", "why", "apply", "seen", "first", "last", "promoted_to"):
                if e.get(key):
                    out.append("- **%s:** %s\n" % (key, e[key]))
    return "".join(out)


def save(head, entries, message):
    paths, repo = targets()
    text = render(head, entries)
    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("saved", p)
    if repo and os.path.isdir(os.path.join(repo, ".git")):
        rel = os.path.join("skills", "claude-latex", REL)
        subprocess.run(["git", "-C", repo, "add", rel], capture_output=True)
        r = subprocess.run(["git", "-C", repo, "commit", "-q", "-m", message, "--", rel],
                           capture_output=True, text=True)
        print("committed in repo (not pushed)" if r.returncode == 0 else "repo: nothing to commit")


def words(s):
    return {w for w in re.findall(r"[a-z0-9]{4,}", s.lower())}


def cmd_list(a):
    _, entries = load()
    active = [e for e in entries if e["status"] == "active"]
    if not active:
        print("no active lessons")
    for e in active:
        print("%s [%s] seen %s: %s\n    apply: %s" % (e["id"], e.get("area"), e.get("seen", "1"),
                                                     e["title"], e.get("apply", "")))


def cmd_add(a):
    head, entries = load()
    today = datetime.date.today().isoformat()
    new = words(a.lesson)
    for e in entries:                               # same lesson again -> count it instead
        old = words(e["title"])
        if e["status"] == "active" and new and len(new & old) / float(len(new | old)) >= 0.6:
            e["seen"] = str(int(e.get("seen", "1")) + 1)
            e["last"] = today
            save(head, entries, "learn: %s seen again" % e["id"])
            print("matched existing %s (seen %s)" % (e["id"], e["seen"]))
            if int(e["seen"]) >= PROMOTE_AT:
                print("-> ready to promote: fold it into the rules/scripts, then `learn.py promote %s`" % e["id"])
            return
    nums = [int(e["id"][1:]) for e in entries] or [0]
    lid = "L%d" % (max(nums) + 1)
    entries.append({"id": lid, "status": "active", "title": a.lesson.strip(), "area": a.area,
                    "trigger": a.trigger, "why": a.why, "apply": a.apply, "seen": "1",
                    "first": today, "last": today})
    save(head, entries, "learn: %s %s" % (lid, a.lesson[:60]))
    print("added", lid)


def cmd_seen(a):
    head, entries = load()
    for e in entries:
        if e["id"] == a.id:
            e["seen"] = str(int(e.get("seen", "1")) + 1)
            e["last"] = datetime.date.today().isoformat()
            save(head, entries, "learn: %s seen again" % a.id)
            return
    sys.exit("no lesson %s" % a.id)


def cmd_promote(a):
    head, entries = load()
    for e in entries:
        if e["id"] == a.id:
            e["status"] = "promoted"
            e["promoted_to"] = a.to
            save(head, entries, "learn: promote %s into %s" % (a.id, a.to))
            return
    sys.exit("no lesson %s" % a.id)


def cmd_stats(a):
    _, entries = load()
    for area in AREAS:
        group = [e for e in entries if e.get("area") == area]
        if group:
            act = sum(1 for e in group if e["status"] == "active")
            print("%-10s %2d lessons (%d active)" % (area, len(group), act))
    ready = [e for e in entries if e["status"] == "active" and int(e.get("seen", "1")) >= PROMOTE_AT]
    for e in ready:
        print("READY TO PROMOTE %s (seen %s): %s" % (e["id"], e["seen"], e["title"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list").set_defaults(f=cmd_list)
    s = sub.add_parser("add")
    s.add_argument("--area", required=True, choices=AREAS)
    s.add_argument("--lesson", required=True, help="the rule, one sentence, imperative")
    s.add_argument("--why", required=True, help="what went wrong / what the user said")
    s.add_argument("--apply", required=True, help="exactly how to apply it next time")
    s.add_argument("--trigger", default="correction", choices=["correction", "check", "self"])
    s.set_defaults(f=cmd_add)
    s = sub.add_parser("seen"); s.add_argument("id"); s.set_defaults(f=cmd_seen)
    s = sub.add_parser("promote"); s.add_argument("id"); s.add_argument("--to", required=True)
    s.set_defaults(f=cmd_promote)
    sub.add_parser("stats").set_defaults(f=cmd_stats)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
