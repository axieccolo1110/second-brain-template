# Second Brain Template

A Karpathy-style **LLM wiki** for professional knowledge, run with [Claude Code](https://claude.com/claude-code). You drop raw material into a folder; Claude synthesizes it into durable, interlinked wiki pages that compound over time. You approve every change.

```
raw/  ──/ingest──▶  wiki/  ──(on request)──▶  reports/
 │
 └─ Teams transcripts ──/ingest──▶ meetings/ (protocols) + wiki/ (knowledge)
```

## Folder structure

| Folder | What lives there |
|--------|------------------|
| `raw/` | Source material, immutable once ingested: notes, article captures, PDF transcriptions, Teams transcripts (`.vtt`/`.docx`). Flat, any filename. |
| `wiki/` | Pages maintained by Claude, in English, with YAML frontmatter. `index.md` is the table of contents, `log.md` records what was ingested. |
| `meetings/` | Meeting protocols generated from transcripts, plus `glossary.md` for speech-recognition corrections. |
| `reports/` | Point-in-time compilations derived from the wiki (talk prep, summaries). Never ingested. |
| `projects/` | Time-bound work, one subfolder per project with a `project.md` (goal, acceptance criteria, log). |

All conventions are spelled out in [`CLAUDE.md`](CLAUDE.md), which Claude reads automatically.

## Prerequisites

- **Claude Code**
- **python3** — converts Teams `.vtt` transcripts (`scripts/vtt2md.py`, standard library only)
- **pandoc** — converts Teams `.docx` transcripts (`brew install pandoc`)
- *Optional:* **Node.js / npx** for the Playwright MCP server in `.mcp.json`, used to capture web pages into `raw/`. Claude Code asks you to approve the server on first start; `npx` needs network/proxy access to download it. Remove `.mcp.json` if you don't need it.

## Quickstart

1. Click **Use this template** on GitHub and create the new repository as **private** — `raw/` and `meetings/` will hold confidential material.
2. Clone it and start Claude Code in the folder: `claude`
3. Put a file into `raw/` (e.g. a Markdown note).
4. Run `/ingest`, review the proposal, confirm.
5. Ask questions with `/query`, check health with `/lint`.

## Skills

- **`/ingest`** — finds files in `raw/` not yet in `wiki/log.md`, proposes new or updated wiki pages and writes them after your approval. Teams transcripts additionally get a protocol in `meetings/` (one approval per transcript).
- **`/query`** — answers questions from the wiki with citations.
- **`/lint`** — checks broken links, missing index entries, stale and outdated pages, report references and project consistency. Read-only.

## Page lifecycle

New pages start as `draft`. Only you set `reviewed`. When new material changes a reviewed page, it becomes `outdated` and returns to `draft` once updated. Each page also carries a `confidence` (`high` / `medium` / `low`).

## Meeting protocols use German terms

The transcript rules in `.claude/commands/ingest.md` expect some German vocabulary: task status `offen`/`erledigt`, `[unklar]` for uncertain items, "vertraulich" to mark a meeting confidential (protocol only, no wiki changes), and "TN-Protokoll" for a participant version. Adjust the command if you work in another language.

## Removing the example

The template ships with one example so you can see the result of an ingest. Delete it before you start — this is the one allowed exception to "raw files are immutable":

1. `raw/example-llm-wiki-pattern.md`
2. `wiki/llm-wiki-pattern.md`
3. the `## Example` section in `wiki/index.md`
4. the example row in `wiki/log.md`
5. the `Cloud Code` example row in `meetings/glossary.md`

## Tips

- Open the folder as an [Obsidian](https://obsidian.md) vault to browse the wiki with graph view and backlinks (`.obsidian/` is gitignored).
- New insights from a report or a finished project go back into the wiki as a note in `raw/` plus `/ingest` — never by editing `wiki/` directly.
