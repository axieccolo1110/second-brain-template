---
name: review
description: Review draft wiki pages by sampling — group drafts into blocks, propose a sample per block, set reviewed on the blocks the user releases
model: sonnet
---

# /review — Release draft pages by sampling

> **Execute steps 1–3 immediately in this turn.** Do not end your turn or announce that the skill is "running" — start with step 1 right away and stop after presenting the sample (step 3). Change nothing before the user decides.

## Trigger
User runs `/review`, optionally with a scope (e.g. `/review kubernetes`, `/review raw/<file>.md`, or a tag). Without a scope, all `draft` pages are in scope.

## Rules (from CLAUDE.md, Status lifecycle)
- Only the user decides `reviewed`. This command sets it only for pages the user explicitly releases in step 4.
- `reviewed` means: the page is a faithful synthesis of its sources (and correct where the user has own knowledge) — not agreement with a source's opinions.
- Only the `status` field changes. Do not touch `updated`, content, or any other field. Never promote `outdated` pages; they must be updated (→ `draft`) first.

## Steps

### 1. Collect drafts
- List all `wiki/*.md` (except `index.md`, `log.md`) with `status: draft` in the frontmatter, limited to the scope if one was given.
- For each page read `title`, `sources`, `tags`, `confidence`.
- If there are none, report "Nothing to review — no draft pages in scope." and stop.

### 2. Group into blocks
- Group pages by origin: pages sharing the same source file(s) or the same ingest (rows in `wiki/log.md`) form a block. For large sources, split along the source's structure (parts, chapters) or the index sections, aiming for blocks of roughly 5–15 pages.
- Pages that fit no group form a block of their own.

### 3. Propose a sample
Present one table per block:

| Block | Pages | Sample | Why these |
|---|---|---|---|

- Per block pick 2–3 representative pages: the hub or overview page, the page with the most sources or the most merged content, and one page that contains numbers, tables or transcribed figures.
- List **every** page with `confidence: medium` or `low` separately as "check individually".
- Give the total: pages in scope vs pages to read.
- Ask the user which blocks to release (e.g. "all", "blocks 1–3", "all except X").

### 4. Set status (after the user's decision)
- Set `status: reviewed` on exactly the pages the user released; leave all others as `draft`.
- Report the count and list per block, and any page skipped because it was not `draft`.
- Propose a commit message that names the batch (scope, blocks, "set to reviewed on user instruction after sampling"). Commit only if the user asks.

## Notes
- Corrections the user finds while sampling are content changes, not status changes: apply them first (the page stays `draft`), then ask again whether the block can be released.
- If the user rejects a sample page, do not release its block; offer to fix the page or to review the block more closely.
