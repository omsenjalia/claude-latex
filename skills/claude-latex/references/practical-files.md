# Practical / Lab-File Solutions (programs, flowcharts, outputs)

Use this when the user gives a list of practicals or programming questions (C, C++, Java,
Python…) and **asks for solutions**. Solutions are user-requested additions (see
`fidelity-rules.md` §6), so they are allowed. The rest of the fidelity rules still apply:
no AI remarks, nothing about "the source", no notes the user didn't ask for.

---

## 1. Page format (default)

```
[practical number] practical statement      ← statement copied from the source
Solution:                                    ← full program
Output:                                      ← real program output, with typed input shown
                                             ← (new page) optional flowchart page
```

- **One program per page.** Each program gets a page of its own, and its size and spacing
  are chosen to fill that page. Use `scripts/practicals.py`, which picks the code font
  (8.5–12 pt) and line spacing (1.2–1.6×) from the line count and longest line, then
  spreads the leftover height as gaps. Never leave a short program at the top of an empty
  page in a tiny font, and never let a program or its output break across pages.
- Very long programs, where code plus output would need less than 8.6 pt, keep the code
  on its own page and put the output on the next page under `<number> Output:`.
- Multi-part practicals (4.9 (i), (ii)) get **one page per part**. The first page shows the
  full statement. Later pages show `number (part)` and that part's formula.
- The first page carries the source's section heading (e.g. `4  Looping Statements`).
- Use the labels the user gives ("Solution", "Output"). Defaults: `Solution:` / `Output:`.

## 2. Writing the programs

- **Compiler style the user names.** For Turbo C use:
  `#include <stdio.h>`, `#include <conio.h>`, `void main()`, `clrscr();` after the
  declarations, `getch();` at the end. `int` is 16-bit, so use `long int` / `%ld` for
  factorials, powers and other large products. Don't use C99-only features (no `for (int i…)`,
  no `//` comments, no `stdbool.h`).
- **Proper spacing (always):** spaces around binary and assignment operators
  (`sum = sum + i`), after commas (`int n, i, sum = 0;`), after `;` in `for`
  (`for (i = 1; i <= n; i++)`), after keywords (`if (`, `while (`, `for (`), a space in
  `#include <stdio.h>`, a cast written as `(float) sum`, 4-space indentation, Allman braces,
  and a blank line between the declarations, the input section, the processing and the
  final output.
- Keep programs simple and syllabus-level: loops for loops practicals, no library
  shortcuts that the practical forbids (e.g. no `pow()` in "without using pow()").
- No comments in the code unless the user asks for them.

## 3. Outputs must be real: compile and run

1. Write each program to `src/<number>.c`.
2. Compile on the host with a shim so Turbo C calls work:
   ```bash
   mkdir -p shim && printf '#define clrscr()\n#define getch() 0\n' > shim/conio.h
   gcc -w -Ishim src/4_1.c -o 4_1.exe && printf '10\n' | ./4_1.exe
   ```
3. Build the output block as it would look on the console: each prompt **followed by the
   typed input** on the same line (`Enter the value of N: 10`), then the program's output.
   Trim trailing spaces.
4. For yes/no programs (prime, palindrome, even/odd…) show **one run for each case**,
   separated by a blank line.
5. Never write an output you didn't get from a real run.

## 4. Typos in the source

If a statement has an obvious typo (e.g. a series whose signs contradict its `±` ending),
**report it in chat and ask**, unless the user has already said to fix typos. When the user
says to fix it, correct the statement in the PDF too and make the program match. Don't add
a note about the correction to the PDF.

## 5. Flowcharts (only when asked)

- One flowchart per program, **on a separate page right after that program**, headed
  `<number> Flowchart`. It's scaled to fill the page (`practicals.py` uses adjustbox to fit
  the text width and 84 % of the text height, keeping the aspect ratio).
- Standard shapes from `claudelatex.sty` `[flowcharts]`: `fc/terminal` (Start/Stop),
  `fc/io` (Read/Print), `fc/process`, `fc/decision`, arrows `fc/arrow`. Give decisions room
  so the text never touches the diamond:
  `fc/decision/.append style={inner sep=1pt, aspect=2.2, minimum width=3.4cm, minimum height=1.5cm}`.
- Layout rules that keep loops readable:
  - Main path straight down the centre. Label the "Yes" branch on the downward arrow.
  - Loop back-edge: from the last body box go down, left to a fixed column `L` (x = −5 cm),
    up to the decision, then into its west side.
  - Loop exit "No": from the decision's east side, right to a fixed column `R` (x = +5 cm),
    down, then into the first node after the loop.
  - Inner decisions (e.g. `i % 2 != 0 ?`) exit on the side *inside* the outer columns, so
    lines never cross.
  - Side branches (`flag = 0`, `Print "not prime"`) sit beside the main column and rejoin
    through one junction point above the next shared node.
- **Use `scripts/flowgen.py` first.** It builds the whole chart from a block list (`io`,
  `process`, `loop` with any nesting, `if`, `ifelse`, optional `connector`) and applies all
  the layout rules above automatically, including column placement per nesting level and
  compact spacing for long charts. Hand-written TikZ is only for shapes it can't express,
  such as a `break` out of a loop. For those, see `scripts/flowchart_examples.py` (4.5) and
  `templates/snippets/flowchart-loop.tex`.
- Abstraction is allowed when it keeps the chart readable: a plain input or print loop can
  be one I/O box (`Read a[0] … a[n − 1]`, `Read matrix a[3][3]`, `Print sorted array`).
  The loops that are the point of the practical (the search, the sort, the row sums) must
  be drawn in full.
- Don't split a chart into connector-joined columns unless both halves are similar in
  height. On portrait A4, one tall column almost always comes out larger. A good case is
  two independent query loops one after the other (e.g. hotel system 9.3): put
  `("connector",)` between them.
- **User-defined functions and recursion:** draw one chart for `main()` (the call shown as
  a process box, e.g. `Call oddEven(num)` or `sum = sumOfN(n)`) and one chart per function,
  started with `start="fact(n)"` and ended with `stop="Return"`, `"Return s"` or `"End"`.
  For a recursive function, use an `ifelse` for the base case and the recursive case
  (`Return 1` / `Return n × fact(n − 1)`). In the spec, give `"flowchart"` as a list of
  `{"title", "file"}`. `practicals.py` measures side-by-side and stacked layouts and keeps
  whichever comes out larger.
- Flowcharts fill the page but are never scaled beyond 1.5×, so tiny charts don't turn
  into giant boxes. Node text never hyphenates; boxes are 6 cm wide so formulas don't wrap
  mid-word.
- Programs whose loops use `break` (prime check, string palindrome) can usually be written
  with the condition in the loop instead (`while (i < len / 2 && flag == 1)`). That keeps
  the program simple and lets `flowgen` draw it.
- File programs: write and read fixed or user-named files, create any input file (e.g.
  `source.txt`) before the test run, and save it with the sources.
- Pointer addresses are printed with `%u` (Turbo C convention). The output shows the
  addresses from the real run, which differ from machine to machine.
- If the statement leaves a formula undefined (e.g. gross/net salary), use a common
  textbook convention, make the program print each component (`DA (40%)`, `HRA (20%)`,
  `PF (12%)`), and tell the user in chat which convention you used.
- TeX gotcha: in node text, write a straight quote as `{\textquotesingle}a{\textquotesingle}`.
  Without the braces, `\textquotesinglea` is read as one unknown command.
- Flowchart steps must match the program exactly: same variables, same conditions, same
  order.
- **Note text:** add a note only if the user asks, worded as they asked, e.g.
  `"flowchart_note": "Note: This flowchart is for learning purposes only."`. Then run the
  checker with `--allow "note:"`.

## 6. Statements that are tables or patterns

Pattern practicals ("print the following pattern") show the pattern itself as the statement.
Typeset it as a `tabular` with one cell per character, so right-aligned and centred
patterns keep their shape, and copy any side text like `where n=4`. Set `"statement_lines"`
in the spec to the pattern's height in lines, so `practicals.py` reserves the right space.
Keep the source's numbering exactly (`5.1)` with its parenthesis, `6.1` without). Test each
pattern program with the n the source shows, and check that every row of the real output
matches the source pattern.

## 7. Saving and naming

- One PDF per practical (topic). When the user wants them saved, name each file
  `Practical <n> - <heading>.pdf` (e.g. `Practical 4 - Looping Statements.pdf`).
  Windows doesn't allow `:` in file names, so use ` - ` and tell the user.
  If the source has no short heading (e.g. "Write a C program to print following Pattern"),
  use a short noun for it (`Patterns`) in the file name only, never inside the PDF.
- Keep the sources next to the PDFs in `sources/practical-<n>/`: `.tex`, `claudelatex.sty`,
  `spec.json`, `src/*.c`, `fc/*.tex`. Then the file can be rebuilt after edits.
- Never leave deliverables only in a session's temporary folder. Offer a permanent folder.

## 8. Build steps

```bash
python scripts/practicals.py spec.json out.tex      # see the docstring for the spec format
python scripts/build.py out.tex
python scripts/check_fidelity.py out.tex --pdf out.pdf [--allow "note:"]
python scripts/pdftool.py render out.pdf png --dpi 70   # look at EVERY page
```

Generate `.tex` and spec files with Python scripts saved to disk (or the Write tool), not
with shell heredocs inside `python - <<EOF`. Some shells collapse `\\` there, which corrupts
LaTeX.

Visual check, every page:
- program page: code and output are on one page, the page is well filled, nothing is cut off
- flowchart page: no text touches a shape border, no lines cross, no label overlaps a box,
  the chart fills the page
