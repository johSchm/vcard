#!/usr/bin/env python3
"""Compile the website's content into a CV.

    python3 tools/cv_pdf.py

Writes res/CV_Johann_Schmidt.pdf, the file behind the "Download CV" button.
Run it (next to build.py) whenever the content changes, then commit the PDF.

The CV has no text of its own. Its settings are in content/cv.md, everything
else comes from the other content files and publications.bib. Entries carry a
`cv:` line with the short text for the CV; "cv: no" leaves an entry out. See
the comment at the top of content/cv.md for what comes from where.

Requires: a TeX distribution with latexmk (e.g. `brew install texlive`);
magick (ImageMagick) to shrink the photo, optional
"""
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import publications  # noqa: E402
from build import ContentError, Node  # noqa: E402
from publications_pdf import native  # noqa: E402

ROOT = publications.ROOT
OUT = ROOT / "res" / "CV_Johann_Schmidt.pdf"
MAX_PAGES = 2

SECTIONS = ("profile", "numbers", "experience", "education", "publications",
            "skills", "service", "talks")

TEMPLATE = r"""\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{tgheros}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[a4paper,hmargin=1.7cm,top=1.4cm,bottom=1.7cm,footskip=.8cm]{geometry}
\usepackage[english]{babel}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{needspace}
\usepackage{tikz}
\usepackage{fontawesome5}
\definecolor{accent}{HTML}{15906B}
\definecolor{muted}{HTML}{5C6664}
\usepackage[hidelinks,pdftitle={Curriculum Vitae},pdfauthor={<NAME>}]{hyperref}

\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlength{\tabcolsep}{0pt}
\setlength{\lineskip}{0pt}  % rows of one and of several lines are spaced alike
\tolerance=1500
\emergencystretch=3em
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[L]{\footnotesize\color{muted}<NAME> \textperiodcentered\ Curriculum Vitae \textperiodcentered\ <DATE>}
\fancyfoot[R]{\footnotesize\color{muted}\thepage}

%% section heading with a rule running to the right margin; never alone at the foot of a page
\newcommand{\cvsection}[1]{\par\addvspace{10pt}\needspace{5\baselineskip}%
  {\small\bfseries\color{accent}\textls[70]{\MakeUppercase{#1}}}\enspace
  {\color{accent!40}\leaders\hrule height 3.1pt depth -2.6pt\hfill\kern0pt}\par\nobreak\vspace{2.5pt}}

%% "title · place                years"
\newcommand{\cvline}[3]{%
  \begin{tabularx}{\linewidth}[t]{@{}>{\raggedright\arraybackslash}X@{\hspace{1em}}r@{}}
    \textbf{#1}\if\relax\detokenize{#2}\relax\else\ {\color{muted}\textperiodcentered\ #2}\fi & {\color{muted}#3}
  \end{tabularx}\par}
\newcommand{\cventry}[3]{\par\addvspace{5pt}\cvline{#1}{#2}{#3}\nobreak}
\newenvironment{cvparts}{\begin{itemize}[leftmargin=1.1em,labelsep=.45em,itemsep=3pt,topsep=3pt,
  parsep=0pt,partopsep=0pt,label={\color{accent}\rule[.25ex]{3pt}{3pt}}]}{\end{itemize}}
\newcommand{\cvpart}[3]{\item \cvline{#1}{#2}{#3}\nobreak}

%% "label   text", used for publications, skills, service and talks
\newcommand{\cvrow}[2]{\par\addvspace{3.5pt}%
  \begin{tabularx}{\linewidth}[t]{@{}>{\raggedright\arraybackslash\bfseries}p{3.35cm}@{\hspace{.7em}}X@{}}
    #1 & #2
  \end{tabularx}\par}

\begin{document}
\fontsize{9.3}{12.4}\selectfont
<BODY>
\end{document}
"""


# --- text -> LaTeX ------------------------------------------------------------

SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
           "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
           "₂": r"\textsubscript{2}", "<": r"\textless{}", ">": r"\textgreater{}", "|": r"\textbar{}",
           '"': r"\textquotedbl{}"}
MARKUP = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)"                               # [label](url)
                    r"|\*\*(.+?)\*\*"                                          # **bold**
                    r"|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])")             # *italic*


def esc(text: str) -> str:
    return "".join(SPECIAL.get(c, c) for c in text)


def href(url: str, label: str) -> str:
    return r"\href{%s}{%s}" % (re.sub(r"([%#&])", r"\\\1", url), label)


def tex(text: str) -> str:
    """Content text as LaTeX: escaped, with **bold**, *italic* and [links](url)."""
    text = re.sub(r"\s*(?:\\\\|\\n|<br\s*/?>)\s*", " ", text)  # the website's line breaks
    text = re.sub(r"(?<=\d) - (?=\d|today)", " – ", text)      # 2020 - today
    out, pos = [], 0
    for m in MARKUP.finditer(text):
        out.append(esc(text[pos:m.start()]))
        label, url, bold, italic = m.groups()
        if label:
            out.append(href(url, esc(label)) if url.startswith(("http://", "https://")) else esc(label))
        elif bold:
            out.append(r"\textbf{%s}" % esc(bold))
        else:
            out.append(r"\textit{%s}" % esc(italic))
        pos = m.end()
    return "".join(out) + esc(text[pos:])


def short_url(url: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", url).rstrip("/")


def year_of(text: str) -> str:
    m = re.search(r"\d{4}", text)
    return m.group(0) if m else ""


# --- reading the content ------------------------------------------------------

def cv_text(node: Node) -> str | None:
    """The node's `cv:` line; None if it says "no" (leave the entry out)."""
    text = node.props.get("cv", "")
    return None if text.lower() in ("no", "-") else text


def counters(docs: dict[str, Node], entries: list[dict]) -> dict[str, int]:
    return {"publications": len(entries), **build.service_counts(docs["service"])}


def fill(text: str, counts: dict[str, int], rows: str = "") -> str:
    for name, value in counts.items():
        text = text.replace("{" + name + "}", str(value))
    return text.replace("{rows}", rows)


# --- sections -----------------------------------------------------------------

CONTACT_ICONS = {"email": r"\faEnvelope", "location": r"\faMapMarker*", "website": r"\faGlobe",
                 "linkedin": r"\faLinkedin", "github": r"\faGithub", "scholar": r"\faGraduationCap"}


def header(docs: dict[str, Node], photo: bool) -> str:
    """Photo, name and headline on the left, contact details with icons on the right."""
    cv, home = docs["cv"], docs["home"]
    contact = []  # (icon, text)
    if home.props.get("email"):
        contact.append(("email", href("mailto:" + home.props["email"], esc(home.props["email"]))))
    if cv.props.get("location"):
        contact.append(("location", tex(cv.props["location"])))
    for key in ("website", "linkedin", "github"):
        url = cv.props.get(key) or home.props.get(key)
        if url:
            contact.append((key, href(url, esc(short_url(url)))))
    if cv.props.get("scholar"):
        contact.append(("scholar", href(cv.props["scholar"], "Google Scholar")))
    rows = r"\\".join(r"{\color{accent}%s} & %s" % (CONTACT_ICONS[icon], text) for icon, text in contact)
    picture = ""
    if photo:  # circle showing the top square of the picture
        picture = (r"\begin{tikzpicture}[baseline={([yshift=-.6ex]current bounding box.center)}]"
                   r"\clip (0,0) circle (1.25cm);"
                   r"\node[anchor=north,inner sep=0pt] at (0,1.25cm) {\includegraphics[width=2.5cm]{photo}};"
                   r"\end{tikzpicture}\hspace{1.3em}")
    return "\n".join([
        picture + r"\begin{tabular}{@{}l@{}}{\fontsize{25}{27}\selectfont\bfseries %s}\\[7pt]"
        % tex(cv.need("name", "cv.md")),
        r"{\fontsize{12.5}{15}\selectfont\color{accent}%s}\end{tabular}\hfill" % tex(cv.need("headline", "cv.md")),
        r"{\small\color{muted}\begin{tabular}{@{}c@{\hspace{.6em}}l@{}}%s\end{tabular}}\par\vspace{7pt}" % rows,
        r"{\color{accent}\rule{\linewidth}{1.2pt}}\par",
    ])


def profile(docs, entries, counts) -> str:
    text = cv_text(docs["about"])
    return r"\vspace{7pt}" + tex(fill(text, counts)) + r"\par" if text else ""


def numbers(docs, entries, counts) -> str:
    """The counters of the About section as a row of key figures."""
    stats = next((c for c in docs["about"].children if c.title.lower() == "numbers"), None)
    cols = []
    for item in build.list_items(stats.body) if stats else []:
        item = fill(item, counts)
        if y := re.match(r"^\{years since (\d{4})\}", item):
            item = str(max(date.today().year - int(y.group(1)), 0)) + item[y.end():]
        m = re.match(r"^(\d+\+?)\s+(.+)$", item)
        if not m:
            raise ContentError(f"about.md: cannot read the number '{item}'")
        cols.append(r"{\fontsize{15}{17}\selectfont\bfseries\color{accent}%s}\newline{\small\color{muted}%s}"
                    % (esc(m.group(1)), tex(m.group(2))))
    if not cols:
        return ""
    return (r"\par\addvspace{8pt}\begin{tabularx}{\linewidth}{@{}*{%d}{>{\centering\arraybackslash}X}@{}}"
            % len(cols) + "\n" + " &\n".join(cols) + "\n" + r"\end{tabularx}\par")


def last_year(node: Node) -> int:
    when = node.props.get("when", "")
    return 9999 if "today" in when.lower() else max(map(int, re.findall(r"\d{4}", when)), default=0)


def resume(docs, section: str, title: str) -> str:
    """Cards of resume.md in this section, plus parts moved here with their own `cv_section:`."""
    found = []  # (entry, its parts)
    for card in docs["resume"].children:
        home = card.props.get("cv_section", "Experience").lower()
        parts = [p for p in reversed(card.children) if cv_text(p) is not None]
        if home == section and cv_text(card) is not None:
            found.append((card, [p for p in parts if p.props.get("cv_section", home).lower() == home]))
        found += [(p, []) for p in parts if p.props.get("cv_section", home).lower() == section != home]
    # newest first; sorted() is stable, so entries ending in the same year keep the file's order reversed
    found = sorted(reversed(found), key=lambda e: -last_year(e[0]))
    out = []
    for node, parts in found:
        out.append(r"\cventry{%s}{%s}{%s}" % (tex(node.title), tex(node.props.get("where", "")),
                                             tex(node.need("when", "resume.md"))))
        if cv_text(node):
            out.append(tex(cv_text(node)) + r"\par")
        if parts:
            out.append(r"\begin{cvparts}")
            for p in parts:
                out.append(r"\cvpart{%s}{%s}{%s}" % (tex(p.title), tex(p.props.get("where", "")),
                                                    tex(p.props.get("when", ""))))
                if cv_text(p):
                    out.append(tex(cv_text(p)) + r"\par")
            out.append(r"\end{cvparts}")
    return r"\cvsection{%s}" % title + "\n" + "\n".join(out) if out else ""


def experience(docs, entries, counts) -> str:
    return resume(docs, "experience", "Experience")


def education(docs, entries, counts) -> str:
    return resume(docs, "education", "Education")


def publications_(docs, entries, counts) -> str:
    names = [n.strip() for n in docs["cv"].props.get("papers", "").split(",") if n.strip()]
    chosen = [build.paper(n, "cv.md: papers") for n in names] if names else entries
    # newest first; sorted() is stable, so reversing first puts later entries of a year on top
    chosen = sorted(reversed([e for e in entries if e in chosen]), key=lambda e: -int(e["fields"]["year"]))
    rows = []
    for e in chosen:
        f = e["fields"]
        authors = []
        for raw in publications.split_top_level(f["author"], r"\s+and\s+"):
            name = publications.format_author(raw)
            authors.append(r"{\color{black}%s}" % esc(name) if name == publications.ME else esc(name))
        title = esc(publications.latex_to_text(f["title"]))
        link = publications.link_of(f)
        detail = ", ".join(authors) + ". " + esc(publications.venue_of(f)) + "."
        label = f"{publications.latex_to_text(f.get('abbr', ''))} {f['year']}".strip()
        rows.append(r"\cvrow{\textcolor{accent}{%s}}{%s\newline{\small\color{muted}%s}}"
                    % (esc(label), href(link, title) if link else title, detail))
    if not rows:
        return ""
    heading = "Selected Publications" if len(chosen) < len(entries) else "Publications"
    return r"\cvsection{%s}" % heading + "\n" + "\n".join(rows)


def skills(docs, entries, counts) -> str:
    rows = []
    for card in docs["coding"].children:
        text = cv_text(card)
        if text is None:
            continue
        if not text:  # no cv: line, join the details of the card's rows
            text = "; ".join(item.rpartition(": ")[2] for item in build.list_items(card.body))
        rows.append(r"\cvrow{%s}{%s}" % (tex(card.title), tex(text)))
    if docs["cv"].props.get("languages"):
        rows.append(r"\cvrow{Spoken Languages}{%s}" % tex(docs["cv"].props["languages"]))
    return r"\cvsection{Skills}" + "\n" + "\n".join(rows) if rows else ""


def service(docs, entries, counts) -> str:
    rows = []
    for card in docs["service"].children:
        text = cv_text(card)
        if not text:
            continue
        labels = ", ".join(item.rpartition(": ")[0] or item for item in build.list_items(card.body))
        rows.append(r"\cvrow{%s}{%s}" % (tex(card.title), tex(fill(text, counts, labels))))
    return r"\cvsection{Leadership and Service}" + "\n" + "\n".join(rows) if rows else ""


def talks(docs, entries, counts) -> str:
    groups: dict[str, list[str]] = {}  # kind of talk -> its talks, newest first
    for t in build.newest_first(docs["talks"].children, "talks.md"):
        text = cv_text(t)
        if text is None:
            continue
        if not text:
            text = f'{t.need("where", "talks.md")}, {year_of(t.props["when"])}'
        groups.setdefault(t.need("type", "talks.md"), []).append(tex(text))
    rows = [r"\cvrow{%s}{%s}" % (tex(kind), "; ".join(items)) for kind, items in groups.items()]
    return r"\cvsection{Talks and Teaching}" + "\n" + "\n".join(rows) if rows else ""


RENDER = {"profile": profile, "numbers": numbers, "experience": experience, "education": education,
          "publications": publications_, "skills": skills, "service": service, "talks": talks}


def photo_of(cv: Node) -> Path | None:
    if not cv.props.get("photo"):
        return None
    path = ROOT / cv.props["photo"]
    if not path.exists():
        raise ContentError(f"cv.md: photo '{cv.props['photo']}' not found")
    return path


def document() -> tuple[str, Path | None]:
    entries = publications.load()
    build.ENTRIES[:] = entries
    docs = {name: build.parse(build.CONTENT / f"{name}.md")
            for name in ("cv", "home", "about", "resume", "talks", "service", "coding")}
    counts = counters(docs, entries)
    order = [s.strip().lower() for s in docs["cv"].props.get("sections", ",".join(SECTIONS)).split(",")]
    unknown = [s for s in order if s not in RENDER]
    if unknown:
        raise ContentError(f"cv.md: unknown section '{unknown[0]}', choose from {', '.join(SECTIONS)}")
    photo = photo_of(docs["cv"])
    body = [header(docs, bool(photo))] + [RENDER[s](docs, entries, counts) for s in order]
    source = (TEMPLATE.replace("<BODY>", "\n\n".join(b for b in body if b))
              .replace("<NAME>", tex(docs["cv"].need("name", "cv.md")))
              .replace("<DATE>", date.today().strftime("%B %Y")))
    return source, photo


def main() -> int:
    if not shutil.which("latexmk"):
        print("'latexmk' not found, install a TeX distribution (e.g. brew install texlive)")
        return 1
    try:
        source, photo = document()
    except publications.BibError as e:
        print(f"publications.bib has problems, no PDF was written:\n  {e}")
        return 1
    except (ContentError, FileNotFoundError) as e:
        print(f"{e}\nNo PDF was written.")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "cv.tex").write_text(source, encoding="utf-8")
        if photo:  # a small copy keeps the PDF light
            if shutil.which("magick"):
                subprocess.run(["magick", str(photo), "-resize", "600x", "-strip", "-quality", "88",
                                str(tmp / "photo.jpg")], check=True, stderr=subprocess.DEVNULL)
            else:
                shutil.copyfile(photo, tmp / f"photo{photo.suffix}")
        run = subprocess.run(native() + ["latexmk", "-pdf", "-interaction=nonstopmode",
                                         "-halt-on-error", "cv.tex"],
                             cwd=tmp, capture_output=True, text=True, errors="replace")
        pdf = tmp / "cv.pdf"
        if run.returncode != 0 or not pdf.exists():
            print("LaTeX failed, no PDF was written. End of the log:\n")
            print("\n".join((run.stdout + run.stderr).splitlines()[-40:]))
            return 1
        log = (tmp / "cv.log").read_text(encoding="utf-8", errors="replace")
        pages = int(m.group(1)) if (m := re.search(r"Output written on .*?\((\d+) page", log, re.S)) else 0
        OUT.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf, OUT)
    print(f"Wrote {OUT.relative_to(ROOT)} ({pages} pages)")
    if pages > MAX_PAGES:
        print(f"  ! longer than {MAX_PAGES} pages: shorten some `cv:` lines, list fewer `papers:` "
              f"in content/cv.md or set more entries to `cv: no`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
