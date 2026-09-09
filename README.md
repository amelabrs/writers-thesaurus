# Writer's Thesaurus

A personal, self-contained thesaurus of writing-craft material — physical beats,
character sketches, sensory notes, dialogue tags, and more — organized by notebook
and headword, with full-text search across everything.

**Live site:** https://amelabrs.github.io/writers-thesaurus/

## What's in this repo

- `index.html` — the shipped, self-contained page (no build step, works offline).
  All content is embedded inline; there are no external requests.
- `_thesaurus_build/data.json` — the source of truth. Every notebook → headword →
  entry, as structured data.
- `_thesaurus_build/generate.py` — the renderer. `python3 generate.py data.json out.html`
  regenerates `index.html` deterministically from `data.json`.
- `_thesaurus_build/IMPLEMENTATION.md` — architecture notes: file map, data schema,
  page behavior, and the reasoning behind various design decisions.
- `_thesaurus_build/summary.md` — a standalone project summary.

## Updating the site

1. Edit `_thesaurus_build/data.json` (add/remove/merge notebooks, headwords, entries).
2. Regenerate: `python3 _thesaurus_build/generate.py _thesaurus_build/data.json index.html`
3. Commit and push both `index.html` and `data.json`. GitHub Pages redeploys
   automatically from the default branch.

## Page features

- Notebook switcher, filterable headword sidebar, and global search (with clickable
  result crumbs that jump straight to a headword).
- Add your own entries (optionally with an attached image) — stored in your
  browser's local storage, exportable as JSON to fold back into `data.json`.
- Delete any entry, built-in or your own; create new headwords/sections from the page.

This is a personal creative-writing reference tool. `data.json` includes short
quoted passages from published novels used as craft reference — kept here for
personal study alongside the site's own original material.
