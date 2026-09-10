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
4. Claude authenticated to GitHub as you (via device login flow, in the sandboxed
   shell Claude uses on your Mac) so it can commit and push directly from here on —
   no more manual git commands needed for routine updates.

That's all done and confirmed working — no need to repeat it.

## Updating the live site (every time there's new material)

Just paste new material to Claude as usual (character notes, beats, exported "my
additions" JSON, etc.), or ask it to make a structural change. Claude merges it
into `_thesaurus_build/data.json`, regenerates `index.html` inside
`writers-thesaurus-repo/`, and now commits + pushes it too. GitHub Pages redeploys
automatically on push — usually live within a minute or two.

If you ever want to push manually yourself instead (e.g. Claude isn't available),
the commands are:
```bash
cd "/Users/amel/Documents/Documents Amel/GitStuff/Thesaurus/0One Notebooks/writers-thesaurus-repo"
git add -A
git commit -m "Update thesaurus"
git push
```

## Checking it worked

- Visit **https://amelabrs.github.io/writers-thesaurus/** directly and hard-refresh
  (Cmd+Shift+R) if it looks stale.
- Or check the **Actions** tab on the repo for a "pages build and deployment" run —
  green check = live, yellow = still building, red = failed (click in to see why).

## Comments & suggestions (giscus)

The live page has a comment box at the bottom ("Comments & suggestions"), backed by
GitHub Discussions via a free widget called **giscus** — visitors sign in with their
own GitHub account to comment; nothing they do changes the thesaurus itself.
Comments land as posts in the repo's **Discussions** tab
(`https://github.com/amelabrs/writers-thesaurus/discussions`), under the
**Announcements** category. You review them there, and when you like a suggestion,
tell Claude (or add it yourself) and it becomes a real entry + commit — same
routing rules as anything else pasted in.

**One manual step required** (GitHub App installs need a human click, can't be
scripted): install the giscus app on this specific repo at
**https://github.com/apps/giscus/installations/new** → choose "Only select
repositories" → pick `writers-thesaurus` → Install. Until this is done, the comment
box will show a "giscus is not installed" message instead of working.

## Notes

- `index.html` is the actual site file GitHub Pages serves — it must stay at the
  repo root.
- `_thesaurus_build/` (data.json, generate.py, IMPLEMENTATION.md, summary.md) is
  the source of truth and reference docs — versioned here too, but not itself
  served as a page.
- The repo is **public** (GitHub Pages requires this on the free plan) — data.json
  includes some verbatim quoted passages from published novels used as personal
  craft reference, kept in mind as a deliberate choice, not an oversight.
