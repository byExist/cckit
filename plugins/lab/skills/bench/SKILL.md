---
name: bench
description: Run variants of a harness component (skill, hook, agent, prompt) in isolation and measure them.
argument-hint: "[target component] [axes (optional)]"
disable-model-invocation: true
---

# Bench

Run variants of a harness component in isolation and measure them. No quality verdicts — the criteria and fixtures belong to the target's tests/; this skill lays results side by side.

Each component has its own injection path, isolation method, and observation channel. Identify the target's kind, and read its playbook before designing anything.

- Doctrine text of a skill or agent → references/skill.md
- Hooks → references/hook.md
- Agent registration and name resolution → references/agent.md
- CLAUDE.md and global prompts → references/claude-md.md
- Anything unlisted → follow the nearest playbook, and mark the method unproven in the report

There are two rigs. The text rig (inline injection into a subagent — cheap, parallel, blind to the loading path) and the live rig (`claude -p` — exercises the real injection path, costs more, inherits the caller's environment). The playbook decides which one applies.

## Design

1. Take fixtures and their per-fixture readers or arguments from the target's tests/. Absent those, settle collection with the user first. A collection session inherits the caller's CLAUDE.md and its style contaminates the output, so generate from a plain task without steering — and record any steering in the provenance.
2. Pick the axes: variants (ablations — remove one line or block at a time), models, execution mode. Default small — at most 9 cells.
3. State the cell count and expected tokens (40-70k per cell) and confirm before running.

## Execution

Follow the playbook's rig; three principles are common.

1. Copy each fixture into a temp directory, one copy per cell. Exposing the tests/ directory to an executor leaks provenance and expectations and contaminates the run.
2. The executor gets only the variant inline, the copy path, and the arguments.
3. Record tokens, duration, and tool calls per cell from the completion reports.

## Reading

1. Measure outputs yourself — wc and diff. Never trust an executor's self-reported numbers.
2. Report a matrix table: per cell, size delta, tokens, duration, cost, and the output path. For cost, look up current per-model rates at run time and quote an approximation — never hardcode a rate table.
3. Hand interpretation to the caller without verdicts, but relay qualitative signals per cell — stated premises, close-call reports, unexpected edits. When a result looks decisive, suggest repeating the same cell — variance is the cheapest discovery.
