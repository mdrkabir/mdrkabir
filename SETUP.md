# Option C — complete profile repository

This folder consolidates the final size-corrected README, all retained navigation
and tool graphics, research-title fixes, light/dark animated headers, and source
metadata. It is **not** a patch to combine with an older ZIP.

## An important packaging limitation

The original PNG files for **JAX, NumPyro, MATLAB, and vLLM** could be viewed through
the research browser but could not be downloaded into the assistant's working
container. Consequently the archive includes **82 local graphics** and references
these four brands using **five genuine upstream PNG URLs** initially (vLLM has two
theme variants). No wrong or placeholder replacement logos are included.

The included setup downloads the five original PNGs, validates their structure and
checksums, records SHA-256 hashes, and changes the two READMEs to use local files.
It is a one-time step, not an ongoing badge service. After setup, every displayed
image is stored in your own repository. You do not need the earlier HTML repair
page or any earlier ZIP.

## Recommended: finish the logo setup locally, then push

Copy **the contents** of this `mdrkabir` folder into the root of your existing local
clone of `mdrkabir/mdrkabir`. Merge/replace matching supplied files. Do not delete
`.git`, unrelated files, or your repository history. Save a copy of your customized
README before replacing it; this version contains the last writing supplied in
this chat, not later changes made only on GitHub.

From inside that existing clone, run:

```bash
python3 tools/fetch_official_logos.py
python3 tools/validate_profile.py --require-local
```

Stop and resolve any error before pushing. These commands need Python 3.9+ and an
internet connection, but no additional Python packages and no API key.

Review and push only the supplied paths:

```bash
git status --short
git diff -- README.md

git add README.md README-static.md assets tools .github design-source \
  SETUP.md EDITING.md ICON-SOURCES.md LICENSE-LOBE-ICONS.txt .gitignore

git commit -m "Consolidate Option C profile and fix image sizing"
git push
```

Do not use `git push --force`. Use your existing clone so the normal remote,
branch, and commit history remain intact. This ZIP deliberately has no `.git`.

## Alternative: let GitHub download the originals after your first push

Push the whole supplied folder, including the hidden `.github` directory and the
`tools` directory. The workflow named **Prepare profile logos** runs on the default
branch, downloads the originals, validates the profile, and commits only the five
PNG files, their manifest, and localized README paths. Existing wording is preserved.
The initial README uses genuine upstream URLs until the workflow succeeds.

This requires GitHub Actions to be enabled and the workflow to have permission to
commit to the default branch. The workflow declares `contents: write` and uses the
repository's automatic `GITHUB_TOKEN`; no personal token needs to be added. Branch
protection or organization policy can still block its commit. In that case, use
the local commands above or commit through your normal pull-request process.

After the workflow makes its commit, run `git pull --ff-only` in your local clone
before editing again. The workflow is idempotent: existing valid local originals
are reused and no new commit is made when there is nothing to change.

If using GitHub's web upload, open this extracted folder and upload its contents,
not the ZIP or another enclosing folder. Dotfolders may be hidden in your file
manager. On macOS, Command+Shift+Period reveals `.github` and `.gitignore`.
For a large upload, Git from your existing clone is the simpler route.

## Expected layout

```text
mdrkabir/mdrkabir
├── README.md
├── README-static.md
├── assets/
├── .github/workflows/profile-assets.yml
├── tools/
├── design-source/
├── SETUP.md
├── EDITING.md
├── ICON-SOURCES.md
├── LICENSE-LOBE-ICONS.txt
└── .gitignore
```

Once the logo setup succeeds, the profile only needs `README.md` and `assets/` to
render. The other files document, validate, or reproduce it. They are included to
make this a complete source repository, rather than another isolated README patch.

## Preserved choices and fixes

- Option C console styling, with animated light/dark and mobile variants.
- Main console, section graphics, and research cards displayed at 720 px maximum.
- Uniform project-title sizes with separate mobile layouts.
- Five toolchain categories and 26 tools, with small names below their logos.
- Labels are not links; only the logos are linked, avoiding underline artifacts.
- FSDP and LaTeX are excluded from the toolchain.
- Smaller navigation buttons and individually proportioned wordmarks.
- Reduced-motion stills and an optional fully static `README-static.md`.

No GitHub Pages configuration, web server, npm installation, or custom stylesheet
is required. HTML previews from older packages are not part of this repository.

## Verification boundaries

The local files, paths, dimensions, theme assets, and setup logic were tested in
the assistant's container. The download/atomic-update logic was tested with local
fixtures; live downloading and a GitHub workflow run could not be tested there.
This is not a live inspection or backup of your currently published repository.

Official GitHub references:
- https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
- https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
- https://docs.github.com/en/actions/tutorials/authenticate-with-github_token
- https://github.com/actions/checkout
