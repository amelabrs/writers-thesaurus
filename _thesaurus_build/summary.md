# Writer's Thesaurus — Project Summary (for resuming in a new conversation)

If you're starting a fresh conversation, paste this file in (or just say "continue
the Writer's Thesaurus project" and point Claude at `_thesaurus_build/` in the
"0One Notebooks" folder) — everything needed to pick up where this left off is on
disk already, nothing lives only in this chat.

## What this is

A personal, self-contained HTML thesaurus of writing-craft material (physical
beats, character sketches, sensory notes, etc.), built from your "0One Notebooks"
folder on your Mac. You open `Writer's Thesaurus.html` directly in a browser — no
server, no build step, works offline.

## Where everything lives (inside "0One Notebooks" on your Mac)

| Path | What it is |
|---|---|
| `Writer's Thesaurus.html` | The shipped file you open. Always overwritten in place — never a new/dated copy. |
| `_thesaurus_build/data.json` | **Source of truth.** Every notebook → headword → entries. Edit this, never the HTML directly. |
| `_thesaurus_build/generate.py` | Pure renderer: `python3 generate.py data.json out.html`. Deterministic — reads only data.json. |
| `_thesaurus_build/IMPLEMENTATION.md` | Full architecture reference — file map, data schema, page behavior, past decisions. Read this for any detail not covered here. |

## Data shape

```json
{
  "Notebook Name": {
    "Headword": [
      { "text": "...", "source": "optional citation" },
      { "text": "...", "image": "data:image/jpeg;base64,..." }
    ]
  }
}
```

24 notebooks as of the last build (~291 headwords, ~1738 entries): Beats, Body, Body
Language Reference, Personality, Joe Beats, Bus Observation, My Own Observation,
Clothes, From Books, Smells, Rural Setting, Metaphors, Food, Animals, Sounds,
Colors, Taste & Texture, Nature & Trees, Automobile, Locations, Words, Time,
Painting, Loose Notes.

## The recurring workflow (also saved as the `thesaurus-notebook-intake` skill)

You paste raw character-note material, or export your in-page additions, and it
gets routed and merged in:

1. **Trait/summary prose** → **Personality** notebook (paragraph-length, not
   chopped into beats).
2. **Character-specific action/dialogue beats** → the relevant **`<Book> Beats`**
   notebook (e.g. "Joe Beats"), citation attached as `source`.
3. **Generic cross-filing** → where a beat clearly maps onto an existing generic
   **Beats** headword *by meaning* (e.g. "gave a sheepish grin" → Smile), a
   generalized copy is filed there too, so plain-word search catches synonyms.
   Deliberately light-touch — only obvious matches, never forced (per your explicit
   "we don't need to go overboard, you have a very good search feature").

For an **exported "my additions" JSON** (from the page's export button): each entry
merges into its notebook/headword; any `__deleted` tombstones get actually removed
from data.json (see below).

After any data.json change: regenerate with `generate.py`, overwrite `Writer's
Thesaurus.html` in place, smoke-test with Playwright for non-trivial changes.

## Page features (as of the last ship)

- Notebook switcher + headword sidebar (with filter) + global search across every
  notebook (result crumbs like "Notebook → Headword" are clickable to jump there).
- **Add a beat** — per headword, with optional image attach (client-side resized).
  Written to `localStorage` only, invisible to Claude until exported.
- **Delete (×)** on *any* entry, built-in or your own. Deleting a built-in entry
  can't touch data.json from the browser, so it's recorded as a `__deleted`
  tombstone in localStorage instead, filtered out at render time — permanent until
  you export and it gets folded into data.json for real.
- **"+ Add section"** at the bottom of the sidebar — create a brand-new headword
  (e.g. a new character) directly from the page, same as how "Glokta" exists.
  Case-insensitive duplicate names are rejected inline.
- **Export my additions (.json)** in the footer — downloads everything you've added
  or deleted from the page, ready to send back for permanent merging.

## Key decisions (so they don't get re-litigated)

- Beats and Body stay separate notebooks despite overlapping headwords (chin, hand,
  elbow, etc.) — your explicit call.
- Eyes reference photos are embedded as base64, not linked externally (most of the
  file's ~3.7MB size).
- Personality entries stay as full paragraph sketches, not micro-beats.
- Original source typos/rough fragments are preserved as-is; new pasted material
  gets only light, obvious typo fixes — never rewritten or embellished.

## To resume

Just paste new material the way you always have ("add this under COSCA", a big
character-notes dump, or an exported additions JSON) — the routing, merge, and ship
steps are all documented above and in the skill/IMPLEMENTATION.md, so a fresh
session can follow the same process without you re-explaining it.
