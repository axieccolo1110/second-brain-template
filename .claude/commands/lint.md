---
name: lint
description: Check wiki and project health — broken links, missing index entries, stale pages, project consistency
model: sonnet
---

# /lint — Wiki health check

> **Execute these checks immediately in this turn.** Do not end your turn or announce that the skill is "running" — start with check 1 right away and only stop after presenting the full lint report.

## Trigger
User runs `/lint`.

## Checks

### 1. Broken links
- Scan all wiki pages for `[[page-name]]` references.
- Ignore links inside fenced code blocks (``` … ```) and inline code spans (`` `[[example]]` ``): they are examples, not links. Strip both before matching.
- Verify that each referenced page exists as `wiki/<page-name>.md`. Origin links to meeting protocols (`[[YYYY-MM-DD-<slug>]]`) resolve against `meetings/<name>.md`.
- Report any broken links with the source page and the missing target.

### 2. Missing index entries
- List all `.md` files in `wiki/` (excluding `index.md` and `log.md`).
- Check whether each page is referenced in `wiki/index.md`.
- Report any pages not listed in the index.

### 3. Stale low-confidence pages
- Find pages where `confidence: low` and `updated` is more than 3 months ago.
- Suggest these pages need better sourcing or should be reviewed.

### 4. Outdated pages
- Find pages where `status: outdated`.
- List them as candidates for refresh or removal.

### 5. Orphaned pages
- Find wiki pages whose `sources` list references raw files that no longer exist.
- Report these as potential issues (though raw files should never be deleted, this catches mistakes).

### 6. Report references
- For each file in `reports/` (ignore `.gitkeep` and `README.md`), read the `based_on` list in its frontmatter.
- Verify each entry exists as `wiki/<page-name>.md`.
- Reports are not wiki pages: never flag them as missing from the index.

### 7. Projects
- Scan `projects/`. Projects are not wiki pages: never flag them as missing from the index.
- **Structure**: report loose files directly in `projects/` (ignore `.gitkeep` and `README.md`; others should be in a project subfolder) and subfolders without `project.md`.
- **Frontmatter**: `project.md` must have `type: project`, `title`, `status` (`active | paused | done | cancelled`), `started`, `owner`. Report missing fields or invalid status values.
- **Acceptance criteria**: report projects without an "Acceptance criteria" section or without any `- [ ]` / `- [x]` item.
- **Status consistency**:
  - `done` with unchecked criteria (`- [ ]`) → inconsistent.
  - `done` or `cancelled` without `ended` date, or `active`/`paused` with an `ended` date.
  - `cancelled` without a reason in the log.
  - `active` with all criteria checked → suggest closing (the user decides).
- **Stale projects**: `active` projects whose newest log entry (fallback: file modification date) is older than 30 days; `paused` older than 90 days. Suggest resuming, pausing, or cancelling.
- **Closed projects without retro**: `done` or `cancelled` projects with no matching retro note in `raw/` (heuristic: a raw file mentioning the project slug or title). Suggest writing one and running `/ingest`.
- **`related_wiki`**: verify each entry exists as `wiki/<page-name>.md`.

## Output format
```
## Wiki Lint Report

### Broken Links
- <page> references [[missing-page]] (line X)
...

### Missing from Index
- <page> is not listed in index.md
...

### Stale (low confidence, >3 months old)
- <page> — last updated YYYY-MM-DD, confidence: low
...

### Outdated
- <page> — marked as outdated
...

### Orphaned Sources
- <page> references raw/... which does not exist
...

### Projects
- <project> — <issue, e.g. no acceptance criteria / done with open criteria / stale since YYYY-MM-DD>
...

### Summary
X issues found (Y broken links, Z missing from index, ..., N project issues)
```

If everything is clean:
```
## Wiki Lint Report

All clear — no issues found.
```

## Rules
- This is a read-only operation. Never modify any files.
- Report issues with enough context to act on them (page name, line, specific link).
