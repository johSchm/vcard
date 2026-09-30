# Website text

Each file here fills one section of the page. After editing, run

```sh
python3 tools/build.py
```

and reload `index.html`. If something is missing or malformed, the script says
which file and line, and leaves the page unchanged.

| File        | Section                                          |
|-------------|--------------------------------------------------|
| `home.md`   | hero screen (greeting, typing phrases, button)   |
| `about.md`  | About Me text and the counters                   |
| `resume.md` | Resume cards                                     |
| `thesis.md` | PhD Thesis (summary and contribution cards)      |
| `talks.md`  | Talks introduction and cards                     |
| `service.md`| Service introduction and cards (reviewing, supervision) |
| `coding.md` | Coding introduction and cards (stack, tools, languages) |
| `legal.md`  | Terms & Policy / Disclaimer pop-ups in the footer |
| `cv.md`     | settings for the CV (header, publications to list, section order) |

Publications are not here; they come from [`../publications.bib`](../publications.bib).

The CV (`res/CV_Johann_Schmidt.pdf`) is generated from these files with
`python3 tools/cv_pdf.py`. A `cv: ...` line under a title is the short text
for the CV and is not shown on the website; `cv: no` leaves the entry out of
the CV. See the comment at the top of `cv.md`.

## Format

```markdown
<!-- comments like this are ignored -->
key: value              ← settings for the section (top of the file)

Normal paragraphs, separated by a blank line.

## Card title           ← starts a card / entry
when: 2020 - today      ← settings for this card, directly under the title
type: Experience

The card's text.

### Extra part          ← a sub-part inside the card (e.g. a thesis in resume.md)
where: Some Institute

Its text.
```

Inside text:

| Write                  | Get                                   |
|------------------------|---------------------------------------|
| `*highlight*`          | text in the green accent color        |
| `**bold**`             | **bold**                              |
| `[label](https://…)`   | a link (external links open in a new tab) |
| `[label](#thesis)`     | a link that scrolls to another section of the page |
| `[label](paper:ITS)`   | a link that jumps to a publication (BibTeX key or PDF name) |
| `- item` / `1. item`   | bullet / numbered list                |
| `one \\ two`, `one \n two`, `one <br> two` | a line break (any of the three) |
| `#### Heading`         | small heading (used in `legal.md`)    |

Which settings each file needs is noted in a comment at the top of that file.
