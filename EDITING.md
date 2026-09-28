# Editing this profile

## Ordinary wording and links

Edit `README.md` for the biography, project descriptions, paper/code links,
toolchain category headings, and the small names beneath logos.
The tool names are inside `<sub>...</sub>` tags. Leave the neighboring `<rt>`,
`<picture>` and image tags in place. Only the logo is linked, not its label.

Preserve the deliberately small image `width` attributes. In particular, keep the
header and project/section images at `width="720"`, and do not add fixed heights.
A SVG's `viewBox="0 0 1200 ..."` describes its internal drawing coordinates; it is
not a request to display the image at 1200 pixels wide.

`README-static.md` is an optional alternative. To publish it, copy its content
into `README.md`; edit that variant too when you want the two versions to match.

## Text within graphics

The visible name/affiliation in the console, the animated commands, and text inside
research-title SVGs are part of image files. Editing `alt`, `title`, or `aria-label`
does not change the visible lettering. Design metadata is retained in
`design-source/` for future rebuilding; changing JSON alone does not modify images.

- `console-scenes.json`: animated prompts and output lines.
- `content.json`: profile and project text used by earlier rendering steps.
- `console-background.svg` / `console-mobile-background.svg`: outlined console art.
- `toolchain.json`: grouped tool inventory and labels.
- `official-logo-sources.json`: original logo source information.

No font files are distributed. SVG letters in the supplied graphics are outlined.

## Logos

The source URLs used for the four corrected brands are in `tools/logo-sources.json`.
After the initial setup, the README references their local PNGs. Do not replace
them with earlier approximate JAX/NumPyro/MATLAB/vLLM symbols.

To intentionally fetch new copies of the source images:

```bash
python3 tools/fetch_official_logos.py --refresh
python3 tools/validate_profile.py --require-local
```

To check an ordinary edit without making any changes:

```bash
python3 tools/validate_profile.py --require-local
```

## Optional website and resume buttons

The supplied profile retains the latest three navigation links (Google Scholar,
LinkedIn, and Repositories). Website and resume button graphics are also included
as `assets/nav-website-*.svg` and `assets/nav-resume-*.svg`; add their links only
once the correct public URLs are known. No guessed URL or placeholder button is
published by default.
