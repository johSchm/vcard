#!/usr/bin/env python3
"""Build the website text into index.html.

    python3 tools/build.py

index.html only holds the layout. The text lives in content/*.md and the
publications in publications.bib; this script renders both and writes them
between the <!-- BUILD:name --> ... <!-- /BUILD:name --> markers in
index.html. Never edit between those markers by hand, it gets overwritten.

The Markdown format is described in content/README.md.
"""
import re
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publications  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PAGE = ROOT / "index.html"


class ContentError(Exception):
    pass


ENTRIES: list[dict] = []  # publications.bib, set in main(); lets the text link to papers


def paper(name: str, where: str) -> dict:
    """The publication called `name` (BibTeX key or PDF name, e.g. 'Schmidt2024b' or 'ITS')."""
    entry = publications.find(ENTRIES, name)
    if not entry:
        raise ContentError(f"{where}: paper '{name}' is neither a key nor a PDF name in publications.bib")
    return entry


# --- Markdown parsing -------------------------------------------------------
#
# A file (and every `## entry` / `### part` in it) may start with
# `key: value` lines, followed by ordinary Markdown.

PROP = re.compile(r"^([a-z][a-z_]*):\s+(.*\S)\s*$")


class Node:
    def __init__(self, title: str | None = None, line: int = 0):
        self.title, self.line = title, line
        self.props: dict[str, str] = {}
        self.body: list[str] = []
        self.children: list["Node"] = []

    def need(self, key: str, file: str) -> str:
        if key not in self.props:
            where = f"'{self.title}'" if self.title else "the top of the file"
            raise ContentError(f"{file}: {where} (line {self.line}) needs a '{key}: ...' line")
        return self.props[key]


def parse(path: Path) -> Node:
    doc = Node(line=1)
    current, reading_props = doc, True
    text = path.read_text(encoding="utf-8")
    # drop <!-- comments --> but keep their newlines so line numbers stay right
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        heading = re.match(r"^(##|###)\s+(.*)$", line)
        if heading:
            node = Node(heading.group(2).strip(), n)
            if heading.group(1) == "##":
                doc.children.append(node)
            else:
                (doc.children[-1] if doc.children else doc).children.append(node)
            current, reading_props = node, True
            continue
        if reading_props:
            m = PROP.match(line)
            if m:
                current.props[m.group(1)] = m.group(2)
                continue
            if not line and not current.props and not current.body:
                continue
            reading_props = False
        current.body.append(line)
    return doc


def inline(text: str) -> str:
    """Escape text and apply **bold**, *highlight*, [links](url), [links](paper:Key) and line breaks
    (written as \\\\, \\n or <br>)."""
    s = escape(text, quote=False)
    s = re.sub(r"\s*(?:\\\\|\\n|&lt;br\s*/?&gt;)\s*", "<br>", s, flags=re.I)

    def link(m):
        label, url = m.group(1), m.group(2)
        if url.startswith("paper:"):  # jumps to the publication's card
            entry = paper(url[6:], f"link '[{label}]({url})'")
            title = escape(publications.latex_to_text(entry["fields"]["title"]))
            return f'<a class="pub-jump" href="#{publications.anchor_of(entry)}" title="{title}">{label}</a>'
        external = url.startswith(("http://", "https://"))
        attrs = ' target="_blank" rel="noopener"' if external else ""
        if url.startswith("#"):
            attrs = ' class="smooth-scroll"'  # same animated scroll as the menu
        return f'<a href="{escape(url)}"{attrs}>{label}</a>'

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r'<span class="text-primary">\1</span>', s)
    return s


def blocks(lines: list[str]) -> list[tuple[str, object]]:
    """Group body lines into ('p', text), ('ul'|'ol', [items]) and ('h', text)."""
    out, para = [], []

    def flush():
        if para:
            out.append(("p", " ".join(para)))
            para.clear()

    for line in lines:
        s = line.strip()
        item = re.match(r"^(-|\d+\.)\s+(.*)$", s)
        if not s:
            flush()
        elif s.startswith("#### "):
            flush()
            out.append(("h", s[5:].strip()))
        elif item:
            flush()
            kind = "ul" if item.group(1) == "-" else "ol"
            if out and out[-1][0] == kind:
                out[-1][1].append(item.group(2))
            else:
                out.append((kind, [item.group(2)]))
        elif out and out[-1][0] in ("ul", "ol") and not para and line.startswith("  "):
            out[-1][1][-1] += " " + s  # indented continuation of a list item
        else:
            para.append(s)
    flush()
    return out


def prose(lines: list[str], p_class: str) -> str:
    html = []
    for kind, data in blocks(lines):
        if kind == "p":
            html.append(f'<p class="{p_class}">{inline(data)}</p>')
        elif kind == "h":
            html.append(f'<h5 class="text-white text-4 mt-4">{inline(data)}</h5>')
        else:
            items = "\n".join(f"  <li>{inline(i)}</li>" for i in data)
            html.append(f'<{kind} class="lh-lg">\n{items}\n</{kind}>')
    return "\n".join(html)


MONTHS = {m: n for n, m in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), 1)}
MONTHS.update(winter=10, summer=4)  # semesters start in October / April


def newest_first(nodes: list[Node], f: str) -> list[Node]:
    """Sort cards by their `when:` date ("March 2026", "Winter Semester 2024/25", "2024"), newest first."""
    def key(node: Node) -> tuple[int, int]:
        when = node.need("when", f)
        year = re.search(r"\d{4}", when)
        if not year:
            raise ContentError(f"{f}: '{node.title}' (line {node.line}) needs a year in 'when: {when}'")
        month = next((n for word in re.findall(r"[a-z]+", when.lower())
                      for m, n in MONTHS.items() if word.startswith(m)), 0)
        return int(year.group(0)), month
    return sorted(nodes, key=key, reverse=True)  # stable: same date keeps the file's order


def list_items(lines: list[str]) -> list[str]:
    return [item for kind, data in blocks(lines) if kind in ("ul", "ol") for item in data]


# --- Sections ---------------------------------------------------------------

def home(doc: Node, f: str) -> str:
    typed = "\n".join(f"  <p>{inline(t)}</p>" for t in list_items(doc.body))
    if not typed:
        raise ContentError(f"{f}: add the rotating hero lines as a '- ...' list")
    return f"""<div class="typed-strings">
{typed}
</div>
<p class="text-7 fw-500 text-white mb-2 mb-md-3">{inline(doc.need("greeting", f))}</p>
<h2 class="text-16 fw-600 text-white mb-2 mb-md-3"><span class="typed"></span></h2>
<p class="text-5 text-light mb-4">{inline(doc.need("tagline", f))}</p>
{contact_button(doc, f)}"""


def contact_button(doc: Node, f: str) -> str:
    """'Get in contact' button that reveals LinkedIn / email options."""
    options = []
    if doc.props.get("linkedin"):
        options.append(f'<a class="btn btn-sm rounded-pill shadow-none contact-option" href="{escape(doc.props["linkedin"])}" '
                       f'target="_blank" rel="noopener" tabindex="-1"><i class="fab fa-linkedin me-2"></i>LinkedIn</a>')
    if doc.props.get("email"):
        # the address is assembled in the browser on click (shown + copied), so it
        # isn't sitting in the HTML for spam bots
        user, _, domain = doc.props["email"].partition("@")
        if not domain:
            raise ContentError(f"{f}: email must look like name@domain")
        options.append(f'<button class="btn btn-sm rounded-pill shadow-none contact-option contact-email" type="button" '
                       f'data-user="{escape(user[::-1])}" data-domain="{escape(domain[::-1])}" tabindex="-1">'
                       f'<i class="fas fa-envelope me-2"></i><span>Email</span></button>')
    if not options:
        raise ContentError(f"{f}: add at least one of 'linkedin: ...' or 'email: ...' for the contact button")
    buttons = "\n".join("    " + o for o in options)
    return f"""<div class="hero-contact mt-2">
  <button class="btn rounded-pill shadow-none hero-contact-toggle" type="button" aria-expanded="false" aria-controls="hero-contact-options">{inline(doc.need("button", f))}</button>
  <div class="hero-contact-options" id="hero-contact-options">
{buttons}
  </div>
</div>"""


def about_intro(doc: Node, f: str) -> str:
    return (f'<h2 class="text-7 text-white fw-600 mb-3">{inline(doc.need("heading", f))}</h2>\n'
            + prose(doc.body, "text-white-50"))


def about_stats(doc: Node, f: str, counts: dict[str, int]) -> str:
    stats = next((c for c in doc.children if c.title.lower() == "numbers"), None)
    if not stats:
        return ""
    cols = []
    for item in list_items(stats.body):
        for name, value in counts.items():  # {publications}, {reviewed}, {theses}
            item = item.replace("{" + name + "}", str(value))
        # {years since 2014}: filled in now and kept current by the script below the counters
        since = ""
        if y := re.match(r"^\{years since (\d{4})\}", item):
            since = f' data-since="{y.group(1)}"'
            item = str(max(date.today().year - int(y.group(1)), 0)) + item[y.end():]
        m = re.match(r"^(\d+)(\+?)\s+(.+)$", item)
        if not m:
            raise ContentError(f"{f}: numbers must look like '- 10+ Years Coding Experience', "
                               f"'- {{years since 2014}}+ Years ...' or '- {{publications}} Papers ...', got '{item}'")
        num, plus, label = m.groups()
        cols.append(f"""<div class="col-6 col-md-3">
  <div class="featured-box text-center">
    <h4 class="text-12 text-white-50 mb-0"><span class="counter" data-from="0" data-to="{num}"{since}>{num}</span>{plus}</h4>
    <p class="text-light mb-0">{inline(label)}</p>
  </div>
</div>""")
    return '<div class="row">\n' + indent("\n".join(cols), 2) + "\n</div>"


def paper_tags(node: Node, f: str, entries: list[dict]) -> str:
    """Row of tags for `papers:` / `paper:` (each jumps to the publication's card) and `status:`."""
    tags = []
    names = ",".join(node.props.get(k, "") for k in ("papers", "paper"))
    for name in filter(None, (n.strip() for n in names.split(","))):
        tags.append(publications.ref(paper(name, f"{f}: '{node.title}' (line {node.line})")))
    if node.props.get("status"):
        tags.append(f'<span class="pub-ref is-pending"><i class="far fa-clock"></i>{inline(node.props["status"])}</span>')
    return f'<p class="pub-refs">{" ".join(tags)}</p>' if tags else ""


def resume(doc: Node, f: str, entries: list[dict]) -> str:
    cards = []
    for e in doc.children:
        parts = [f'<p class="text-primary">{inline(e.need("where", f))}</p>',
                 paper_tags(e, f, entries),
                 prose(e.body, "text-white-50 mb-0")]
        for sub in e.children:
            when = (f' <span class="badge bg-danger text-2 fw-400 align-middle ms-1">{inline(sub.props["when"])}</span>'
                    if "when" in sub.props else "")
            parts.append(f'<h3 class="text-5 text-white mt-4">{inline(sub.title)}{when}</h3>')
            if "where" in sub.props:
                parts.append(f'<p class="text-primary">{inline(sub.props["where"])}</p>')
            parts.append(paper_tags(sub, f, entries))
            parts.append(prose(sub.body, "text-white-50 mb-0"))
        details = indent("\n".join(p for p in parts if p), 4)
        kind = (f' <p class="badge bg-secondary text-2 fw-400 mb-2">{inline(e.props["type"])}</p>'
                if "type" in e.props else "")
        cards.append(f"""<div class="bg-dark rounded p-4 mb-4 resume-card">
  <div class="resume-card-header" role="button" tabindex="0" aria-expanded="false">
    <div>
      <p class="badge bg-danger text-2 fw-400 mb-2">{inline(e.need("when", f))}</p>{kind}
      <h3 class="text-5 text-white mb-0">{inline(e.title)}</h3>
    </div>
    <i class="fas fa-chevron-down resume-card-icon"></i>
  </div>
  <div class="resume-card-body">
    <div class="resume-card-inner">
{details}
    </div>
  </div>
</div>""")
    return "\n".join(cards)


# Animated figures for the thesis intro (`figure: <name>` in thesis.md).
# The animation itself lives in js/canon-viz.js.
FIGURES = {
    "canonicalization": """<figure class="canon-viz bg-dark rounded p-4 mb-4">
  <canvas role="img" aria-label="A wire-frame surface over the input space. The frozen model solves the problem only in the highlighted training region. Test queries come from another region, and canonicalization maps all of them along trajectories to the same spot in the training region."></canvas>
  <figcaption>
    <ol class="canon-viz-steps">
      <li class="canon-viz-step"><span class="canon-viz-step-num">01</span><span class="canon-viz-step-title">Training</span><span class="canon-viz-step-text">The model solves the problem in the region it was trained on.</span></li>
      <li class="canon-viz-step"><span class="canon-viz-step-num">02</span><span class="canon-viz-step-title">Testing</span><span class="canon-viz-step-text">Queries come from a region the model has never seen, and it fails on them.</span></li>
      <li class="canon-viz-step"><span class="canon-viz-step-num">03</span><span class="canon-viz-step-title">Canonicalization</span><span class="canon-viz-step-text">The whole test region is mapped to one spot in the training region. The model stays frozen.</span></li>
    </ol>
  </figcaption>
</figure>""",
}


def thesis(doc: Node, f: str, entries: list[dict]) -> str:
    where = doc.props.get("where")
    parts = [f'<h3 class="text-white {"mb-2" if where else "mb-4"}">{inline(doc.need("title", f))}</h3>']
    if where:
        parts.append(f'<p class="text-primary mb-4">{inline(where)}</p>')
    parts.append(prose(doc.body, "text-white-50 mb-4"))
    figure = doc.props.get("figure")
    if figure:
        if figure not in FIGURES:
            raise ContentError(f"{f}: unknown figure '{figure}', use one of: {', '.join(FIGURES)}")
        parts.append(FIGURES[figure])
    if doc.children:
        parts.append(f'<h4 class="text-6 text-white fw-600 mt-5 mb-4">'
                     f'{inline(doc.props.get("heading", "Main contributions"))}</h4>')
    for n, e in enumerate(doc.children, 1):
        refs = paper_tags(e, f, entries)
        refs = f"\n  {refs}" if refs else ""
        parts.append(f"""<div class="thesis-card bg-dark rounded p-4 mb-4">
  <div class="thesis-card-head">
    <span class="thesis-card-num" aria-hidden="true">{n:02d}</span>
    <h3 class="text-5 text-white mb-0">{inline(e.title)}</h3>
  </div>{refs}
{indent(prose(e.body, "text-white-50 mb-0"), 2)}
</div>""")
    return "\n".join(p for p in parts if p)


def coding_intro(doc: Node, f: str) -> str:
    return prose(doc.body, "text-white-50 mb-0")


def coding(doc: Node, f: str) -> str:
    cards = []
    for e in doc.children:
        icon = f'<i class="{escape(e.need("icon", f))}"></i>'
        if e.props.get("link"):
            icon = f'<a href="{escape(e.props["link"])}" target="_blank" rel="noopener">{icon}</a>'
        cards.append(f"""<div class="coding-card bg-dark rounded p-4 mb-4">
  <div class="featured-box style-3">
    <div class="featured-box-icon text-primary bg-dark-1 shadow-sm rounded">
      {icon}
    </div>
    <p class="text-primary-50 mb-0">{inline(e.need("when", f))}</p>
    <h3 class="text-white">{inline(e.title)}</h3>
{indent(chr(10).join(card_body(e.body)), 4)}
  </div>
</div>""")
    return "\n".join(cards)


def ai_intro(doc: Node, f: str) -> str:
    return (f'<h3 class="ai-lead text-white text-center mb-3">{inline(doc.need("lead", f))}</h3>\n'
            + prose(doc.body, "text-white-50 text-center mb-5"))


def ai(doc: Node, f: str) -> str:
    """Principle cards, three per row: number, icon, title, one sentence, short points."""
    cols = []
    for n, e in enumerate(doc.children, 1):
        parts = []
        for kind, data in blocks(e.body):
            if kind == "p":
                parts.append(f'<p class="text-white-50 mb-3">{inline(data)}</p>')
            elif kind in ("ul", "ol"):
                items = "\n".join(f"  <li>{inline(i)}</li>" for i in data)
                parts.append(f'<ul class="ai-points list-unstyled mb-0">\n{items}\n</ul>')
        cols.append(f"""<div class="col-lg-4">
  <div class="ai-card bg-dark rounded p-4 h-100">
    <div class="ai-card-head">
      <span class="ai-card-icon text-primary bg-dark-1 shadow-sm rounded"><i class="{escape(e.need("icon", f))}"></i></span>
      <span class="ai-card-num" aria-hidden="true">{n:02d}</span>
    </div>
    <h3 class="text-5 text-white mt-4 mb-2">{inline(e.title)}</h3>
{indent(chr(10).join(parts), 4)}
  </div>
</div>""")
    return '<div class="ai-grid row g-4">\n' + indent("\n".join(cols), 2) + "\n</div>"


def talks_intro(doc: Node, f: str) -> str:
    return prose(doc.body, "text-white-50 mb-5")


# icon per kind of talk, picked by the first keyword found in `type:`
TALK_ICONS = (
    (("training", "certificate"), "fas fa-award"),
    (("video", "recording"), "fas fa-play"),
    (("seminar", "lecture", "course", "teaching"), "fas fa-chalkboard-teacher"),
    (("oral", "conference", "workshop"), "fas fa-users"),
)
TALK_LINKS = (  # setting, label, icon
    ("video", "Watch video", "fas fa-play"),
    ("slides", "Slides", "fas fa-images"),
    ("link", "Event", "fas fa-external-link-alt"),
)


def talks(doc: Node, f: str) -> str:
    cards = []
    for e in newest_first(doc.children, f):
        kind = e.need("type", f)
        icon_class = e.props.get("icon") or next(
            (icon for words, icon in TALK_ICONS if any(w in kind.lower() for w in words)),
            "fas fa-microphone-alt")
        icon = f'<i class="{escape(icon_class)}"></i>'
        main = e.props.get("video") or e.props.get("link")
        if main:
            icon = f'<a href="{escape(main)}" target="_blank" rel="noopener" aria-label="{escape(e.title)}">{icon}</a>'
        links = "\n".join(
            f'  <a href="{escape(e.props[key])}" target="_blank" rel="noopener"><i class="{cls}"></i>{label}</a>'
            for key, label, cls in TALK_LINKS if e.props.get(key))
        parts = [f'<p class="text-primary mb-0">{inline(e.need("where", f))}</p>',
                 paper_tags(e, f, ENTRIES),
                 prose(e.body, "text-white-50 mt-2 mb-0"),
                 f'<div class="talk-links">\n{links}\n</div>' if links else ""]
        cards.append(f"""<div class="talk-card bg-dark rounded p-4 mb-4">
  <div class="featured-box style-3">
    <div class="featured-box-icon text-primary bg-dark-1 shadow-sm rounded">
      {icon}
    </div>
    <p class="mb-2"><span class="badge bg-danger text-2 fw-400">{inline(e.need("when", f))}</span> <span class="badge bg-secondary text-2 fw-400">{inline(kind)}</span></p>
    <h3 class="text-5 text-white mb-2">{inline(e.title)}</h3>
{indent(chr(10).join(p for p in parts if p), 4)}
  </div>
</div>""")
    return "\n".join(cards)


def service_intro(doc: Node, f: str) -> str:
    return prose(doc.body, "text-white-50 mb-5")


def tag_rows(items: list[str]) -> str:
    """'- Label: detail' lines as rows with the label as a tag."""
    rows = []
    for item in items:
        label, sep, detail = item.rpartition(": ")
        if not sep:
            label, detail = item, ""
        rows.append(f'  <li><span class="pub-ref">{inline(label)}</span><span>{inline(detail)}</span></li>')
    return '<ul class="tag-rows list-unstyled text-white-50">\n' + "\n".join(rows) + "\n</ul>"


def card_body(lines: list[str]) -> list[str]:
    """Card text: paragraphs, and '- Label: detail' lists as tag rows."""
    parts = []
    for kind, data in blocks(lines):
        if kind == "p":
            parts.append(f'<p class="text-white-50">{inline(data)}</p>')
        elif kind in ("ul", "ol"):
            parts.append(tag_rows(data))
    return parts


def thesis_list(card: Node, f: str, first_id: int) -> str:
    """Supervised theses: title, date and partner; the abstract unfolds on click."""
    items = []
    for n, t in enumerate(newest_first(card.children, f), first_id):
        meta = f'{inline(t.need("when", f))} · {inline(t.need("type", f))} thesis'
        if t.props.get("with"):
            meta += f' · with {inline(t.props["with"])}'
        text = (f'<span class="thesis-item-text">\n'
                f'      <span class="thesis-item-title">{inline(t.title)}</span>\n'
                f'      <span class="thesis-item-meta">{meta}</span>\n'
                f'    </span>')
        abstract = " ".join(data for kind, data in blocks(t.body) if kind == "p")
        if abstract:
            items.append(f"""<li class="thesis-item">
  <button class="thesis-item-head" type="button" aria-expanded="false" aria-controls="thesis-abstract-{n}">
    {text}
    <i class="fas fa-chevron-down" aria-hidden="true"></i>
  </button>
  <div class="pub-panel" id="thesis-abstract-{n}">
    <div class="pub-panel-inner">
      <p class="pub-abstract">{inline(abstract)}</p>
    </div>
  </div>
</li>""")
        else:
            items.append(f"""<li class="thesis-item">
  <div class="thesis-item-head">
    {text}
  </div>
</li>""")
    return '<ul class="thesis-list list-unstyled">\n' + indent("\n".join(items), 2) + "\n</ul>"


def service(doc: Node, f: str) -> str:
    cards, n_theses = [], 0
    for e in doc.children:
        parts = card_body(e.body)
        if e.children:
            parts.append(thesis_list(e, f, n_theses))
            n_theses += len(e.children)
        when = (f'    <p class="mb-2"><span class="badge bg-danger text-2 fw-400">{inline(e.props["when"])}</span></p>\n'
                if "when" in e.props else "")
        cards.append(f"""<div class="service-card bg-dark rounded p-4 mb-4">
  <div class="featured-box style-3">
    <div class="featured-box-icon text-primary bg-dark-1 shadow-sm rounded">
      <i class="{escape(e.need("icon", f))}"></i>
    </div>
{when}    <h3 class="text-5 text-white mb-3">{inline(e.title)}</h3>
{indent(chr(10).join(parts), 4)}
  </div>
</div>""")
    return "\n".join(cards)


def service_counts(doc: Node) -> dict[str, int]:
    """Numbers for the counters in about.md."""
    reviewed = sum(int(m.group(1))
                   for e in doc.children if e.title.lower() == "reviewing"
                   for item in list_items(e.body)
                   if (m := re.search(r":\s+(\d+)\b", item)))
    return {"reviewed": reviewed, "theses": sum(len(e.children) for e in doc.children)}


def legal(doc: Node, f: str) -> str:
    modals = []
    for e in doc.children:
        parts = [prose(e.body, "")]
        for sub in e.children:
            parts.append(f'<h3 class="text-white mb-3 mt-4">{inline(sub.title)}</h3>')
            parts.append(prose(sub.body, ""))
        body = indent("\n".join(p for p in parts if p).replace(' class=""', ""), 6)
        modals.append(f"""<div id="{escape(e.need("id", f))}" class="modal fade" role="dialog" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
    <div class="modal-content bg-dark-2 text-light">
      <div class="modal-header border-secondary">
        <h5 class="modal-title text-white">{inline(e.title)}</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body p-4">
{body}
      </div>
    </div>
  </div>
</div>""")
    return "\n".join(modals)


# --- Writing into index.html --------------------------------------------------

def indent(html: str, n: int) -> str:
    """Indent every line by n spaces, except inside <pre> where whitespace matters."""
    out, in_pre = [], False
    for line in html.splitlines():
        in_pre = in_pre or line.lstrip().startswith("<pre>")
        out.append(line if in_pre or not line else " " * n + line)
        in_pre = in_pre and "</pre>" not in line
    return "\n".join(out)


def fill(page: str, name: str, source: str, html: str) -> str:
    n = re.escape(name)
    pattern = re.compile(rf"^([ \t]*)<!-- BUILD:{n}(?: [^\n]*?)? -->\n.*?^[ \t]*<!-- /BUILD:{n} -->",
                         re.S | re.M)
    m = pattern.search(page)
    if not m:
        raise ContentError(f"index.html: markers for '{name}' not found")
    pad = m.group(1)
    block = (f"{pad}<!-- BUILD:{name} (generated from {source}, do not edit here) -->\n"
             + (indent(html, len(pad)) + "\n" if html else "")
             + f"{pad}<!-- /BUILD:{name} -->")
    return page[:m.start()] + block + page[m.end():]


def main() -> int:
    try:
        entries = publications.load()
        ENTRIES[:] = entries
        docs = {name: parse(CONTENT / f"{name}.md")
                for name in ("home", "about", "resume", "thesis", "talks", "service", "coding", "ai", "legal")}
        sections = [
            ("home", "content/home.md", home(docs["home"], "home.md")),
            ("about", "content/about.md", about_intro(docs["about"], "about.md")),
            ("about-numbers", "content/about.md", about_stats(docs["about"], "about.md", {
                "publications": len(entries), **service_counts(docs["service"])})),
            ("resume", "content/resume.md", resume(docs["resume"], "resume.md", entries)),
            ("thesis", "content/thesis.md", thesis(docs["thesis"], "thesis.md", entries)),
            ("talks-intro", "content/talks.md", talks_intro(docs["talks"], "talks.md")),
            ("talks", "content/talks.md", talks(docs["talks"], "talks.md")),
            ("service-intro", "content/service.md", service_intro(docs["service"], "service.md")),
            ("service", "content/service.md", service(docs["service"], "service.md")),
            ("coding-intro", "content/coding.md", coding_intro(docs["coding"], "coding.md")),
            ("coding", "content/coding.md", coding(docs["coding"], "coding.md")),
            ("ai-intro", "content/ai.md", ai_intro(docs["ai"], "ai.md")),
            ("ai", "content/ai.md", ai(docs["ai"], "ai.md")),
            ("publications", "publications.bib", publications.render(entries)),
            ("legal", "content/legal.md", legal(docs["legal"], "legal.md")),
        ]
        page = PAGE.read_text(encoding="utf-8")
        for name, source, html in sections:
            page = fill(page, name, source, html)
    except publications.BibError as e:
        print(f"publications.bib has problems, index.html was not changed:\n  {e}")
        return 1
    except (ContentError, FileNotFoundError) as e:
        print(f"{e}\nindex.html was not changed.")
        return 1
    PAGE.write_text(page, encoding="utf-8")
    print(f"Built index.html ({len(entries)} publications)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
