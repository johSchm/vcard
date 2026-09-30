#!/usr/bin/env python3
"""Compile publications.bib into a PDF publication list.

    python3 tools/publications_pdf.py

Writes res/Publications_Johann_Schmidt.pdf, the file behind the "Download
as PDF" button in the publications section. Run it (next to build.py)
whenever publications.bib changes, then commit the PDF.

The entries are typeset by biblatex, newest first; entries from the same
year are listed in reverse file order. The website-only fields (abbr, pdf,
abstract, code) are left out, and an entry with a `doi` shows that instead
of its `url`.

Requires: a TeX distribution with latexmk and biber (e.g. `brew install texlive`)
"""
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publications  # noqa: E402

ROOT = publications.ROOT
OUT = ROOT / "res" / "Publications_Johann_Schmidt.pdf"

NAME = "Johann Schmidt"
SITE = "johann-schmidt.com"

TEMPLATE = r"""\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{tgheros}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage[english]{babel}
\usepackage{csquotes}
\usepackage{microtype}
\usepackage{xcolor}
\definecolor{accent}{HTML}{15906B}
\usepackage[backend=biber,style=numeric,sorting=none,giveninits=true,maxbibnames=99,
            isbn=false,eprint=false]{biblatex}
\addbibresource{publications.bib}
\usepackage[colorlinks,allcolors=accent,pdftitle={Publications},pdfauthor={<NAME>}]{hyperref}

%% my own name in bold (entries carry an `author+an` annotation)
\renewcommand*{\mkbibnamegiven}[1]{\ifitemannotation{highlight}{\textbf{#1}}{#1}}
\renewcommand*{\mkbibnamefamily}[1]{\ifitemannotation{highlight}{\textbf{#1}}{#1}}
\setlength{\bibitemsep}{.9\baselineskip}
\setlength{\parindent}{0pt}
\urlstyle{same}

\begin{document}
{\Huge\bfseries Publications}\par\medskip
{\large <NAME>}\hfill{\small\color{gray}\href{https://<SITE>}{<SITE>} \textperiodcentered\ <DATE>}\par
\smallskip{\color{accent}\rule{\linewidth}{1.2pt}}\par\bigskip
\nocite{*}
\printbibliography[heading=none]
\end{document}
"""


def bib_entry(entry: dict) -> str:
    f = {k: v for k, v in entry["fields"].items()
         if k not in publications.CARD_ONLY_FIELDS and v}
    if "doi" in f:
        f["doi"] = re.sub(r"^https?://(dx\.)?doi\.org/", "", f["doi"])
        f.pop("url", None)
    names = publications.split_top_level(f["author"], r"\s+and\s+")
    mine = [i for i, n in enumerate(names, 1) if publications.format_author(n) == publications.ME]
    if mine:
        f["author+an"] = ";".join(f"{i}=highlight" for i in mine)
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in f.items())
    return f"@{entry['type']}{{{entry['key']},\n{body}\n}}"


def native() -> list[str]:
    """Command prefix that leaves Rosetta on Apple Silicon.

    An Intel Python makes its child processes run translated too, and Homebrew's
    biber (arm64 Perl modules) then dies with "Attempt to reload List/Util.pm".
    """
    if platform.system() == "Darwin" and platform.machine() == "x86_64":
        translated = subprocess.run(["sysctl", "-n", "sysctl.proc_translated"],
                                    capture_output=True, text=True).stdout.strip()
        if translated == "1":
            return ["arch", "-arm64"]
    return []


def main() -> int:
    for tool in ("latexmk", "biber"):
        if not shutil.which(tool):
            print(f"'{tool}' not found, install a TeX distribution (e.g. brew install texlive)")
            return 1
    try:
        entries = publications.load()
    except publications.BibError as e:
        print(f"publications.bib has problems, no PDF was written:\n  {e}")
        return 1

    # newest first; sorted() is stable, so reversing first puts later entries of a year on top
    entries = sorted(reversed(entries), key=lambda e: -int(e["fields"]["year"]))
    tex = (TEMPLATE.replace("<NAME>", NAME).replace("<SITE>", SITE)
           .replace("<DATE>", date.today().strftime("%B %Y")))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "publications.bib").write_text("\n\n".join(bib_entry(e) for e in entries) + "\n",
                                              encoding="utf-8")
        (tmp / "publications.tex").write_text(tex, encoding="utf-8")
        run = subprocess.run(native() + ["latexmk", "-pdf", "-interaction=nonstopmode",
                                         "-halt-on-error", "publications.tex"],
                             cwd=tmp, capture_output=True, text=True, errors="replace")
        pdf = tmp / "publications.pdf"
        if run.returncode != 0 or not pdf.exists():
            print("LaTeX failed, no PDF was written. End of the log:\n")
            print("\n".join((run.stdout + run.stderr).splitlines()[-40:]))
            return 1
        OUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf, OUT)
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(entries)} publications)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
