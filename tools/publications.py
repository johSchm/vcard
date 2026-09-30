"""Publications section: cards rendered from publications.bib (used by build.py).

For every entry in publications.bib:
  1. if it has a `pdf` field (a file in res/papers/), render that PDF's first
     page to images/publications/<pdf name>.webp (skipped when up to date)
  2. render a card for it, including a copyable BibTeX block

Required fields: title, author, year. The venue comes from booktitle,
journal, howpublished or note. An `abstract` adds an "Abstract" panel to
the card, a `code` URL (e.g. a GitHub repo) activates the "Code" link. The
fields abbr, pdf, abstract and code are used for the card only and left out
of the copyable BibTeX. Cards are ordered by year, oldest first; entries from the same year keep their order from the file.

Requires: pdftoppm (poppler), magick (ImageMagick)
"""
import re
import subprocess
import tempfile
import unicodedata
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "publications.bib"
PAPERS = ROOT / "res" / "papers"
THUMBS = ROOT / "images" / "publications"

INDENT = ""  # build.py indents the block to match its markers
ME = "J. Schmidt"
REQUIRED = ("title", "author", "year")
CARD_ONLY_FIELDS = {"abbr", "pdf", "abstract", "code"}


# --- BibTeX parsing ---------------------------------------------------------

class BibError(Exception):
    pass


def _read_value(text: str, i: int) -> tuple[str, int]:
    """Read a field value starting at text[i]; return (raw value, index after it)."""
    if text[i] == "{":
        depth, j = 0, i
        while j < len(text):
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            if depth == 0:
                return text[i + 1:j], j + 1
            j += 1
        raise BibError("unbalanced braces")
    if text[i] == '"':
        depth, j = 0, i + 1
        while j < len(text):
            c = text[j]
            depth += {"{": 1, "}": -1}.get(c, 0)
            if c == '"' and depth == 0:
                return text[i + 1:j], j + 1
            j += 1
        raise BibError("unterminated quote")
    m = re.compile(r"[\w.+-]+").match(text, i)
    if not m:
        raise BibError(f"unexpected character {text[i]!r}")
    return m.group(0), m.end()


def parse_bib(text: str) -> list[dict]:
    entries = []
    for m in re.finditer(r"@\s*(\w+)\s*\{", text):
        kind = m.group(1).lower()
        if kind in ("comment", "string", "preamble"):
            continue
        i = m.end()
        key_end = text.index(",", i)
        key = text[i:key_end].strip()
        line = text.count("\n", 0, m.start()) + 1
        fields, i = {}, key_end + 1
        try:
            while True:
                while i < len(text) and text[i] in " \t\r\n,":
                    i += 1
                if text[i] == "}":
                    break
                fm = re.compile(r"([\w-]+)\s*=\s*").match(text, i)
                if not fm:
                    raise BibError(f"expected 'field = value' near {text[i:i + 20]!r}")
                value, i = _read_value(text, fm.end())
                fields[fm.group(1).lower()] = " ".join(value.split())
        except (BibError, IndexError) as e:
            raise BibError(f"line {line}, entry '{key}': {e or 'unexpected end of file'}")
        entries.append({"type": kind, "key": key, "fields": fields, "line": line})
    return entries


# --- LaTeX -> text ----------------------------------------------------------

_ACCENTS = {'"': "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303",
            "=": "\u0304", ".": "\u0307", "c": "\u0327", "u": "\u0306", "v": "\u030c",
            "H": "\u030b", "k": "\u0328"}
_SYMBOLS = {"ss": "ß", "o": "ø", "O": "Ø", "ae": "æ", "AE": "Æ", "aa": "å", "AA": "Å",
            "l": "ł", "L": "Ł", "i": "ı", "&": "&", "%": "%", "_": "_", "$": "$", "#": "#"}


def latex_to_text(s: str) -> str:
    accent = lambda m: m.group(2) + _ACCENTS[m.group(1)]
    s = re.sub(r"""\\(["'`^~=.])\s*\{?\s*([A-Za-z])\s*\}?""", accent, s)
    s = re.sub(r"\\([cuvHk])\s*\{\s*([A-Za-z])\s*\}", accent, s)
    s = re.sub(r"\\([cuvHk])\s+([A-Za-z])", accent, s)
    s = re.sub(r"\\(ss|ae|AE|aa|AA|[oOlLi])(?![A-Za-z])\s*", lambda m: _SYMBOLS[m.group(1)], s)
    s = re.sub(r"\\([&%_$#])", lambda m: _SYMBOLS[m.group(1)], s)
    s = s.replace("---", "\u2014").replace("--", "\u2013").replace("~", "\u00a0")
    s = s.replace("{", "").replace("}", "")
    return unicodedata.normalize("NFC", " ".join(s.split()))


def split_top_level(s: str, sep: str) -> list[str]:
    """Split on a regex separator, ignoring matches inside braces."""
    parts, depth, start = [], 0, 0
    for i, c in enumerate(s):
        depth += {"{": 1, "}": -1}.get(c, 0)
        if depth == 0:
            m = re.compile(sep).match(s, i)
            if m and m.start() == i:
                parts.append(s[start:i])
                start = m.end()
    parts.append(s[start:])
    return [p.strip() for p in parts if p.strip()]


def format_author(raw: str) -> str:
    """'Schmidt, Johann' / 'Johann Schmidt' -> 'J. Schmidt'."""
    if raw.startswith("{") and raw.endswith("}"):
        return latex_to_text(raw)  # organisation name
    if "," in raw:
        last, first = [p.strip() for p in raw.split(",", 1)]
    else:
        *first, last = split_top_level(raw, r"\s+")
        first = " ".join(first)
    initials = " ".join("-".join(p[0] + "." for p in word.split("-") if p)
                        for word in latex_to_text(first).split())
    return f"{initials} {latex_to_text(last)}".strip()


def format_authors(field: str) -> str:
    names = split_top_level(field, r"\s+and\s+")
    et_al = names and names[-1].lower() == "others"
    names = [format_author(n) for n in names if n.lower() != "others"]
    names = [escape(n) for n in names]
    names = [f'<strong class="text-white fw-500">{n}</strong>' if n == ME else n for n in names]
    if et_al:
        return ", ".join(names) + " et al."
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


# --- Card rendering ---------------------------------------------------------

def venue_of(f: dict) -> str:
    for field in ("booktitle", "journal", "howpublished", "note", "publisher"):
        if f.get(field):
            return latex_to_text(f[field])
    if f.get("archiveprefix", "").lower() == "arxiv" and f.get("eprint"):
        return f"arXiv preprint arXiv:{f['eprint']}"
    return ""


def link_of(f: dict) -> str:
    if f.get("url"):
        return f["url"]
    if f.get("doi"):
        return "https://doi.org/" + re.sub(r"^https?://(dx\.)?doi\.org/", "", f["doi"])
    if f.get("eprint") and f.get("archiveprefix", "arxiv").lower() == "arxiv":
        return "https://arxiv.org/abs/" + f["eprint"]
    return ""


def bibtex_of(entry: dict) -> str:
    fields = {k: v for k, v in entry["fields"].items() if k not in CARD_ONLY_FIELDS and v}
    width = max(len(k) for k in fields)
    body = ",\n".join(f"  {k.ljust(width)} = {{{v}}}" for k, v in fields.items())
    return f"@{entry['type']}{{{entry['key']},\n{body}\n}}"


def find(entries: list[dict], name: str) -> dict | None:
    """Entry with this BibTeX key, or whose `pdf` is <name>.pdf (e.g. 'Schmidt2024b' or 'ITS')."""
    wanted = name.strip().lower()
    for e in entries:
        if e["key"].lower() == wanted or Path(e["fields"].get("pdf", "")).stem.lower() == wanted:
            return e
    return None


def anchor_of(entry: dict) -> str:
    """id of the entry's card, so other sections can link to it."""
    return "pub-" + re.sub(r"[^\w-]", "-", entry["key"])


def ref(entry: dict) -> str:
    """Small tag like 'ICML 2024' that jumps to the entry's card (used by the thesis section)."""
    f = entry["fields"]
    title = escape(latex_to_text(f["title"]))
    label = escape(f"{latex_to_text(f.get('abbr', ''))} {latex_to_text(f['year'])}".strip())
    return (f'<a class="pub-ref" href="#{anchor_of(entry)}" title="{title}" '
            f'aria-label="{label}, go to publication: {title}"><i class="fas fa-file-alt"></i>{label}</a>')


def render_preview(pdf: Path) -> Path:
    thumb = THUMBS / (pdf.stem + ".webp")
    if thumb.exists() and thumb.stat().st_mtime >= pdf.stat().st_mtime:
        return thumb
    THUMBS.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "page"
        # 300px wide = 2x the 150px display width, crisp on retina screens
        subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-singlefile", "-png",
                        "-scale-to-x", "300", "-scale-to-y", "-1", str(pdf), str(png)],
                       check=True, stderr=subprocess.DEVNULL)
        subprocess.run(["magick", f"{png}.png", "-strip", "-quality", "82", str(thumb)],
                       check=True)
    print(f"  rendered preview {thumb.relative_to(ROOT)}")
    return thumb


def card(entry: dict, thumb: Path | None) -> str:
    f = entry["fields"]
    title = escape(latex_to_text(f["title"]))
    link = escape(link_of(f))
    venue = escape(venue_of(f))
    abbr = latex_to_text(f.get("abbr", ""))
    if not abbr and (m := re.search(r"\(([^()]+)\)\s*$", venue)):
        abbr = m.group(1)
    uid = re.sub(r"[^\w-]", "-", entry["key"])

    badges = f'<span class="badge bg-danger text-2 fw-400">{escape(latex_to_text(f["year"]))}</span>'
    if abbr:
        badges += f' <span class="badge bg-secondary text-2 fw-400">{escape(abbr)}</span>'

    icon = '<i class="fas fa-file-alt"></i>'
    img = ""
    if thumb:
        src = escape(quote(thumb.relative_to(ROOT).as_posix()))
        img = f'\n    <img src="{src}" alt="First page of {title}" loading="lazy" onerror="this.remove()">'
    if link:
        preview = (f'<a class="pub-thumb" href="{link}" target="_blank" rel="noopener" '
                   f'aria-label="Open paper: {title}">\n    {icon}{img}\n  </a>')
        read = f'\n      <a class="pub-link" href="{link}" target="_blank" rel="noopener">Read paper <i class="fas fa-arrow-right"></i></a>'
    else:
        preview = f'<div class="pub-thumb">\n    {icon}{img}\n  </div>'
        read = ""
    venue_html = f'\n    <p class="pub-venue text-primary mb-0">{venue}</p>' if venue else ""

    if f.get("code"):
        code = (f'\n      <a class="pub-code" href="{escape(f["code"])}" target="_blank" rel="noopener">'
                f'<i class="fab fa-github"></i>Code</a>')
    else:
        code = ('\n      <span class="pub-code is-disabled" aria-disabled="true" title="Code not available">'
                '<i class="fab fa-github"></i>Code</span>')

    toggles, panels = "", ""
    if f.get("abstract"):
        toggles += (f'\n      <button class="pub-panel-toggle" type="button" aria-expanded="false" '
                    f'aria-controls="abstract-{uid}"><i class="fas fa-align-left"></i>Abstract</button>')
        panels += f"""
  <div class="pub-panel" id="abstract-{uid}">
    <div class="pub-panel-inner">
      <p class="pub-abstract">{escape(latex_to_text(f["abstract"]))}</p>
    </div>
  </div>"""
    toggles += (f'\n      <button class="pub-panel-toggle" type="button" aria-expanded="false" '
                f'aria-controls="bib-{uid}"><i class="fas fa-quote-right"></i>BibTeX</button>')
    panels += f"""
  <div class="pub-panel" id="bib-{uid}">
    <div class="pub-panel-inner">
      <div class="pub-bib-box">
        <button class="pub-bib-copy" type="button"><i class="far fa-copy"></i><span>Copy</span></button>
<pre><code>{escape(bibtex_of(entry))}</code></pre>
      </div>
    </div>
  </div>"""

    html = f"""<article class="pub-card bg-dark rounded p-3 p-md-4 mb-4" id="{anchor_of(entry)}">
  {preview}
  <div class="pub-body">
    <p class="mb-2">{badges}</p>
    <h3 class="text-5 text-white mb-2">{title}</h3>
    <p class="text-white-50 mb-1">{format_authors(f["author"])}</p>{venue_html}
    <div class="pub-actions">{read}{code}{toggles}
    </div>
  </div>{panels}
</article>"""
    # indent everything except the <pre> contents, whose whitespace is significant
    out, in_pre = [], False
    for line in html.splitlines():
        in_pre = in_pre or line.startswith("<pre>")
        out.append(line if in_pre else INDENT + line)
        in_pre = in_pre and "</pre>" not in line
    return "\n".join(out)


def load() -> list[dict]:
    """Parse and validate publications.bib; raises BibError listing all problems."""
    entries = parse_bib(DATA.read_text(encoding="utf-8"))
    problems = []
    keys = [e["key"] for e in entries]
    problems += [f"duplicate key '{k}'" for k in sorted({k for k in keys if keys.count(k) > 1})]
    for e in entries:
        missing = [f for f in REQUIRED if not e["fields"].get(f)]
        if missing:
            problems.append(f"line {e['line']}, entry '{e['key']}' is missing: {', '.join(missing)}")
        elif not re.fullmatch(r"\d{4}", e["fields"]["year"]):
            problems.append(f"line {e['line']}, entry '{e['key']}': year must be 4 digits")
    if problems:
        raise BibError("\n  ".join(problems))
    return entries


def render(entries: list[dict]) -> str:
    cards = []
    for e in sorted(entries, key=lambda e: int(e["fields"]["year"])):
        thumb = None
        if e["fields"].get("pdf"):
            pdf = PAPERS / e["fields"]["pdf"]
            if pdf.exists():
                thumb = render_preview(pdf)
            elif (THUMBS / (pdf.stem + ".webp")).exists():
                thumb = THUMBS / (pdf.stem + ".webp")  # PDF not on this machine, keep existing preview
            else:
                print(f"  ! no preview for '{e['key']}': {pdf.relative_to(ROOT)} not found")
        cards.append(card(e, thumb))
    return "\n".join(cards)
