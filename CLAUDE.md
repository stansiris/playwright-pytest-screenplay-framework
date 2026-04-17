# CLAUDE.md

> Repository instructions live in [AGENTS.md](AGENTS.md). Read that file first — it contains all architectural rules, naming conventions, and validation discipline for this project.

## Skills

Custom skills for this repository are in [.agents/](.agents/). Read the relevant `SKILL.md` before generating code for that skill.

| Skill | Path | Purpose |
|-------|------|---------|
| `python-screenplay-generator` | [.agents/python-screenplay-generator/SKILL.md](.agents/python-screenplay-generator/SKILL.md) | Generate Targets, Tasks, Questions, and test scaffolding |
| `gherkin-planner` | [.agents/skills/gherkin-planner/SKILL.md](.agents/skills/gherkin-planner/SKILL.md) | Plan Gherkin scenarios |
| `planner` | [.agents/skills/planner/SKILL.md](.agents/skills/planner/SKILL.md) | Plan Screenplay implementation |

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
