# Checks performed on the restored console bundle

These are local checks, not verification on the live GitHub profile.

## Animation

- The loop is `whoami` → `cat research.txt` → `ls selected-work/` → repeat.
- Both theme GIFs are 936 × 750 pixels, with 58 encoded frames and a 16.97-second
  cycle. Each completed scene has a 3.2-second reading pause.
- Every one of the 61 semantic timeline states was sampled in the decoded GIF.
  Each matched its expected palette-quantized rendering exactly in both themes.
- Fixed chrome, identity text, and the footer were pixel-identical across all frames.
- A single shared palette per theme prevents palette changes between scenes.
- The static alternative remains the completed research summary, as before.

## Preservation

- README.md and README-static.md are byte-for-byte identical to the MATLAB-corrected
  base repository.
- Only two visual assets changed: console-light.gif and console-dark.gif.
- Research focus, navigation, metadata, toolchain graphics, and the corrected MATLAB
  marks are byte-for-byte unchanged. The Hierarchical models · MCMC subtitle remains.
- Animation dimensions and both 312 × 250-pixel header display footprints are unchanged.
- All 70 distinct image references in the animated/static READMEs resolve to local files.
- No font files are distributed.

## Local rendering

The included README was rendered in Chromium in light and dark themes at 390 and
1060-pixel viewport widths. All images loaded, both panels retained their 312 × 250
footprint, and no horizontal page overflow occurred. The screenshot previews freeze
only the console to its decoded first frame for consistent captures. HTML previews
and README.md use the complete animated GIFs. This stylesheet approximates GitHub;
it is not a live GitHub rendering.

Raw results: design/animation-checks.json, design/layout-checks.json,
design/asset-checksums.json, and design/validation.json.
