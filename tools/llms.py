"""Machine-readable versions of the website, written by build.py.

    llms.txt          the whole profile as plain Markdown (https://llmstxt.org), for
                      language models and other programs that read the site
    JSON-LD           a schema.org Person in the <head> of index.html, for search engines

Both are put together from the same content/*.md and publications.bib as the
page, so they never say more or less than the page does. They contain facts
only, no text addressed to whoever reads them.
"""
import json
import re
from datetime import date

import build
import publications
from build import Node, list_items

URL = "https://johann-schmidt.com"


def plain(text: str) -> str:
    """The Markdown-like inline syntax of content/*.md as plain Markdown."""
    s = re.sub(r"\s*(?:\\\\|\\n|<br\s*/?>)\s*", " ", text, flags=re.I)
    s = re.sub(r"\[([^\]]+)\]\((?:paper:|project:|thesis:|#)[^)]*\)", r"\1", s)  # links inside the page
    s = re.sub(r"(?<![\w*])\*(?!\*)(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s)  # *highlight*
    return s.strip()


def paragraphs(lines: list[str]) -> list[str]:
    """Body text as Markdown paragraphs and lists, without the `- item` rows of cards."""
    out, para = [], []
    for line in lines + [""]:
        s = line.strip()
        if s and not re.match(r"^(-|\d+\.)\s", s):
            para.append(s)
        elif para:
            out.append(plain(" ".join(para)))
            para = []
    return out


def fill(text: str, counts: dict[str, int]) -> str:
    for name, value in counts.items():
        text = text.replace("{" + name + "}", str(value))
    if y := re.search(r"\{years since (\d{4})\}", text):
        text = text.replace(y.group(0), str(max(date.today().year - int(y.group(1)), 0)))
    return text


def kind_of(entry: dict) -> str:
    """'journal', 'conference', 'workshop' (abbr like "AAAI: MALTA") or 'preprint', so a
    reader can tell them apart instead of counting every paper the same."""
    f = entry["fields"]
    if entry["type"] == "article":
        return "journal"
    if ":" in f.get("abbr", ""):
        return "workshop"
    if "arxiv" in (f.get("abbr", "") + publications.venue_of(f)).lower():
        return "preprint"
    return "conference"


def authors(field: str) -> str:
    names = [publications.format_author(n) for n in publications.split_top_level(field, r"\s+and\s+")]
    return ", ".join(names)


# --- llms.txt -------------------------------------------------------------------

def profile_markdown(docs: dict[str, Node], entries: list[dict], counts: dict[str, int]) -> str:
    home, about, cv = docs["home"], docs["about"], docs["cv"]
    md = [f"# {cv.need('name', 'cv.md')}", ""]
    if about.props.get("cv"):
        md += [f"> {plain(fill(about.props['cv'], counts)).replace('**', '')}", ""]

    md += [f"- Role: {cv.props.get('headline', '')}",
           f"- Location: {cv.props.get('location', '')}",
           f"- Status: {plain(home.props.get('tagline', ''))}"]
    if cv.props.get("languages"):
        md.append(f"- Languages: {cv.props['languages']}")
    md.append(f"- Email: {home.props['email']}" if home.props.get("email") else "")
    for key, label in (("linkedin", "LinkedIn"), ("github", "GitHub"), ("scholar", "Google Scholar"),
                       ("researchgate", "ResearchGate")):
        url = cv.props.get(key) or home.props.get(key)
        if url:
            md.append(f"- {label}: {url}")
    md += [f"- Website: {URL}", f"- CV (PDF): {URL}/res/CV_Johann_Schmidt.pdf", ""]

    md += ["## About", ""]
    for p in paragraphs(about.body):
        md += [p, ""]
    stats = next((c for c in about.children if c.title.lower() == "numbers"), None)
    if stats:
        md += [f"- {fill(item, counts)}" for item in list_items(stats.body)] + [""]

    md += ["## Experience and education", ""]
    for card in docs["resume"].children:
        md += [f"### {plain(card.title)} ({card.props.get('when', '')})",
               f"{plain(card.props.get('where', ''))}", ""]
        md += [p + "\n" for p in paragraphs(card.body)]
        for part in card.children:
            when = f" ({part.props['when']})" if part.props.get("when") else ""
            where = f", {plain(part.props['where'])}" if part.props.get("where") else ""
            md += [f"#### {plain(part.title)}{when}{where}", ""]
            md += [p + "\n" for p in paragraphs(part.body)]

    thesis = docs["thesis"]
    md += ["## PhD thesis", "", f"**{thesis.need('title', 'thesis.md')}**", ""]
    if thesis.props.get("where"):
        md += [plain(thesis.props["where"]), ""]
    md += [p + "\n" for p in paragraphs(thesis.body)]
    for e in thesis.children:
        papers = [publications.find(entries, n.strip()) for n in e.props.get("papers", "").split(",") if n.strip()]
        tags = [f"{p['fields'].get('abbr', '')} {p['fields']['year']}".strip() for p in papers if p]
        if e.props.get("status"):
            tags.append(e.props["status"])
        md += [f"### {plain(e.title)}" + (f" ({'; '.join(tags)})" if tags else ""), ""]
        md += [p + "\n" for p in paragraphs(e.body)]

    md += ["## Publications", ""]
    kinds = {}
    for e in entries:
        kinds[kind_of(e)] = kinds.get(kind_of(e), 0) + 1
    md += [f"{len(entries)} papers: " + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())), ""]
    for e in sorted(reversed(entries), key=lambda e: -int(e["fields"]["year"])):
        f = e["fields"]
        title = publications.latex_to_text(f["title"])
        link = publications.link_of(f)
        venue, abbr = publications.venue_of(f), publications.latex_to_text(f.get("abbr", ""))
        if abbr and abbr not in venue:
            venue = f"{venue} ({abbr})" if venue else abbr
        md.append(f"- {f['year']}, {kind_of(e)}: {f'[{title}]({link})' if link else title}. "
                  f"{authors(f['author'])}. {venue}.")
    md.append("")

    md += ["## Skills", ""]
    for p in paragraphs(docs["coding"].body):
        md += [p, ""]
    for card in docs["coding"].children:
        md += [f"### {plain(card.title)} ({card.props.get('when', '')})", ""]
        md += [p + "\n" for p in paragraphs(card.body)]
        md += [f"- {plain(i)}" for i in list_items(card.body)] + [""]

    ai = docs["ai"]
    md += ["## AI at work", "", plain(ai.need("lead", "ai.md")), ""]
    md += [p + "\n" for p in paragraphs(ai.body)]
    for card in ai.children:
        md += [f"### {plain(card.title)}", ""]
        md += [p + "\n" for p in paragraphs(card.body)]
        md += [f"- {plain(i)}" for i in list_items(card.body)] + [""]

    md += ["## Talks and teaching", ""]
    for t in build.newest_first(docs["talks"].children, "talks.md"):
        md.append(f"- {t.props['when']}, {t.props.get('type', '')}: {plain(t.title)}. {plain(t.props.get('where', ''))}.")
    md.append("")

    md += ["## Service and supervision", ""]
    for card in docs["service"].children:
        when = f" ({card.props['when']})" if card.props.get("when") else ""
        md += [f"### {plain(card.title)}{when}", ""]
        md += [p + "\n" for p in paragraphs(card.body)]
        md += [f"- {plain(i)}" for i in list_items(card.body)]
        for t in build.newest_first(card.children, "service.md"):  # titles only, the abstracts are the students'
            partner = f", with {t.props['with']}" if t.props.get("with") else ""
            md.append(f"- {t.props.get('type', '')} thesis, {t.props['when']}{partner}: {plain(t.title)}")
        md.append("")

    text = "\n".join(md)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


# --- JSON-LD --------------------------------------------------------------------

def person_jsonld(docs: dict[str, Node], entries: list[dict]) -> str:
    home, cv = docs["home"], docs["cv"]
    city, _, country = cv.props.get("location", "").partition(",")
    current = next((c for c in docs["resume"].children if "today" in c.props.get("when", "").lower()), None)
    schools = []
    for card in docs["resume"].children:
        if card.props.get("cv_section", "").lower() == "education" and "where" in card.props:
            name = plain(card.props["where"]).rsplit(",", 1)[0]
            if name not in schools:
                schools.append(name)
    same_as = [cv.props.get(k) or home.props.get(k) for k in ("linkedin", "github", "scholar", "researchgate")]
    person = {
        "@type": "Person",
        "name": cv.need("name", "cv.md"),
        "jobTitle": cv.props.get("headline"),
        "url": URL,
        "image": f"{URL}/{cv.props['photo']}" if cv.props.get("photo") else None,
        "email": f"mailto:{home.props['email']}" if home.props.get("email") else None,
        "address": {"@type": "PostalAddress", "addressLocality": city.strip(),
                    "addressCountry": country.strip()} if city else None,
        "worksFor": {"@type": "Organization", "name": plain(current.props["where"])} if current else None,
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": s} for s in schools] or None,
        "knowsAbout": [t.strip() for t in cv.props.get("topics", "").split(",") if t.strip()] or None,
        "knowsLanguage": [re.sub(r"\s*\(.*?\)", "", l).strip()
                          for l in cv.props.get("languages", "").split(",") if l.strip()] or None,
        "sameAs": [u for u in same_as if u] or None,
    }
    page = {"@context": "https://schema.org", "@type": "ProfilePage", "url": URL,
            "dateModified": date.today().isoformat(),
            "mainEntity": {k: v for k, v in person.items() if v}}
    body = json.dumps(page, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{body}\n</script>'
