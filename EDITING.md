# Editing the profile

## Ordinary wording and links

Edit the root `README.md`. The biography, numbered research headings, descriptions,
project links, and toolchain section headings are ordinary Markdown/HTML text.
The project headings use the same native font and baseline for their numbers and titles.
There are no layout tables or image-based project titles.

## Artwork text

The animated console and research-focus panel are generated graphics. Change the relevant
strings in `design/profile.json`, then rebuild them. The required third subtitle is:

```
Hierarchical models · MCMC
```

A pre-rendered static alternative is included as `README-static.md`. Use that file as
`README.md` to disable the console animation.

## Optional rebuilding

No rebuilding is needed to publish. For later graphic changes, install the packages in
`tools/requirements.txt`. Fonts are read from your own computer; no font files are bundled.
The builder prefers Inter and DejaVu Sans Mono. A system Arial fallback is supported.
`PROFILE_FONT_DIR` can point to your local Inter/DejaVu font directory.

```
python3 -m pip install -r tools/requirements.txt
python3 tools/build_profile.py --assets-only
python3 tools/validate_profile.py
```

`--assets-only` preserves hand-edited README text. To regenerate the README from the
configuration as well, omit that flag; back up your text first.

Toolchain caption text and group membership are in `design/toolchain.json`.
The supplied tool marks retain the previous kit's artwork. See `ICON-SOURCES.md` for
reconstructed and representative marks; do not describe them all as official artwork.

## Layout

Each header panel has a 312 × 250 display footprint. Together they take approximately
629 pixels including ordinary inline spacing; they wrap to separate rows on narrow
screens. There are no mobile-specific image sources to accidentally stretch on desktop.
The animation is rendered at 936 × 750 pixels (3× its display size). The focus panel is
vector artwork. Navigation is 30 pixels high. Tool tiles have an 80 × 66 display footprint.

The README does not depend on the CSS or JavaScript in the browser preview. Preview files
are conveniences, not deployment requirements. After changing README wording, regenerate
the preview with `python3 tools/make_preview.py` (requires markdown-it-py).
