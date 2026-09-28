# Editing this version

## Ordinary writing changes

Edit `README.md` directly for the bio, project titles, descriptions, links,
keywords, section names, or their order. Project titles are native Markdown text.
There is no need to rebuild an image for a project-title change.

## Animation and logo-label changes

The exact artwork source and renderer are included:

- `design/profile.json`: name, affiliation, terminal lines, research-focus text,
  project metadata, and display width.
- `design/toolchain.json`: toolchain sections, names beneath the logos, and URLs.
- `design/legacy-logos/`: individual logo/symbol artwork used by the renderer.
- `tools/build_profile.py`: creates high-resolution animation, small metadata
  graphics, and evenly sized transparent logo/caption images.

Install the optional Python dependencies from `tools/requirements.txt` to
regenerate. The renderer uses locally installed Inter/DejaVu fonts where
available, with a system Arial fallback. No font files are distributed here.
Set `PROFILE_FONT_DIR` to a directory containing your own installed Inter and
DejaVuSansMono fonts when needed. Different fallback fonts can change the artwork.

```
python3 -m pip install -r tools/requirements.txt
python3 tools/build_profile.py --assets-only
python3 tools/validate_profile.py
```

`--assets-only` preserves your manually edited README. A full run without it
recreates both READMEs from the configuration and can overwrite manual wording
changes; save a copy before doing a full rebuild.

To change only the toolchain or project graphics without rebuilding the GIF:

```
python3 tools/build_profile.py --assets-only --skip-animation
```

The artwork uses actual 3x pixel dimensions; DPI metadata is not the mechanism.
The README's explicit display width keeps the high-resolution GIF compact.
The captions are drawn into individual transparent images (not a screenshot of
the whole page), keeping them centered without underlines, tables, or ruby markup.

The decorative project motifs are illustrations, not experiment-result plots.
See ICON-SOURCES.md for the provenance and limitations of individual marks.
