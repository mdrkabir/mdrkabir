# Profile validation

The current front page is a text-first GitHub README with one small, theme-aware
SVG divider. The previous animated console and tool logo gallery are archived in
`assets/profile-v4/` and are not referenced by the README.

`python3 tools/validate_profile.py` checks the profile heading, three selected
publications and paper links, matching static copy, local light/dark artwork,
SVG structure, absence of CSS or script dependencies, and absence of bundled fonts.

`python3 tools/make_preview.py` generates both local HTML previews directly from
`README.md`. The preview stylesheet approximates GitHub's Markdown styles. Visual
checks should be made in a browser before publishing because local preview styling
can differ from GitHub's rendering.
