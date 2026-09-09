# Writer's Thesaurus — Implementation Notes

Reference doc for how this tool is built, so a future session (me or Amel) doesn't
have to re-derive it. Pairs with the `thesaurus-notebook-intake` skill, which covers
the day-to-day workflow of adding new pasted material; this doc covers the
architecture underneath it.

## File map

All paths below are inside the connected folder **`0One Notebooks`** on Amel's Mac.

| Path | What it is |
|---|---|
| `Writer's Thesaurus.html` | The shipped, self-contained file Amel opens. Fully static — all data is embedded inline as JSON in a `<script type="application/json">` tag. No network calls, works offline. |
| `_thesaurus_build/data.json` | **Source of truth.** Every headword and entry in the thesaurus. Edit this, then regenerate — never hand-edit the HTML. |
| `_thesaurus_build/generate.py` | Pure renderer. `python3 generate.py <data.json> <output.html>`. Reads only data.json (never the previous HTML), wraps it in the page template, writes the output. Deterministic and safe to overwrite the HTML with. |
| `beats/Beats Thesaurus.html` | The original, single-notebook prototype (just the "Beats" notebook). Left in place, untouched, superseded by the file above but not deleted. |
| Various notebook folders (`body`, `personality`, `Smells`, `Metaphors`, etc.) | Amel's original source material — PDFs (pulled quotes, one per file, usually a header + a Peake/Catton/Pratchett/etc. citation), a couple of `.docx`/`.md` files. These were the one-time seed for data.json; not read again unless rebuilding from scratch. |

## Data schema

```json
{
  "Notebook Name": {
    "Headword": [
      { "text": "the beat/entry text", "source": "optional citation string" },
      { "text": "...", "image": "data:image/jpeg;base64,..." }
    ]
  }
}
```

- Every notebook is a flat map of headword → list of entries.
- An entry is `{text, source?}` normally; the Eyes-shape entries under **Body** additionally
  carry `image` (a base64 data URI) instead of relying on text alone.
- `source` is optional and rendered as a small italic citation under the entry.
- No entry has an id; identity for dedup purposes is exact-match on `text` within a
  headword. Always check before inserting — the generator does not dedupe for you.
- data.json never contains deletion state — that only ever exists as a `__deleted`
  tombstone in a browser's localStorage (see "Delete (×)" below) until it's folded
  back in by actually removing the entry here.

## Notebooks (as of the last full rebuild)

23 notebooks, ~284 headwords, ~1764 entries. Origins:

- **Beats** — the original body-part/gesture notebook (38 headwords). Mix of pulled
  quotes (mostly Mervyn Peake's Gormenghast) and short crisp original beats Claude
  wrote on request ("propped his elbow on the table" style — no metaphor).
- **Body** — richer body-part folder (68 headwords): individual parts, "Types of X"
  catalogs (Beard Styles, Smile Types, etc.), an **Eyebrows** headword (merged from
  two source files), an **Eye**/**Eye Pictures** headword, and ten **`<Shape> Eyes`**
  headwords (Almond Eyes, Hooded Eyes, Monolid Eyes, …) holding embedded reference
  photos from the source `eyes/` subfolder.
- **Body Language Reference** — parsed from a pre-existing curated markdown file
  (`body/Body_Language_Reference_for_Writers.md`) with table rows of the form
  `Name — Description (Traits)`, plus a Craft Notes headword.
- **Personality** — full character sketches pulled from books Amel's read (Gormenghast,
  The Luminaries, Dune, First Law, etc.), trait-summary blurbs extracted from pasted
  character notes, **and** (as of the "Joe Beats" consolidation) that same character's
  book-specific action/dialogue beats — all under one headword per character, e.g.
  **Glokta** holds both his sketch-paragraph entries and his short quoted beats. Not
  chopped into uniform micro-beats — sketch entries stay paragraph-length, beat
  entries stay short, side by side under the same headword.
- **Everything else** (Bus Observation, My Own Observation, Clothes, From Books, Smells,
  Rural Setting, Metaphors, Food, Animals, Sounds, Colors, Taste & Texture,
  Nature & Trees, Automobile, Locations, Words, Time, Painting, Loose Notes) — one
  notebook per original source folder (or, for Loose Notes, three stray top-level
  files that weren't in any folder), same flat headword→entries shape throughout.

There is no longer a separate `<Book> Beats` notebook pattern — a "Joe Beats"
notebook existed for a while (Jezal, Bayaz, Longfoot, Salamo Narba, General
Vissbruck, Glokta, Vitari, Cosca, Vurms) but Amel had it merged into Personality:
every one of those headwords already existed there as a character sketch, so the
beats were folded in as additional entries under the same headword (Vurms, which
didn't exist yet, was created fresh), and the Joe Beats notebook was deleted. Going
forward, book-specific character beats route straight into **Personality** under
the character's existing (or new) headword — see the intake skill.

## The HTML page's own behavior

- **Notebook switcher** (top-right `<select>`) + **headword sidebar** (scoped to the
  active notebook, with its own filter box since some notebooks are long) +
  **global search** (spans every notebook, shows `Notebook → Headword` per hit,
  capped at 400 results).
- **"Add a beat"** (a `<details>` under each headword's entry list) writes to
  `localStorage` under key `writersThesaurus_v2`, namespaced
  `{ notebook: { headword: [entries] } }`. **This never touches data.json** — it's
  purely client-side, per-browser. Entries added this way render with a "yours" tag
  and a hover-to-delete ×.
  - There's a one-time migration on load from the older single-notebook prototype's
    storage key (`beatsThesaurus_v1`) into the new namespaced store, so nothing from
    early testing is silently lost.
- **"Export my additions (.json)"** in the footer downloads the current localStorage
  contents. This is the bridge back to permanence — see the intake skill for how an
  exported file gets folded into data.json.
- **Delete (×)** — every entry, built-in or "yours" alike, has a hover-to-reveal ×.
  - Deleting a **"mine"** entry just splices it out of `mine[notebook][headword]` in
    localStorage (and drops the headword entirely from `mine` if that was its last
    entry — same as before this feature existed).
  - Deleting a **built-in** (data.json-sourced) entry can't touch data.json from
    client-side JS, so instead it's recorded as a **tombstone**:
    `mine.__deleted[notebook][headword] = ["exact entry text", ...]`. `entriesFor()`
    filters any built-in entry whose text appears in that list before rendering, so
    it disappears everywhere (headword view *and* search results) and stays gone
    across reloads. It rides along automatically in "Export my additions" since it's
    just another property of the same `mine` object — when folding an export into
    data.json, check for `__deleted` and actually remove those entries (or leave them
    out) rather than merging them back in.
  - Works from both the headword view and the global search-results view (shared
    `wireDeleteButtons()`).
- **"+ Add section"** at the bottom of the headword sidebar lets Amel create a brand
  new headword in the current notebook from the page itself (e.g. a new character —
  "Vurms" — the same way "Glokta" exists as a headword in Personality). Case-insensitive
  duplicate names are rejected with an inline message. A new section starts as
  `mine[notebook][name] = []` (0 entries, empty-state shown) and is selected
  immediately so the Add-a-beat form is right there. Like everything else added from
  the page, a new section lives only in localStorage until exported.

## Adding new material — quick version

(Full routing rules live in the `thesaurus-notebook-intake` skill; this is the gist.)

1. Amel pastes raw notebook material (character notes: trait blurb + short beats +
   citation) *or* sends an exported "my additions" JSON from the page.
2. For pasted raw material, classify into up to two destinations per chunk (both
   land in **Personality**, under the character's headword — create the headword if
   new): trait/summary prose as paragraph-length entries; short character-attributed
   action/dialogue beats as their own short entries (citation attached as `source`
   where given). Separately, where a beat clearly maps onto an existing generic
   **Beats** headword by meaning (not literal word — "grin" still means Smile), file
   a generalized, name-stripped copy there too, so plain-word search catches
   synonyms. Light touch on this last step — only the clean matches, not every line.
3. For an exported JSON, no reclassification needed — merge each entry into its
   existing notebook/headword, deduped.
4. Merge into `_thesaurus_build/data.json` (always dedupe on exact `text` match),
   regenerate via `generate.py`, overwrite `Writer's Thesaurus.html` in place.

## Testing after a change

The page is plain HTML/CSS/JS with no build step, but since edits happen headlessly
(no visual check), verify with a quick Playwright pass after any non-trivial change:
stage the regenerated HTML into the container, launch Chromium
(`/opt/pw-browsers/chromium`), and check for zero console/page errors, that the
notebook `<select>` lists the expected count, that a known headword loads, and that a
search term surfaces a newly-added entry (this last check is what caught nothing
being broken when the Smile cross-filing was added).

## Decisions made along the way (so they don't get re-litigated)

- **Beats and Body stay separate notebooks**, even though headwords overlap (chin,
  hand, elbow, etc.) — Amel's explicit call.
- **Eyes reference photos are embedded** as base64 in data.json/HTML rather than
  linked externally, so the file stays fully self-contained and offline-usable. This
  is most of the file's size (~3.5MB of the ~3.7MB total).
- **Personality entries are not chopped into micro-beats** — a character's sketch
  stays as one or a few paragraph-length entries, unlike Beats/Body where each line
  is its own short entry.
- **Typos and rough/truncated fragments in the original source material are preserved
  as-is** — this collection has always had some intentionally imperfect entries (OCR
  artifacts, mid-sentence cuts). New pasted material gets only light, obvious typo
  fixes, never rewriting or embellishing.
- **The generic cross-filing step is deliberately light-touch** — Amel pushed back
  on over-engineering this ("we don't need to go overboard as you have a very good
  search feature"), so it exists specifically to close the synonym gap plain search
  can't, not to duplicate everything everywhere.
- **No separate `<Book> Beats` notebooks** — tried once ("Joe Beats"), then Amel had
  it merged straight into Personality under each character's existing headword and
  the notebook deleted. One headword per character holds both the sketch and the
  beats now; don't recreate a book-specific beats notebook for future material.
