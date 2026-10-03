#!/usr/bin/env python3
"""Remember per-series settings (next page number, options) between runs.

  series.py get  "<series>"                         print the stored state (or nothing)
  series.py set  "<series>" --next-page 10 [--opt codecolor=on --opt mode=notes ...]
  series.py list                                    all known series

A "series" is a topic delivered as several source files (Lecture 1, 2, 3...). Output page
numbers continue across the series; store where the next file must start after each run.

State is kept in state/series.json inside the INSTALLED skill only. It is user data, so it
is never written to the source repo and never committed or pushed.
"""
import argparse
import datetime
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(SKILL, "state", "series.json")


def load():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save(data):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(data, open(STATE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("get"); g.add_argument("series")
    s = sub.add_parser("set"); s.add_argument("series")
    s.add_argument("--next-page", type=int)
    s.add_argument("--opt", action="append", default=[], help="key=value, repeatable")
    sub.add_parser("list")
    a = ap.parse_args()
    data = load()
    key = getattr(a, "series", "").strip().lower()
    if a.cmd == "get":
        if key in data:
            print(json.dumps(data[key], indent=1, ensure_ascii=False))
    elif a.cmd == "set":
        entry = data.get(key, {"name": a.series.strip()})
        if a.next_page is not None:
            entry["next_page"] = a.next_page
        for kv in a.opt:
            k, _, v = kv.partition("=")
            entry.setdefault("options", {})[k.strip()] = v.strip()
        entry["updated"] = datetime.date.today().isoformat()
        data[key] = entry
        save(data)
        print("saved", json.dumps(entry, ensure_ascii=False))
    else:
        for v in data.values():
            print("%s: next page %s %s" % (v["name"], v.get("next_page", "?"), v.get("options", "")))


if __name__ == "__main__":
    main()
