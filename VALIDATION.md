# Checks performed on this bundle

This is a local check, not verification on the owner's live GitHub profile.

- The README's native headings and actual local artwork were rendered in Chromium.
  The preview uses a GitHub-style Markdown stylesheet without hiding table borders or
  applying profile-specific layout classes. The README itself contains no custom CSS.
- Tested light and dark color schemes at 320, 390, 760, and 1060-pixel viewport widths.
- Both header panels have identical 312 × 250 display footprints. At desktop widths
  they share the same top edge; on mobile they wrap to the same left edge.
- Research heading prefixes (01, 02, 03) have matching measured left positions and widths.
- No horizontal page overflow or missing images occurred in these eight local cases.
- All 70 distinct image dependencies across the animated and static READMEs are local.
- Both console GIFs contain 22 frames, rendered at 936 × 750 pixels. Each cycle lasts
  8.58 seconds and begins with 5.5 seconds of fully readable completed text.
- The focus panel is a separate vector image. Both theme variants contain the exact
  subtitle `Hierarchical models · MCMC`.
- Light/dark preview buttons were toggled repeatedly and loaded all images successfully.
- Five toolchain categories remain. FSDP and LaTeX are excluded.
- No font files are distributed.

Raw results: `design/validation.json`, `design/layout-checks.json`, and
`design/animation-checks.json`. Existing reconstructed-tool-logo caveats remain in
`ICON-SOURCES.md`.

The screenshot previews freeze the console on its completed first frame. The included
`PREVIEW.html` and README use the actual animated file. GitHub's current exact typography
and spacing may differ from the locally approximated stylesheet.
