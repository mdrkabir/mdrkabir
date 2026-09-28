# Editing the GitHub profile

The published front page is the root `README.md`. It uses ordinary Markdown for the
name, introduction, publication list, links, and methods. Edit that file directly.
`README-static.md` is retained as a matching copy; after editing the front page, copy
`README.md` over it so the two do not drift.

The only display assets are the restrained divider in
`assets/profile-v5/research-thread-light.svg` and
`assets/profile-v5/research-thread-dark.svg`. Keep both variants in sync if changing
its colors or geometry. The profile needs no custom CSS, JavaScript, external image
service, or animation.

Publication titles, venues, authorship labels, summaries, and links should be checked
against the papers before changing them. The current publication sources are the
arXiv preprint, the AAAI proceedings page, and the Science Advances DOI linked in the
README.

## Check and preview

From the repository root:

```bash
python3 tools/validate_profile.py
python3 tools/make_preview.py
```

The preview generator accepts `markdown-it-py` or Pandoc. Open `PREVIEW-local.html`
for a local approximation of the GitHub page; `PREVIEW.html` embeds the divider and
can be shared as one file. GitHub's own rendering remains the final authority.

`tools/build_profile.py`, `design/profile.json`, and `assets/profile-v4/` belong to
the previous animated profile. The builder now preserves the current README even if
it is run. None of those archived assets are needed to display the front page.
