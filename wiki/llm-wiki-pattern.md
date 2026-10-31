---
title: "LLM Wiki Pattern"
sources:
  - raw/example-llm-wiki-pattern.md
created: 2026-10-29
updated: 2026-10-29
tags: [llm, knowledge-management, example]
related: []
status: draft
confidence: high
---

# LLM Wiki Pattern

> Example page shipped with the template — delete it together with its source (see README).

An approach to personal knowledge management in which an LLM maintains a wiki from raw sources, instead of searching the raw sources on every question.

## How it works

1. **Collect** — raw material (notes, articles, transcripts) is stored unchanged and never edited.
2. **Synthesize** — the LLM reads each new source once and folds its content into durable pages: it extends existing pages or creates new ones.
3. **Approve** — the LLM proposes changes; a human confirms before anything is written.
4. **Query** — questions are answered from the wiki, citing pages and sources.
5. **Maintain** — health checks find broken links, stale pages and missing index entries.

## Properties

- **Compounding** — each source improves existing pages rather than adding another isolated document.
- **Traceable** — every page lists the sources it rests on, plus a status (`draft`, `reviewed`, `outdated`) and a confidence level.
- **Human-verified** — only a human promotes a page to `reviewed`.
- **Tool-friendly** — plain Markdown in git, so coding agents can read, write, diff and search it with ordinary file tools.

## Compared to classic RAG

| | Classic RAG | LLM wiki |
|---|---|---|
| When the LLM reads sources | on every question | once, at ingest |
| What is stored | raw chunks + embeddings | synthesized pages |
| Contradictions | surface at query time | resolved at ingest, visibly marked |
