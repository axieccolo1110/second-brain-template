# Note: the LLM wiki pattern

Example source note shipped with the template. Delete it together with its wiki page (see README).

Idea popularised by Andrej Karpathy: instead of asking an LLM to search a pile of documents every time (classic RAG), let it maintain a small wiki of its own.

- Raw sources (articles, notes, transcripts) are collected unchanged in one place.
- The LLM reads each new source once and writes what it learned into durable, interlinked pages — creating new pages or extending existing ones.
- Pages carry metadata: which sources they rest on, when they were last updated, how confident the synthesis is.
- Questions are answered from the wiki, with citations back to pages and sources.
- Knowledge compounds: every new source improves existing pages instead of adding another isolated document.
- A human stays in the loop: the LLM proposes changes, the human approves them, and only the human marks pages as verified.
- Periodic health checks catch broken links, stale pages and missing index entries.

Why it works well with coding agents: the wiki is plain Markdown in a git repo, so the agent can read, write, diff and search it with its normal file tools.
