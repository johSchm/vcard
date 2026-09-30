<!--
  Settings for the CV (res/CV_Johann_Schmidt.pdf, the "Download CV" button).
  Build it with: python3 tools/cv_pdf.py

  The CV has no text of its own. It is put together from the other files:
    about.md    the profile (its `cv:` line) and the counters
    resume.md   Experience and Education (`cv:` lines, `cv_section:`)
    service.md  Leadership and Service (`cv:` lines)
    talks.md    Talks and Teaching (grouped by `type:`)
    coding.md   Skills (`cv:` lines)
    home.md     email and LinkedIn
    publications.bib   the publications
  A `cv:` line is the short version of a text for the CV. "cv: no" leaves an
  entry out. In a `cv:` line **text** is bold and *text* is italic.

  name:       shown at the top (required)
  headline:   the line under the name (required)
  photo:      path of your photo, shown as a circle at the top (optional)
  location:   where you live (optional)
  website:    your website (optional)
  github:     GitHub profile (optional)
  scholar:    Google Scholar profile (optional)
  languages:  spoken languages, shown as the last row under Skills (optional)
  papers:     the publications to list: keys from publications.bib (or PDF names),
              separated by commas. They are sorted by year, newest first. Leave the
              line out to list all publications.
  sections:   the sections and their order (optional). The default is
              profile, numbers, experience, education, publications, skills, service, talks
-->
name: Johann Schmidt
headline: Research Scientist in Deep Learning
photo: images/profile.jpg
location: Magdeburg, Germany
website: https://johann-schmidt.com
github: https://github.com/johSchm
scholar: https://scholar.google.com/citations?user=VmKtXYoAAAAJ
languages: German (native), English (daily working language)
papers: Schmidt2026b, Lindner2026, Schmidt2026a, Schmidt2025a, Schmidt2024b, Schmidt2024a, Lang2021
