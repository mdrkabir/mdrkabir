# Publish the GitHub profile

The front page is `README.md` in the root of the `mdrkabir/mdrkabir` profile
repository. It needs only two local assets:

```
README.md
assets/profile-v5/research-thread-light.svg
assets/profile-v5/research-thread-dark.svg
```

Commit those files and push them to the repository's default branch to publish.
No build step, account connection, external image host, or GitHub Action is required.
`README-static.md` is a matching local copy, not a separate published page.

To check the local bundle before publishing:

```bash
python3 tools/validate_profile.py
python3 tools/make_preview.py
```

Open `PREVIEW-local.html` or the self-contained `PREVIEW.html` to review light and
dark appearances. The preview approximates GitHub Markdown styling; it is not a
screenshot of the live GitHub page.
