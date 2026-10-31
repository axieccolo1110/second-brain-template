---
name: ingest
description: Scan raw/ for new source files and propose wiki page changes (meeting transcripts also get a protocol in meetings/)
---

# /ingest — Process raw sources into wiki pages

> **Execute these steps immediately in this turn.** Do not end your turn or announce that the skill is "running" — start with step 1 right away and only stop after presenting the proposal (step 3) or reporting that there is nothing to ingest.

## Trigger
User runs `/ingest`, optionally with a path argument to limit scope (e.g. `/ingest raw/2026-10-23-source-file.md`).

## Steps

### 1. Discover new files
- List all files in `raw/` recursively (exclude `.gitkeep`).
- **Teams originals** (`.vtt`, and `.docx` that is a Teams transcript, recognisable by speaker lines such as `Name: text` or `Name  0:01`; if unsure, ask) are excluded from the log diff below. An original is already handled if a transcript in `raw/` points to it via `source_original`. Otherwise convert it (see "Transcripts → Conversion"); the converted `.md` is what gets ingested. Originals never appear in `log.md`. A `.docx` that is not a meeting transcript is an ordinary source.
- Read `wiki/log.md` and extract the "Source File" column to get already-processed files.
- Compute the diff: files present in `raw/` (without Teams originals) but not in `log.md` are **new**.
- If no new files, report "Nothing to ingest — all raw files are already processed." and stop.
- **Transcripts are processed one at a time**, each with its own proposal and approval, separately from other raw files. If several are new, list them and start with the oldest meeting date. After one transcript is approved and written, continue with the proposal for the next one in the same run.

### 2. Read and analyze each new file
For each new file:
- Read its full content.
- Determine the topic and key concepts.
- Decide whether the content fits an existing wiki page (update) or needs a new page (create).
- When updating, identify which sections to extend or revise.

### 3. Propose changes
Present the user with a clear summary of proposed changes:
- For each **new page**: show the proposed filename, title, tags, and a brief content outline.
- For each **updated page**: show what will change and why.
- Group proposals logically if multiple files are being ingested.

**Wait for user confirmation before proceeding.** Do not write any files until the user approves.

### 4. Execute changes (after confirmation)
For each approved change:
- **New pages**: Create the wiki page in `wiki/` with proper YAML frontmatter (title, sources, created, updated, tags, related, status: draft, confidence based on source quality).
- **Updated pages**: Update the existing page content, add the new source to `sources`, update the `updated` date, and adjust `confidence` if warranted.
- **Update `wiki/index.md`**: Add new pages to the index, organized by topic/tag.
- **Prepend to `wiki/log.md`**: Insert new rows directly below the table header (newest first). One row per source file processed, with date, source path, action (created/updated), and target wiki page.

### 5. Summary
Report what was done: how many files ingested, pages created, pages updated.

## Transcripts
Meeting transcripts (`type: transcript` in the frontmatter, or a Teams original to convert) produce two results: a **protocol** in `meetings/` and **knowledge** for topic pages. The transcript itself never becomes wiki content.

### Conversion
- `.vtt`: `python3 -I scripts/vtt2md.py convert raw/<file>.vtt raw/<date>-meeting-<slug>.md`, frontmatter on stdin (`info` first for speakers).
- `.docx`: `pandoc -t gfm --wrap=none raw/<file>.docx`, write the text unchanged below the frontmatter into `raw/<date>-meeting-<slug>.md`.
- Frontmatter: `type: transcript`, `date`, `participants`, `speakers`, `context` (one line: what the meeting was), `completeness` (`full`, or `partial` if the recording starts late, ends early or has gaps), `language`, `source_original: raw/<original file>`. Never overwrite an existing file; the original stays in `raw/`.
- Conversion is the only write before approval: it adds a verbatim copy to `raw/` and changes nothing else. Convert each original right before its own proposal.
- Slug: lowercase, hyphenated meeting title. Date from the content or filename; otherwise use the file's modification date and flag it in the proposal for confirmation.
- No timestamps or no speakers (common in `.docx`): say so in the proposal; evidence then cites paragraphs as `[¶n]` (n = nth non-empty paragraph of the transcript body below the frontmatter, starting at 1).

### Before drafting
- Read `meetings/glossary.md` and correct names, product names and acronyms accordingly. If unsure, write "[unklar]" instead of guessing.
- Leave out noise (small talk, repetition, technical problems). Group by topic, not chronologically.
- Discussed ≠ decided: treat hesitation or reservations ("ich versuch's", "eigentlich", "müssten wir mal") deliberately; a proposal without agreement is not a decision.
- **Date conversion**: turn relative deadlines into an ISO date counted from the meeting date ("bis Freitag" → the next Friday; "Ende nächster Woche" → Friday of next week; "nächste Woche" → "Woche ab <Monday's date>"). Ambiguous ones ("vor dem Release") → "[unklar]".
- **Check pass**: before showing the draft, check every decision and task against the transcript once more: was it said like this, was it really decided, is the owner right?

### Protocol (`meetings/<date>-<slug>.md`)
- Language of the meeting. Participants' names appear only here.
- Frontmatter:
  ```yaml
  ---
  type: meeting
  title: "..."
  date: 2026-10-29
  participants: [..]
  source: "[[raw/<transcript file without .md>]]"
  topics: []          # topic pages touched, as "[[page]]"
  ingest: true        # false = confidential
  status: draft
  ---
  ```
- Sections (headings in the meeting language): **Decisions** (short rationale + transcript timestamp) · **Not decided** (contested points as "Positionen: A / B") · **Tasks** (table: owner, task, due, status `offen`/`erledigt`, timestamp; no date → "offen"; no clear owner → "[Owner unklar]"; tentative commitments like "ich versuch's" marked as such) · **Open questions** · optional **Information** (facts reported in the meeting that are neither decision nor task; second-hand statements marked). Nothing invented. Neutral tone, no personal judgements.

### Topic pages
- English, regardless of the meeting language.
- **No names, no roles.** Origin noted as "Meeting [[<date>-<slug>]]" linking to the protocol; add the transcript and the protocol path to `sources`. No transcript timestamps on the page.
- Subject and process knowledge only, no statements about people, no tasks or open to-dos.
- Only decided or established facts are stated as facts. Proposals and positions from "Not decided" appear, if at all, explicitly as open ("proposed, not decided"), never as a plan or sequence.
- Existing names on a page are not cleaned up unasked; new text contains none.
- Extend existing pages; create a new page only if the topic is missing.
- Contradictions: do not overwrite. Show old / new / proposal in the draft and mark it on the page (`~~old~~ → new (date, Meeting [[...]])`) wherever the old statement occurs.
- Partial transcripts (`completeness: partial`) or text without timestamps: `confidence` at most `medium`.

### Proposal and approval
One proposal per transcript containing the protocol draft, the topic-page changes and any glossary additions. **Evidence in the draft**: under every topic-page statement and every task, give the timestamp (or `[¶n]`) and a short verbatim quote, e.g.
```
onboarding-checklist (addition):
  "New members get access in their first week."
   ↳ [00:04:12] „Zugänge gibt's in der ersten Woche.“
```
Mark uncertain points. Write nothing before approval. After approval, write the protocol, the topic pages, `index.md`, and the proposed glossary rows plus any corrections the user made as new rows in `meetings/glossary.md` (`| As transcribed | Correct | Context |`, no separate approval). Log: one row per transcript — date = ingest date, source = transcript, action e.g. `updated; protocol meetings/<file>.md`, wiki page = touched pages comma-separated (or `–`).

### Confidential (`ingest: false` or user says "vertraulich")
Protocol only, with `ingest: false`. No topic-page changes. Log row with action `skipped (ingest: false)`.

### Participant version (on request only)
"TN-Protokoll" for meeting X: produced only from the approved protocol, never from the transcript, and only output in the chat (not saved). Same content and order; remove wiki links, frontmatter, timestamps, references to `raw/` and topic pages. Plain Markdown for mail, Teams or Confluence. No "[unklar]" left: resolve it with the user first.

## Rules
- Files in `raw/` are immutable once their row is in `log.md`. Before that, corrections the user gives during the proposal go directly into LLM-authored notes (not a new note). External sources stay verbatim; corrections to them go into a separate short note.
- Only scan `raw/`. Never ingest files from `reports/` — they are derived from the wiki and would create circular sources.
- Always use `[[page-name]]` format for cross-references between wiki pages.
- Set `status: draft` on all new or substantially updated pages.
- Set `confidence` based on source quality: `high` if authoritative/detailed, `medium` if reasonable but incomplete, `low` if speculative or thin.
- Write wiki content in the language of its sources; keep terms as written in the source.
