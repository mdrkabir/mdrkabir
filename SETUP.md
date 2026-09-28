# Publish this complete profile

The bundle is self-contained. All display images are already generated and stored locally.
No account connection, logo downloader, network fetch, or build step is required.

1. Save a backup of any customized wording in your current README.
2. Copy the **contents** of this `mdrkabir` folder into your existing local profile repository.
   Keep your repository's `.git` folder and unrelated files.
3. At minimum, update the root `README.md` and add **all** of `assets/profile-v4/`.
4. Commit the files and push to your repository's default branch.

Do not put the contents inside an additional `mdrkabir` directory. The structure must be:

```
README.md
assets/
  profile-v4/
    console-light.gif
    console-dark.gif
    focus-light.svg
    focus-dark.svg
    ...
```

Old profile-v2 assets may remain; the new README does not refer to them. You do not need
any earlier ZIP. This folder deliberately uses a new asset path to avoid mixing generations.

## Existing automatic workflow

If a previous kit installed `.github/workflows/profile-assets.yml`, replace it with the
file included here. It validates the files and cannot modify or regenerate your README.
The read-only workflow is optional; the profile displays without GitHub Actions.

## Optional offline validation

Run from the repository root:

```
python3 tools/validate_profile.py
```

## View before publishing

Open `PREVIEW.html` in a browser. It embeds the supplied images and includes light/dark
controls. It is a local approximation of GitHub's README styling, not a live GitHub page.
The animation has a long readable pause before each typing cycle.
