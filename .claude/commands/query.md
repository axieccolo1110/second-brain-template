---
name: query
description: Search the wiki and synthesize answers with citations
---

# /query — Ask questions against the wiki

> **Execute these steps immediately in this turn.** Do not end your turn or announce that the skill is "running" — start with step 1 right away and only stop after presenting the answer in the output format below.

## Trigger
User runs `/query <question>` with a natural language question.

## Steps

### 1. Parse the question
Identify key topics, concepts, and intent from the user's question.

### 2. Search wiki pages
- Read `wiki/index.md` to get an overview of available pages.
- Search wiki pages by:
  - **Tags** in frontmatter matching question topics.
  - **Title** relevance.
  - **Content** keyword and concept matching.
- Read the most relevant pages in full.

### 2b. Check active projects
- Glob `projects/*/project.md` and read the frontmatter of each. Consider only projects with `status: active` or `paused`.
- If the question touches a project (title, goal, `related_wiki`), read its `project.md` in full.
- Project content is work in progress, not verified knowledge. Always label it as such in the answer and never mix it into wiki-based claims.

### 3. Synthesize an answer
- Compose a clear, direct answer to the question.
- Draw from multiple wiki pages when relevant.
- Note the `confidence` level of source pages — flag when relying on low-confidence material.
- If the wiki doesn't contain enough information, say so explicitly and suggest what raw material could fill the gap.

### 4. Cite sources
- Reference specific wiki pages using `[[page-name]]` links.
- Where a wiki page traces back to raw sources, mention those too for traceability.
- Cite projects by path (`projects/<slug>/project.md`), not as `[[...]]` links, and mark them as "project, current state".

## Output format
```
**Answer**: <synthesized answer>

**Sources**:
- [[page-name]] — <what this page contributed>
- [[other-page]] — <what this page contributed>

**Confidence**: <overall confidence based on source page confidence levels>
```

If the question cannot be answered from the wiki:
```
**Not enough information in the wiki.**

To answer this, consider adding source material about <suggested topics> to `raw/`.
```

### 5. Offer to save as report
After answering, ask whether to save the answer as a report. Only on confirmation, write `reports/YYYY-MM-DD-<topic>.md` with frontmatter (`type: report`, `title`, `date`, `purpose`, `based_on` = cited wiki pages only, not projects). Do not touch `wiki/`, `index.md`, or `log.md`.

## Rules
- Never fabricate information not present in the wiki pages.
- Be transparent about gaps and confidence levels.
- Projects are read-only here: never modify `projects/` from `/query`.
- Prefer breadth (citing multiple pages) over depth when the question spans topics.
