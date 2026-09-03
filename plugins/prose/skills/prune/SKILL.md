---
name: prune
description: Remove unneeded content from a work product.
argument-hint: "[target] [reader] (each optional)"
disable-model-invocation: true
---

# Prune

Never prune in this session — dispatch to the `prose:pruner` agent. Padding is prose that serves its writer, and the writer is usually this session, so its own eye cannot pick it out.

## Dispatch

1. Take the target and the reader from the argument; absent either, infer them from the conversation. First settle what kind of writing this is and what the reader will do with it. Ask the user when unsure.
2. Secure the original to diff against: git suffices when it tracks the target; otherwise keep a copy.
3. Spawn one `prose:pruner`. Put nothing in the prompt but the file path and the reader with their purpose.

## Review

When the agent finishes, read the diff.

1. Restore only what this session alone knows the reader needs.
2. Settle the agent's close calls where this session can judge; hand the rest to the user.
3. Report briefly what was removed.
