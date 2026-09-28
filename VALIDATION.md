# Validation performed

- Both animated and still READMEs have only repository-local image dependencies.
- All 74 distinct image references resolve to included files.
- Light and dark modes were rendered in Chromium at viewport widths 1200, 850,
  390, and 320 pixels. Every rendered image loaded; no horizontal page overflow
  was observed in these tests.
- Header, section headings, and native project titles share the same left edge.
- Tool images have identical 84 × 76 CSS-pixel display boxes.
- Animated sources are 2280 × 1008 pixels, displayed at up to 720 pixels wide.
- The offline preview's light/dark controls were exercised.

These checks use local Chromium renderings of the actual README with
GitHub-like Markdown presentation. They are NOT tests against the user's live
GitHub repository or GitHub's complete production HTML sanitizer. GitHub may
apply different outer spacing. Font sizing of the native text follows GitHub.

Detailed numeric logs are in design/layout-checks.json and
design/animation-checks.json.
