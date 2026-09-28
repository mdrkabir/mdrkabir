# Publish the profile

This is a complete, self-contained repository—not a patch. No image downloads,
browser repair pages, Python runs, or GitHub Actions are required to display it.

1. Save a copy of your current README if you have edited its wording.
2. Open your existing `mdrkabir/mdrkabir` local repository. Keep its `.git` directory.
3. Copy the contents of this ZIP's `mdrkabir` directory into that repository.
   `README.md` must be at the top level, with `assets/` beside it.
4. Commit the files to the default branch and push.

Required for display:

```
README.md
assets/profile-v2/   (the entire supplied directory)
```

Do not upload the outer ZIP or nest another `mdrkabir/` directory inside your repo.
The `profile-v2` folder isolates these assets from earlier versions, so you do not
need to delete your older logo files. There are no remote image dependencies.

## Important for installations using an earlier supplied workflow

Copy the included `.github/workflows/profile-assets.yml` as well. It REPLACES the
old download-and-rewrite workflow with a read-only validator. The new workflow
never downloads logos, edits the README, or commits changes. Also copy `tools/`
when using it. Alternatively, disable/remove that specific old workflow yourself.
Do not remove unrelated workflows.

The remaining files are optional source/documentation. `README-static.md` gives
the same layout with a still header: copy its contents to `README.md` to use it.

GitHub documentation:
https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github
