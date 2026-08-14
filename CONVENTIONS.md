# Library Conventions

Standards every skill in this library follows. Read this before authoring or editing a skill.

## Frontmatter

Only two fields, both required:

```yaml
---
name: skill-name
description: >
  [what it does] [what it covers] [3 concrete triggers] [1 implicit trigger]
---
```

- `name` matches the directory name exactly. Lowercase, hyphenated, names a capability rather than a topic.
- `description` is the only text always resident in context. It is the trigger mechanism, so it states both WHAT and WHEN, and closes with an implicit trigger that catches casual phrasing where the user never says the technical term.
- Banned description shapes: "Helps with prompts", "Best practices for X", anything without a verb.

## Body structure

Every SKILL.md uses these headings in this order. Omit a heading only when it genuinely does not apply.

```
# Title
## Purpose
## When to Use
## When NOT to Use
## Required Inputs
## Optional Inputs
## Decision Tree
## Procedure
## Decision Rules
## Validation
## Failure Conditions
## Anti-Patterns
## Output Format
## Evaluation Criteria
## References
```

## Writing rules

1. Imperative voice. "Rewrite the query into three variants", not "the agent should consider rewriting".
2. Every procedure step pairs a condition with an action. No step says "use your judgement".
3. No theory in SKILL.md. Definitions and background move to `references/concepts.md`.
4. Under 500 lines. Past that, add a reference layer with an explicit pointer.
5. State why a rule matters when the reason is not obvious. A model that understands the reason generalizes to cases the skill did not list.

## Files

```
skill-name/
├── SKILL.md          required
├── references/       loaded on demand, never preloaded
│   ├── concepts.md   background and definitions
│   ├── patterns.md   named patterns and variants
│   ├── examples.md   simple / realistic / edge case
│   └── sources.md    traceability table, required in every skill
├── assets/           templates that appear in output
└── scripts/          only for deterministic execution
```

Reference files over 300 lines open with a table of contents.

## No duplication

Each fact lives in exactly one file. Other skills point to it:
`See prompt-design/references/elements.md`.

## Traceability

`references/sources.md` is required and uses this table:

| Claim | Source | Type |
|---|---|---|
| ... | `pages/...` | Source-derived |
| ... | none | Architect recommendation |

Anything not traceable to the DAIR.AI repository is labelled an architect recommendation. Never attribute an unsourced claim to DAIR.AI.

## Quality gate

A skill ships only after passing all seven:

1. One clear trigger that does not compete with another skill.
2. Executable without opening the source repository.
3. Every step has a condition and an action.
4. Validation is checkable against a stated criterion.
5. Failure conditions say when to stop and when to ask.
6. At least three real anti-patterns.
7. Every claim in `sources.md` is attributed or labelled.
