# Profile validation

The current front page is static. The name, role, introduction, expertise, and
links are native Markdown. Five groups of linked logo tiles close the page.
There is no hero image or animation in the README.

`python3 tools/validate_profile.py` checks:

- The personal website link and an identical `README-static.md` copy.
- A final tech stack section with every tool from `design/toolchain.json`.
- All 26 linked logo tiles, descriptive alt text, and light/dark sources.
- All 52 local PNG signatures and 240 × 198 pixel dimensions.
- Static artwork, no custom CSS or scripts, and no bundled font files.

The tiles display at 80 × 66 pixels. Inline rows can wrap on narrow screens.
Both theme variants have been visually inspected at their display size.

`python3 tools/make_preview.py` generates HTML directly from `README.md`,
including a self-contained preview. Its stylesheet approximates GitHub Markdown;
it is not a screenshot of the live profile.

The previous console artwork, v5 divider, and v6 animated header remain archived.
Only the v4 tool tiles appear in the current README.
