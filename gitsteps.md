# Git / GitHub Pages steps — Writer's Thesaurus

Repo folder on your Mac: `.../GitStuff/Thesaurus/0One Notebooks/writers-thesaurus-repo`
GitHub repo: `https://github.com/amelabrs/writers-thesaurus`
Live site: **https://amelabrs.github.io/writers-thesaurus/**

## One-time setup (already done)

1. `git init`, `git add -A`, `git commit` inside `writers-thesaurus-repo/`.
2. `gh repo create writers-thesaurus --public --source=. --remote=origin --push`
   (or created on github.com, then `git remote add origin ...` + `git push -u origin main`).
3. On github.com: repo → **Settings** → **Pages** (left sidebar, under "Code and
   automation") → **Source**: "Deploy from a branch" → **Branch**: `main` / `(root)`
   → **Save**.

That's done and confirmed working — no need to repeat it.

## Updating the live site (every time there's new material)

1. Paste new material to Claude as usual (character notes, beats, exported "my
   additions" JSON, etc.). Claude merges it into
   `_thesaurus_build/data.json` and regenerates `index.html` **inside this repo
   folder**, `writers-thesaurus-repo/`.
2. In Terminal:
   ```bash
   cd "/Users/amel/Documents/Documents Amel/GitStuff/Thesaurus/0One Notebooks/writers-thesaurus-repo"
   git add -A
   git commit -m "Update thesaurus"
   git push
   ```
3. GitHub Pages redeploys automatically on push — usually live within a minute or two.

## Checking it worked

- Visit **https://amelabrs.github.io/writers-thesaurus/** directly and hard-refresh
  (Cmd+Shift+R) if it looks stale.
- Or check the **Actions** tab on the repo for a "pages build and deployment" run —
  green check = live, yellow = still building, red = failed (click in to see why).

## Notes

- `index.html` is the actual site file GitHub Pages serves — it must stay at the
  repo root.
- `_thesaurus_build/` (data.json, generate.py, IMPLEMENTATION.md, summary.md) is
  the source of truth and reference docs — versioned here too, but not itself
  served as a page.
- The repo is **public** (GitHub Pages requires this on the free plan) — data.json
  includes some verbatim quoted passages from published novels used as personal
  craft reference, kept in mind as a deliberate choice, not an oversight.
