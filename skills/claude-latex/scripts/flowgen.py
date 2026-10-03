#!/usr/bin/env python3
"""Generate a TikZ flowchart (tikzpicture) from a nested block description.

    from flowgen import flowchart
    tex = flowchart([
        ("io", "Read n"),
        ("loop", "i = 0", r"i $<$ n ?", [            # init (or None), condition, body
            ("io", "Read a[i]"),
            ("process", "i = i + 1"),                 # body should end with the update step
        ]),
        ("if", r"a[0] $>$ 0 ?", [("io", "Print a[0]")]),            # if without else
        ("ifelse", r"found == 1 ?", [("io", "Print ``found''")],    # if / else (else = one node)
                   ("io", "Print ``not found''")),
        ("connector",),                               # optional: continue in a new column
    ])
    open("fc/x.tex", "w").write(tex)

Start and Stop are added automatically; for a user-defined function's own chart pass e.g.
start="fact(n)", stop="Return" (practicals.py can show it beside main()). Layout rules (see references/practical-files.md):
- main path straight down the centre; "Yes" on the downward arrow
- each loop: back-edge on its own left column, "No" exit on its own right column;
  nested loops use columns further in, so lines never cross
- if: "No" bypasses on the right, inside the enclosing loop's columns, and rejoins below
- charts with many nodes per column switch to a compact spacing automatically
- optional ("connector",) blocks continue the chart in a new column (circle A, B, ...);
  only worth it when the two halves are similar in height
Use with \\usepackage[flowcharts]{claudelatex}; practicals.py scales the result to the page.
"""

INNER_COL = 4.1      # |x| of the innermost loop's columns (cm)
COL_STEP = 1.35      # extra |x| per enclosing loop level (cm)
COLUMN_GAP = 2.6     # space between split columns (cm)


def _depth(blocks, d=0):
    m = d
    for b in blocks:
        if b[0] == "loop":
            m = max(m, _depth(b[3], d + 1))
        elif b[0] in ("if", "ifelse"):
            m = max(m, _depth(b[2], d))
    return m


def _count(blocks):
    n = 0
    for b in blocks:
        if b[0] == "loop":
            n += (1 if b[1] else 0) + 1 + _count(b[3])
        elif b[0] in ("if", "ifelse"):
            n += 1 + _count(b[2])
        elif b[0] == "connector":
            n += 1
        else:
            n += 1
    return n


class _Flow:
    def __init__(self, max_depth):
        self.nodes, self.edges = [], []
        self.k = 0
        self.prev = None
        self.prev_is_coord = False
        self.incoming = []
        self.gap = None
        self.max_depth = max_depth
        self.xoff = 0.0
        self.start = None
        self.conn = 0

    def col(self, depth):
        return INNER_COL + COL_STEP * (self.max_depth - 1 - depth)

    def _new(self):
        self.k += 1
        return "v%d" % self.k

    def _wire(self, target, is_coord):
        te = target if is_coord else target + ".east"
        for e in self.incoming:
            self.edges.append(e % {"t": target, "te": te, "arrow": "-" if is_coord else "fc/arrow"})

    def _straight_from(self, name):
        self.incoming = [r"\draw[%(arrow)s] (" + name + r") -- (%(t)s);"]

    def node(self, style, text):
        name = self._new()
        pos = "" if self.prev is None else ", %s %s" % (self.gap or "below=of", self.prev)
        self.nodes.append(r"\node[fc/%s%s] (%s) {%s};" % (style, pos, name, text))
        self._wire(name, False)
        self.prev, self.prev_is_coord, self.gap = name, False, None
        self._straight_from(name)
        return name

    def junction(self):
        name = self._new()
        self.nodes.append(r"\node[coordinate, below=5mm of %s] (%s) {};" % (self.prev, name))
        self._wire(name, True)
        self.prev, self.prev_is_coord, self.gap = name, True, None
        self._straight_from(name)
        return name

    def items(self, blocks, depth):
        for b in blocks:
            kind = b[0]
            if kind in ("io", "process"):
                self.node(kind, b[1])
            elif kind == "loop":
                self.loop(b[1], b[2], b[3], depth)
            elif kind == "if":
                self.if_(b[1], b[2], None, depth)
            elif kind == "ifelse":
                self.if_(b[1], b[2], b[3], depth)
            elif kind == "connector":
                self.connector()
            else:
                raise ValueError("unknown block %r" % (kind,))

    def loop(self, init, cond, body, depth):
        if init:
            self.node("process", init)
        dec = self.node("decision", cond)
        self.incoming = [r"\draw[%(arrow)s] (" + dec + r") -- node[right]{@YES@} (%(t)s);"]
        self.items(body, depth + 1)
        x = self.col(depth)
        src = "(%s)" % self.prev if self.prev_is_coord else "(%s.south)" % self.prev
        self.edges.append(r"\draw[fc/arrow] %s -- ++(0,-4mm) -| (%.2f,0 |- %s) -- (%s.west);"
                          % (src, self.xoff - x, dec, dec))
        self.incoming = [r"\draw[%(arrow)s] (" + dec + r".east) -- node[above,pos=0.3]{@NO@} ("
                         + "%.2f,0 |- %s" % (self.xoff + x, dec) + r") |- (%(te)s);"]
        self.gap = "below=11mm of"

    def if_(self, cond, yes, other, depth):
        dec = self.node("decision", cond)
        self.incoming = [r"\draw[%(arrow)s] (" + dec + r") -- node[right]{@YES@} (%(t)s);"]
        first_yes = self.k + 1
        self.items(yes, depth)
        j = self.junction()
        if other is None:
            x = self.xoff + (self.col(depth - 1) - 0.9 if depth > 0 else INNER_COL)
            self.edges.append(r"\draw (%s.east) -- node[above,pos=0.3]{@NO@} (%.2f,0 |- %s) |- (%s);"
                              % (dec, x, dec, j))
        else:
            style, text = other
            alt = self._new()
            if _has_loop(yes):
                # the Yes branch has loop columns: put the else box level with the decision,
                # to the right of every loop column, so no lines cross
                x = self.col(depth - 1 if depth > 0 else 0) + 3.4
                self.nodes.append(r"\node[fc/%s] (%s) at ($(%s)+(%.2f,0)$) {%s};"
                                  % (style, alt, dec, x, text))
                self.edges.append(r"\draw[fc/arrow] (%s.east) -- node[above]{@NO@} (%s.west);" % (dec, alt))
            else:
                self.nodes.append(r"\node[fc/%s, right=12mm of v%d] (%s) {%s};"
                                  % (style, first_yes, alt, text))
                self.edges.append(r"\draw[fc/arrow] (%s.east) -| node[above,pos=0.25]{@NO@} (%s.north);"
                                  % (dec, alt))
            self.edges.append(r"\draw (%s.south) |- (%s);" % (alt, j))

    def connector(self):
        """End this column with a labelled circle; continue at the top of a new column."""
        self.conn += 1
        label = chr(ord("A") + self.conn - 1)
        self.node("connector", label)
        self.xoff += 2 * self.col(0) + COLUMN_GAP
        name = self._new()
        self.nodes.append(r"\node[fc/connector] (%s) at ($(%s)+(%.2f,0)$) {%s};"
                          % (name, self.start, self.xoff, label))
        self.prev, self.prev_is_coord, self.gap = name, False, None
        self._straight_from(name)

    def render(self, blocks, start="Start", stop="Stop"):
        self.start = self.node("terminal", start)
        self.items(blocks, 0)
        if stop:
            self.node("terminal", stop)
        return self.nodes, self.edges


def _auto_split(blocks, limit):
    """Insert a connector at the top-level boundary that best halves a tall chart."""
    if any(b[0] == "connector" for b in blocks) or len(blocks) < 2:
        return blocks
    total = _count(blocks) + 2
    if total <= limit:
        return blocks
    best, run = None, 1
    for i, b in enumerate(blocks[:-1]):
        run += _count([b])
        score = abs(total / 2.0 - run)
        if best is None or score < best[0]:
            best = (score, i + 1)
    i = best[1]
    return blocks[:i] + [("connector",)] + blocks[i:]


def _has_loop(blocks):
    return any(b[0] == "loop" or (b[0] in ("if", "ifelse") and _has_loop(b[2])) for b in blocks)


def flowchart(blocks, compact=None, split_over=None, start="Start", stop="Stop",
              branch=("Yes", "No")):
    """Return a tikzpicture string for the given blocks.

    On a portrait A4 page one tall column almost always scales better than two side-by-side
    columns, so splitting is off by default. Pass split_over=N to split charts with more
    than N nodes into two connector-joined columns, or place ("connector",) yourself when
    two halves are similar in height. `branch` sets the decision labels to match the
    source, e.g. ("True", "False") or ("T", "F")."""
    if split_over:
        blocks = _auto_split(blocks, split_over)
    depth = _depth(blocks)
    cols = 1 + sum(1 for b in blocks if b[0] == "connector")
    per_col = (_count(blocks) + 2) / float(cols)
    if compact is None:
        compact = per_col > 16
    f = _Flow(max(depth, 1))
    nodes, edges = f.render(blocks, start, stop)
    opts = [r"node distance=%s" % ("4.5mm" if compact else "7mm"),
            r"every node/.style={font=\large, execute at begin node=\hyphenpenalty 10000\relax}",
            r"fc/process/.append style={minimum width=4.6cm, text width=6cm}",
            r"fc/io/.append style={minimum width=4.4cm, text width=5.4cm}",
            r"fc/connector/.append style={circle, draw, minimum size=9mm, inner sep=0pt}"]
    if compact:
        opts.append(r"fc/decision/.append style={minimum height=1.05cm, aspect=2.8}")
    tex = ("\\begin{tikzpicture}[" + ",\n  ".join(opts) + "]\n"
           + "\n".join(nodes) + "\n" + "\n".join(edges) + "\n\\end{tikzpicture}\n")
    return tex.replace("@YES@", branch[0]).replace("@NO@", branch[1])


if __name__ == "__main__":
    print(flowchart([
        ("io", "Read n"),
        ("loop", "i = 1", r"i $\le$ n ?", [("io", "Print i"), ("process", "i = i + 1")]),
    ]))
