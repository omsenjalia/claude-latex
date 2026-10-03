# Lessons Learned

The skill's memory. **Read the active lessons before every run** and apply them. Add a
lesson after every run where the user corrected something, a check failed, or you hit and
fixed a non-obvious problem (`scripts/learn.py add`). Lessons seen 3+ times get promoted
into the main rules or scripts (`scripts/learn.py promote`).

Never record personal data, document contents, names or file paths from the user's
documents. Record only the general, reusable lesson.

## Active lessons

### L9 [active] Confirm every edit really applied (and rebuild succeeded) before sending the PDF
- **area:** workflow
- **trigger:** self
- **why:** A scripted text replace failed on an assert, and the unchanged PDF was sent as if it were fixed.
- **apply:** After each fix, check the edit output, rebuild, grep the PDF text for the changed string, then send.
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03

### L10 [active] Do text edits to .tex with the Edit tool or a saved script using raw strings; never sed or inline python with backslashes
- **area:** build
- **trigger:** self
- **why:** sed turned usetikzlibrary into Setikzlibrary and inline python raised unicode-escape errors on LaTeX backslashes.
- **apply:** Use Edit for single changes; for bulk changes Write a .py file with r-strings and run it.
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03

## Promoted (now part of the rules)

### L1 [promoted] Never add AI remarks, 'reconstructed' labels, colophons or comments about 'the source' to the PDF
- **area:** fidelity
- **trigger:** correction
- **why:** A previous AI-made PDF had a 'Reconstructed academic notes' header, a closing colophon and lines like 'as in the source method'; the user rejected them.
- **apply:** Run check_fidelity.py on every output; report doubts in chat only.
- **seen:** 1
- **first:** 2026-10-01
- **last:** 2026-10-01
- **promoted_to:** references/fidelity-rules.md

### L2 [promoted] Give code proper spacing: around operators, after commas and for-semicolons, blank lines between sections
- **area:** code
- **trigger:** correction
- **why:** User asked for 'proper spacing' after seeing cramped Turbo C code like for(i=1;i<=n;i++).
- **apply:** Write for (i = 1; i <= n; i++), sum = sum + i, int n, i, sum = 0; blank line between declarations, input, processing, output.
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** references/practical-files.md

### L3 [promoted] Give each program a whole page and size it to fill the page
- **area:** layout
- **trigger:** correction
- **why:** User said 'you have the whole page for a program, use it wisely' when short programs sat at the top of mostly empty pages.
- **apply:** Use practicals.py (fitted font/spacing, one program per page, output to next page only below 8.6 pt).
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** scripts/practicals.py

### L4 [promoted] Fix an obvious typo in a statement only after the user agrees, and change statement and program together
- **area:** fidelity
- **trigger:** correction
- **why:** A series printed as 1 - x + x^2/2! + x^3/3! ... +- x^n/n! contradicted its +- ending; the user confirmed it was a typo and asked for the fix.
- **apply:** Report suspected typos in chat; when approved, correct the PDF statement and the program, with no note in the PDF.
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** references/practical-files.md

### L5 [promoted] Put flowcharts on their own page after each program, scaled to fill it, with a note only if the user asked
- **area:** flowchart
- **trigger:** correction
- **why:** User asked for a flowchart per program on a separate page with 'for learning purposes only'.
- **apply:** Build charts with flowgen.py; practicals.py adds the page, scales up to 1.5x, prints flowchart_note; checker with --allow 'note:'.
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** scripts/flowgen.py

### L6 [promoted] Generate .tex/.py files with the Write tool or saved scripts, never through shell heredocs that contain backslashes
- **area:** build
- **trigger:** self
- **why:** Git Bash heredocs collapsed \\ and \n several times, corrupting LaTeX and Python.
- **apply:** Write generator scripts to disk with the Write tool, then run them.
- **seen:** 3
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** references/practical-files.md

### L7 [promoted] Save deliverables as 'Practical <n> - <heading>.pdf' in a permanent folder, sources in sources/practical-<n>/
- **area:** output
- **trigger:** correction
- **why:** User asked for files named 'Practical n: (heading)'; ':' is invalid on Windows, and the session folder is temporary.
- **apply:** Use ' - ' instead of ':', tell the user, keep sources beside the PDFs.
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** references/practical-files.md

### L8 [promoted] Never put absolute machine paths in the .tex
- **area:** fidelity
- **trigger:** check
- **why:** check_fidelity flagged \input paths containing the tool's folder name.
- **apply:** Use paths relative to the .tex (practicals.py does this).
- **seen:** 1
- **first:** 2026-10-03
- **last:** 2026-10-03
- **promoted_to:** references/checklist.md
