"""Worked example: TikZ flowcharts for C looping practicals (4.1-4.9), written to ./fc/*.tex.

loop_chart(pre, cond, body, post) builds the standard counted/conditional loop layout
(Start -> pre -> decision -> body -> back-edge, "No" exit -> post -> Stop).
The hand-written 4.2 / 4.5 / 4.7 charts show a nested decision, an early exit (break) with
a junction point, and an if/else after a loop. Copy and adapt; see references/practical-files.md.
"""
import os

os.makedirs("fc", exist_ok=True)

HEAD = r"""\begin{tikzpicture}[node distance=7mm, every node/.style={font=\large},
  fc/process/.append style={minimum width=4.6cm, text width=5.6cm},
  fc/io/.append style={minimum width=4.6cm, text width=5cm},
  fc/decision/.append style={inner sep=1pt, aspect=2.2, minimum width=3.4cm, minimum height=1.5cm}]
\coordinate (L) at (-5.0,0);
\coordinate (R) at (5.0,0);
"""
TAIL = "\\end{tikzpicture}\n"


def loop_chart(pre, cond, body, post):
    """pre/post: list of (style, text); body: list of process texts; Start/Stop added."""
    o = [HEAD, r"\node[fc/terminal] (n0) {Start};"]
    prev = "n0"
    for k, (st, tx) in enumerate(pre):
        o.append(r"\node[fc/%s, below=of %s] (p%d) {%s};" % (st, prev, k, tx))
        prev = "p%d" % k
    o.append(r"\node[fc/decision, below=of %s] (dec) {%s};" % (prev, cond))
    prev = "dec"
    for k, tx in enumerate(body):
        o.append(r"\node[fc/process, below=of %s] (b%d) {%s};" % (prev, k, tx))
        prev = "b%d" % k
    last_body = prev
    first_post = None
    for k, (st, tx) in enumerate(post):
        dist = "below=14mm of" if k == 0 else "below=of"
        o.append(r"\node[fc/%s, %s %s] (q%d) {%s};" % (st, dist, prev, k, tx))
        first_post = first_post or "q%d" % k
        prev = "q%d" % k
    o.append(r"\node[fc/terminal, %s %s] (end) {Stop};" % ("below=of" if post else "below=14mm of", prev))
    first_post = first_post or "end"
    chain = ["n0"] + ["p%d" % k for k in range(len(pre))] + ["dec"]
    for a, b in zip(chain, chain[1:]):
        o.append(r"\draw[fc/arrow] (%s) -- (%s);" % (a, b))
    o.append(r"\draw[fc/arrow] (dec) -- node[right]{Yes} (b0);")
    for k in range(len(body) - 1):
        o.append(r"\draw[fc/arrow] (b%d) -- (b%d);" % (k, k + 1))
    o.append(r"\draw[fc/arrow] (%s.south) -- ++(0,-5mm) -| (L |- dec) -- (dec.west);" % last_body)
    o.append(r"\draw[fc/arrow] (dec.east) -- node[above,pos=0.4]{No} (R |- dec) |- (%s.east);" % first_post)
    posts = ["q%d" % k for k in range(len(post))] + ["end"]
    for a, b in zip(posts, posts[1:]):
        o.append(r"\draw[fc/arrow] (%s) -- (%s);" % (a, b))
    o.append(TAIL)
    return "\n".join(o)


def write(name, text):
    open(os.path.join("fc", name + ".tex"), "w", encoding="utf-8").write(text)


write("4_1", loop_chart(
    [("io", "Read n"), ("process", "sum = 0, i = 1")],
    r"i $\le$ n ?",
    [r"Print i\\ sum = sum + i", "i = i + 1"],
    [("process", "avg = sum / n"), ("io", "Print sum, avg")]))

write("4_3", loop_chart(
    [("io", "Read n"), ("process", "fact = 1, i = 1")],
    r"i $\le$ n ?",
    [r"fact = fact $\times$ i", "i = i + 1"],
    [("io", "Print fact")]))

write("4_4", loop_chart(
    [("io", "Read n"), ("process", "a = 0, b = 1, i = 1")],
    r"i $\le$ n ?",
    [r"Print a\\ c = a + b\\ a = b, b = c", "i = i + 1"],
    []))

write("4_6", loop_chart(
    [("io", "Read n"), ("process", "sum = 0")],
    r"n $>$ 0 ?",
    [r"r = n \% 10\\ sum = sum + r\\ n = n / 10"],
    [("io", "Print sum")]))

write("4_8", loop_chart(
    [("io", "Read base, expo"), ("process", "result = 1, i = 1")],
    r"i $\le$ expo ?",
    [r"result = result $\times$ base", "i = i + 1"],
    [("io", "Print result")]))

write("4_9_i", loop_chart(
    [("io", "Read n"), ("process", "sum = 0, i = 1")],
    r"i $\le$ n ?",
    [r"sum = sum + 1 / i", "i = i + 1"],
    [("io", "Print sum")]))

write("4_9_ii", loop_chart(
    [("io", "Read x, n"), ("process", r"term = 1, sum = 1\\ i = 1")],
    r"i $\le$ n ?",
    [r"term = term $\times$ ($-$x) / i\\ sum = sum + term", "i = i + 1"],
    [("io", "Print sum")]))

# 4.2 — loop with an inner decision, then count check
write("4_2", HEAD + r"""
\node[fc/terminal] (n0) {Start};
\node[fc/io, below=of n0] (p0) {Read x, y};
\node[fc/process, below=of p0] (p1) {sum = 0, count = 0\\ i = x};
\node[fc/decision, below=of p1] (dec) {i $\le$ y ?};
\node[fc/decision, below=of dec] (odd) {i \% 2 $\ne$ 0 ?};
\node[fc/process, below=of odd] (b0) {Print i\\ sum = sum + i\\ count = count + 1};
\node[fc/process, below=of b0] (inc) {i = i + 1};
\node[fc/decision, below=14mm of inc] (cnt) {count $>$ 0 ?};
\node[fc/process, below=of cnt] (avg) {avg = sum / count};
\node[fc/io, below=of avg] (out) {Print sum, avg};
\node[fc/terminal, below=of out] (end) {Stop};
\node[fc/io, right=10mm of avg, text width=3.4cm, minimum width=3cm] (none) {Print ``No odd numbers''};
\draw[fc/arrow] (n0) -- (p0);
\draw[fc/arrow] (p0) -- (p1);
\draw[fc/arrow] (p1) -- (dec);
\draw[fc/arrow] (dec) -- node[right]{Yes} (odd);
\draw[fc/arrow] (odd) -- node[right]{Yes} (b0);
\draw[fc/arrow] (b0) -- (inc);
\draw[fc/arrow] (odd.east) -- node[above,pos=0.5]{No} ($(odd.east -| R)+(-1.0,0)$) |- (inc.east);
\draw[fc/arrow] (inc.south) -- ++(0,-5mm) -| (L |- dec) -- (dec.west);
\draw[fc/arrow] (dec.east) -- node[above,pos=0.4]{No} (R |- dec) |- (cnt.east);
\draw[fc/arrow] (cnt) -- node[right]{Yes} (avg);
\draw[fc/arrow] (avg) -- (out);
\draw[fc/arrow] (out) -- (end);
\draw[fc/arrow] (cnt.east) ++(0,0) -| node[above,pos=0.25]{No} (none.north);
\draw[fc/arrow] (none.south) |- (end.east);
""" + TAIL)

# 4.5 — prime check with early exit
write("4_5", HEAD + r"""
\node[fc/terminal] (n0) {Start};
\node[fc/io, below=of n0] (p0) {Read n};
\node[fc/process, below=of p0] (p1) {flag = 1, i = 2};
\node[fc/decision, below=of p1] (le1) {n $\le$ 1 ?};
\node[fc/decision, below=of le1] (dec) {i $\le$ n / 2 ?};
\node[fc/decision, below=of dec] (div) {n \% i == 0 ?};
\node[fc/process, below=of div] (inc) {i = i + 1};
\node[fc/decision, below=16mm of inc] (fl) {flag == 1 ?};
\node[fc/io, below=of fl] (pr) {Print ``prime''};
\node[fc/terminal, below=of pr] (end) {Stop};
\node[fc/process, minimum width=2.4cm, text width=2.4cm] (f0a) at ($(le1)+(6.2,0)$) {flag = 0};
\node[fc/process, minimum width=2.4cm, text width=2.4cm] (f0b) at ($(div)+(6.2,0)$) {flag = 0};
\node[fc/io, minimum width=3cm, text width=3.2cm] (npr) at ($(pr)+(-6,0)$) {Print ``not prime''};
\coordinate (col) at ($(f0a.east)+(0.7,0)$);
\coordinate (j) at ($(fl.north)+(0,8mm)$);
\draw[fc/arrow] (n0) -- (p0);
\draw[fc/arrow] (p0) -- (p1);
\draw[fc/arrow] (p1) -- (le1);
\draw[fc/arrow] (le1) -- node[right]{No} (dec);
\draw[fc/arrow] (le1) -- node[above]{Yes} (f0a);
\draw[fc/arrow] (dec) -- node[right]{Yes} (div);
\draw[fc/arrow] (div) -- node[right]{No} (inc);
\draw[fc/arrow] (div) -- node[above]{Yes} (f0b);
\draw[fc/arrow] (inc.south) -- ++(0,-5mm) -| (L |- dec) -- (dec.west);
\draw (f0a.east) -- (col);
\draw (f0b.east) -- (f0b.east -| col);
\draw (dec.east) -- node[above,pos=0.2]{No} (dec.east -| col);
\draw[fc/arrow] (col) |- (j) -- (fl.north);
\draw[fc/arrow] (fl) -- node[right]{Yes} (pr);
\draw[fc/arrow] (fl.west) -| node[above,pos=0.25]{No} (npr.north);
\draw[fc/arrow] (pr) -- (end);
\draw[fc/arrow] (npr.south) |- (end.west);
""" + TAIL)

# 4.7 — reverse loop, then palindrome decision
write("4_7", HEAD + r"""
\node[fc/terminal] (n0) {Start};
\node[fc/io, below=of n0] (p0) {Read n};
\node[fc/process, below=of p0] (p1) {rev = 0, temp = n};
\node[fc/decision, below=of p1] (dec) {temp $>$ 0 ?};
\node[fc/process, below=of dec] (b0) {r = temp \% 10\\ rev = rev $\times$ 10 + r\\ temp = temp / 10};
\node[fc/io, below=14mm of b0] (q0) {Print rev};
\node[fc/decision, below=of q0] (pal) {n == rev ?};
\node[fc/io, below=of pal] (yes) {Print ``palindrome''};
\node[fc/io, right=8mm of yes, text width=3.6cm, minimum width=3cm] (no) {Print ``not palindrome''};
\node[fc/terminal, below=of yes] (end) {Stop};
\draw[fc/arrow] (n0) -- (p0);
\draw[fc/arrow] (p0) -- (p1);
\draw[fc/arrow] (p1) -- (dec);
\draw[fc/arrow] (dec) -- node[right]{Yes} (b0);
\draw[fc/arrow] (b0.south) -- ++(0,-5mm) -| (L |- dec) -- (dec.west);
\draw[fc/arrow] (dec.east) -- node[above,pos=0.4]{No} (R |- dec) |- (q0.east);
\draw[fc/arrow] (q0) -- (pal);
\draw[fc/arrow] (pal) -- node[right]{Yes} (yes);
\draw[fc/arrow] (pal.east) -| node[above,pos=0.25]{No} (no.north);
\draw[fc/arrow] (yes) -- (end);
\draw[fc/arrow] (no.south) |- (end.east);
""" + TAIL)
print(sorted(os.listdir("fc")))
