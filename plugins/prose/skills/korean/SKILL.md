---
name: korean
description: Rewrite the Korean in a work product until it reads as though written in Korean from the start.
argument-hint: "[target to rewrite (optional)]"
disable-model-invocation: true
---

# Korean

Never rewrite in this session — dispatch to the `prose:rewriter`
agent. The fresh context is the mechanism: the eye that wrote a
sentence finds it natural, and in a long session any doctrine loaded
here dilutes. Both are solved only outside this session.

## Dispatch

1. Resolve the target to a file list: the argument, or absent one, this
   session's Korean work products.
2. Before dispatching, secure the original to diff against: git
   suffices when it tracks the target; otherwise keep a copy.
3. Spawn one `prose:rewriter` agent for the whole list, not one per
   file — one set of eyes keeps terms consistent across files.
4. Write the prompt in Korean, and put nothing in it but the file paths.

## Review

When the agent finishes, diff each file and judge only what this
session can judge.

- Meaning, identifiers, and the project's own terms — this session
  knows the intent; restore them where the rewrite broke them.
- Readings the agent's report left unresolved are this session's to
  settle: pick the intended one and apply it.
- A term coined by direct translation goes back to the established
  form; a term is a word-level fix, so it is in bounds.
- Keep the fixes local: put words back, do not rewrite sentences. The
  prose's naturalness is the agent's verdict — do not re-litigate it.
