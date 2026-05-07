# LLM Wiki — Second Brain Design

**Date:** 2026-05-07  
**Domain:** Work / Business  
**Primary use case:** Recall  
**Scale:** 1–3 active projects at a time  
**Location:** `~/Documents/Second Brain/`

---

## Architecture

Three layers:

1. **Raw sources** (`raw/`) — immutable. You put files here; the LLM only reads them, never modifies them. Source of truth.
2. **Wiki** (`wiki/`) — LLM-maintained markdown. The LLM creates, updates, and cross-links all pages here.
3. **Schema** (`CLAUDE.md`) — rules for the LLM wiki agent. Defines operations, templates, naming conventions.

---

## Folder Structure

```
~/Documents/Second Brain/
  CLAUDE.md              ← schema: LLM wiki agent rules
  index.md               ← master directory of all projects + pages
  log.md                 ← append-only operation history

  raw/                   ← immutable source documents
    project-x/
    project-y/
    assets/              ← downloaded images

  wiki/                  ← LLM-maintained pages
    _overview.md         ← high-level summary of all active projects
    project-x/
      index.md           ← project summary, status, key people, open items
      people.md          ← contacts, roles, relationships
      decisions.md       ← decisions log with dates
      meetings/          ← one file per meeting (YYYY-MM-DD-topic.md)
    project-y/
      ...
```

---

## Operations

### ingest
Trigger: "ingest [filename]" or drop file in `raw/project-x/` and say "ingest this."

LLM workflow:
1. Read the source file from `raw/`.
2. Ask 1–2 clarifying questions if context is ambiguous (project assignment, date, etc.).
3. Write or update relevant wiki pages (meetings, people, decisions, project index).
4. Update `index.md` with any new pages.
5. Append entry to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`

A single ingest may touch multiple wiki pages. The LLM notes which pages were updated in the log entry.

### query
Trigger: any recall question ("What did we agree on X?", "What's the status of Project Y?").

LLM workflow:
1. Read `index.md` to find relevant pages.
2. Read those pages.
3. Answer with inline citations to wiki page paths.
4. If the answer required meaningful synthesis, offer to file it as a new wiki page.

### lint
Trigger: "lint the wiki."

LLM checks for:
- Orphan pages (no inbound links from index or other pages)
- Stale open items (unchecked items older than 30 days)
- Missing cross-links (person mentioned in a meeting but not in `people.md`)
- Data gaps worth filling (project has no `decisions.md` entries)

Returns a punch list. User decides which items to act on.

---

## Page Templates

### Project index — `wiki/[project]/index.md`

```markdown
# [Project Name]
**Status:** Active | Paused | Closed  
**Last updated:** YYYY-MM-DD  
**Client:** Name | **Key contact:** Name

## Summary
2–3 sentence overview of the project and current state.

## Open items
- [ ] Item — owner — due date

## Key decisions
- YYYY-MM-DD: Decision summary → see decisions.md

## People
→ see people.md

## Recent meetings
→ see meetings/YYYY-MM-DD-topic.md
```

### Meeting note — `wiki/[project]/meetings/YYYY-MM-DD-topic.md`

```markdown
# YYYY-MM-DD — [Topic]
**Attendees:** Names  
**Source:** raw/[project]/[filename]

## Key points

## Decisions made

## Action items

## Follow-up needed
```

### People — `wiki/[project]/people.md`

```markdown
# People — [Project Name]

## [Full Name]
**Role:** Title / relationship to project  
**Contact:** email or phone (if known)  
**Notes:** relevant context
```

### Decisions — `wiki/[project]/decisions.md`

```markdown
# Decisions — [Project Name]

## YYYY-MM-DD — [Decision title]
**Made by:** Names  
**Context:** Why this decision was made  
**Decision:** What was decided  
**Source:** raw/[project]/[filename] or meetings/YYYY-MM-DD-topic.md
```

---

## index.md Structure

Master directory. LLM reads this first on every query.

```markdown
# Second Brain Index
Last updated: YYYY-MM-DD

## Active Projects
- [Project X](wiki/project-x/index.md) — one-line summary

## Pages
### Project X
- [Index](wiki/project-x/index.md) — project overview and open items
- [People](wiki/project-x/people.md) — contacts and roles
- [Decisions](wiki/project-x/decisions.md) — decision log
- [Meeting YYYY-MM-DD Topic](wiki/project-x/meetings/YYYY-MM-DD-topic.md) — brief description
```

---

## log.md Structure

Append-only. Each entry prefixed for grep-ability.

```markdown
# Log

## [YYYY-MM-DD] ingest | Source Title
Pages updated: wiki/project-x/meetings/..., wiki/project-x/index.md
Notes: brief description of what changed

## [YYYY-MM-DD] query | Question asked
Answer summary. Filed as: wiki/project-x/page.md (if applicable)

## [YYYY-MM-DD] lint | Lint pass
Issues found: N. Actions taken: description.
```

---

## Naming Conventions

- Project folders: lowercase-hyphenated (e.g., `acme-corp`, `website-redesign`)
- Meeting files: `YYYY-MM-DD-brief-topic.md`
- Raw files: keep original filename, no renaming
- Wiki pages: lowercase, hyphenated where multi-word

---

## Constraints

- LLM **never** modifies `raw/`. Read-only.
- LLM **always** updates `index.md` and `log.md` after every ingest.
- Pages stay focused — one purpose per file. Don't merge meetings into one file.
- Keep `index.md` under ~150 lines (add pagination by project if needed as scale grows).
