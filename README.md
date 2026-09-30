# johann-schmidt.com
This is the associated GitHub repo for the website.

## Editing the text

All text lives in [`content/`](content/) as Markdown, one file per section
(`home.md`, `about.md`, `resume.md`, `thesis.md`, `talks.md`, `coding.md`,
`legal.md`).
`index.html` only holds the layout. After editing, run

```sh
python3 tools/build.py
```

which writes the text (and the publications) into `index.html`. Don't edit
between `<!-- BUILD:... -->` markers in `index.html`; that part is generated.
The format is explained in [`content/README.md`](content/README.md).

## Updating the CV

The CV behind the "Download CV" button (`res/CV_Johann_Schmidt.pdf`) is
generated from the same content:

```sh
python3 tools/cv_pdf.py
```

Entries carry a `cv:` line with their short text for the CV. The settings
(header, which publications, order of the sections) are in
[`content/cv.md`](content/cv.md), which also lists what comes from where.
The script warns if the CV grows beyond two pages. Requires LaTeX with
`latexmk` (`brew install texlive`).

## Adding a publication

1. Paste the paper's BibTeX (e.g. from Google Scholar or DBLP) into
   [`publications.bib`](publications.bib) and add two optional fields:
   ```bibtex
   @inproceedings{schmidt2025example,
     title     = {Paper Title},
     author    = {Schmidt, Johann and Stober, Sebastian},
     booktitle = {International Conference on Machine Learning (ICML)},
     year      = {2025},
     url       = {https://arxiv.org/abs/...},
     abbr      = {ICML},             % short venue tag on the card
     pdf       = {any-file-name.pdf} % preview source in res/papers/
   }
   ```
   `abbr` and `pdf` are only used for the card and are left out of the
   BibTeX that visitors copy. Cards are sorted by year automatically.
2. Put the PDF into `res/papers/` (not committed, only its preview is).
3. Run `python3 tools/build.py` to update the cards and
   `python3 tools/publications_pdf.py` to update the PDF list behind the
   "Download as PDF" button (`res/Publications_Johann_Schmidt.pdf`) and
   `python3 tools/cv_pdf.py` to update the CV, then commit.

Requires `pdftoppm` and `magick` (`brew install poppler imagemagick`); the
PDF list additionally needs LaTeX with `latexmk` and `biber`
(`brew install texlive`).
