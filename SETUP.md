# Publish the GitHub profile

The front page is `README.md` in the root of the `mdrkabir/mdrkabir` profile
repository. Commit it with the light and dark stack logo tiles:

```
README.md
assets/profile-v4/tool-*-light.png
assets/profile-v4/tool-*-dark.png
```

`README-static.md` is an identical copy of the current static profile. The
52 PNG tiles cover 26 tools across five groups. Retain `ICON-SOURCES.md` and
the included license notices with the repository. All artwork is local; no
external image host, GitHub Action, or build step is needed to display it.

To check and preview locally:

```bash
python3 tools/validate_profile.py
python3 tools/make_preview.py
```

Open `PREVIEW-local.html` or the self-contained `PREVIEW.html` to inspect both
themes. These previews approximate GitHub's styling; they are not screenshots
of the live GitHub page.
