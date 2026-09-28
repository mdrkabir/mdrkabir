# Editing the GitHub profile

The published front page is `README.md`. It uses ordinary Markdown for the
name, role, introduction, expertise, and links. The tech stack at the bottom
uses local PNG logo tiles with separate light and dark versions.

## Wording and links

Edit `README.md` directly. Keep `README-static.md` identical; the profile is
now entirely static.

The personal website holds the full research record. Keep the GitHub README
focused on expertise and tools, and update its website URL if it changes.

## Stack logos

`design/toolchain.json` records the five groups, 26 tools, labels, and links.
The README uses the corresponding `assets/profile-v4/tool-*-light.png` and
`tool-*-dark.png` files. Each 240 × 198 tile displays at 80 × 66 pixels and
includes a logo and caption. Keep both theme sources and descriptive alt text
when adding or replacing a tile. Update the inventory and both READMEs together.

See `ICON-SOURCES.md` for attribution and the distinction between source-derived
logos, reconstructed marks, and representative symbols.

## Rebuild and preview

Run from the repository root:

```bash
python3 tools/validate_profile.py
python3 tools/make_preview.py
```

The preview generator accepts `markdown-it-py` or Pandoc. `PREVIEW-local.html`
uses local images; `PREVIEW.html` embeds the artwork as a single-file preview.
These approximate GitHub's Markdown styling. The profile needs no build step
on GitHub.

The v4 tool tiles are reused from the earlier layout. Other v4 artwork, the v5
divider, and the v6 animated header are archived and unused by the front page.
`tools/build_profile.py` and `tools/build_hero.py` rebuild earlier artwork; they
are not needed to edit or publish the current profile.
