# CLAUDE.md

> Repository instructions live in [AGENTS.md](AGENTS.md). Read that file first — it contains all architectural rules, naming conventions, and validation discipline for this project.

## Skills

Custom skills for this repository are in [.agents/](.agents/). Read the relevant `SKILL.md` before generating code for that skill.

| Skill | Path | Purpose |
|-------|------|---------|
| `planner` | [.agents/skills/planner/SKILL.md](.agents/skills/planner/SKILL.md) | Generate Screenplay plans, Gherkin scenarios, or both |
| `python-screenplay-generator` | [.agents/skills/python-screenplay-generator/SKILL.md](.agents/skills/python-screenplay-generator/SKILL.md) | Generate Targets, Tasks, Questions, and test scaffolding from an approved plan |

## Keeping Claude Code slash commands in sync

Each skill in `.agents/` has a thin wrapper in [.claude/commands/](.claude/commands/) so it appears as a `/skill-name` slash command in Claude Code.

**When adding a new skill under `.agents/`**, also create `.claude/commands/<skill-name>.md` with this shape:

```markdown
---
description: <one-line description>. Canonical skill: .agents/<path>/SKILL.md
argument-hint: "<hint>"
---

Read [.agents/<path>/SKILL.md](.agents/<path>/SKILL.md) and follow it exactly.

Arguments: $ARGUMENTS
```

The wrapper is intentionally minimal — all skill logic stays in `.agents/` as the single source of truth for both Claude Code and OpenAI Codex.
