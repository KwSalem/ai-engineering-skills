# Skill Dependencies

How the 17 skills relate. Every edge in this file is transcribed directly
from a skill's own `Related:` line in its `References` section, or from an
explicit prerequisite statement in its `Purpose`/`When to Use` (phrases like
"assumes X" or "go to X first"). Nothing here is inferred or added on
intuition; if a relationship isn't written in the skill itself, it isn't in
this file.

This file was rebuilt from a direct audit that found the previous version
contained several inferred relationships not actually present in the
skills' own text, alongside real ones that were missing. See the note at
the bottom for what changed and why that matters going forward.

Two relationship types:

- **Hard dependency** (`↓`): the skill's own text explicitly states it
  assumes the upstream skill's decision is already made, or explicitly
  says to go there first.
- **Complementary** (`+`): listed in the skill's own `Related:` line, but
  not stated as a prerequisite. Real systems often need both; neither
  requires the other to function on its own.

---

## Explicit hard dependencies (verified against each skill's own text)

| Skill | Assumes / requires first | Where it's stated |
|---|---|---|
| `few-shot-prompting` | `prompt-design` | When to Use: "This is the handoff point from `prompt-design`." |
| `structured-output-and-extraction` | `prompt-design` | When NOT to Use: "this skill assumes a working prompt" |
| `rag-retrieval-and-grounding` | `rag-architecture-design` | When to Use: "a RAG index already exists" |
| `rag-evaluation` | `rag-architecture-design`, `rag-retrieval-and-grounding` | When NOT to Use: "Go to `rag-architecture-design` first"; Related: "for what this skill measures" |
| `function-calling-and-tool-design` | `agentic-system-design` | Purpose: "assumes the architecture... is already decided by `agentic-system-design`" |
| `react-agent` | `agentic-system-design`, `function-calling-and-tool-design` | Purpose: "assumes `agentic-system-design` has already decided... and that `function-calling-and-tool-design` has already defined the tools" |

Every other skill's own text stops short of an explicit "assumes" or "go
there first" statement, even where a logical order clearly exists (a
system generally needs a working prompt before it needs a context budget,
for instance). Rather than infer a hard dependency the skill itself
doesn't declare, those relationships are listed as complementary below.
`prompt-design`, `context-engineering`, `reasoning-and-deliberation`,
`prompt-chaining-and-workflows`, `synthetic-data-generation`,
`rag-architecture-design`, `agentic-system-design`,
`prompt-evaluation-and-optimization`, `factuality-and-hallucination-control`,
`prompt-injection-defense`, and `jailbreak-resistance` have no upstream
hard dependency stated in their own text.

---

## Complementary relationships (transcribed from each skill's `Related:` line)

| Skill | Related (verbatim skill names from its own References section) |
|---|---|
| `prompt-design` | `few-shot-prompting`, `reasoning-and-deliberation`, `rag-architecture-design`, `context-engineering`, `structured-output-and-extraction`, `prompt-chaining-and-workflows`, `prompt-evaluation-and-optimization`, `factuality-and-hallucination-control`, `function-calling-and-tool-design`, `prompt-injection-defense` |
| `few-shot-prompting` | `prompt-design`, `structured-output-and-extraction`, `prompt-evaluation-and-optimization` |
| `context-engineering` | `prompt-design`, `prompt-injection-defense`, `rag-retrieval-and-grounding` |
| `reasoning-and-deliberation` | `prompt-design`, `rag-architecture-design`, `structured-output-and-extraction`, `prompt-chaining-and-workflows`, `function-calling-and-tool-design` |
| `prompt-chaining-and-workflows` | `prompt-design`, `agentic-system-design`, `structured-output-and-extraction` |
| `structured-output-and-extraction` | `prompt-design`, `few-shot-prompting`, `factuality-and-hallucination-control`, `prompt-chaining-and-workflows` |
| `synthetic-data-generation` | `prompt-chaining-and-workflows`, `few-shot-prompting`, `rag-architecture-design`, `prompt-evaluation-and-optimization`, `rag-evaluation` |
| `rag-architecture-design` | `context-engineering`, `rag-retrieval-and-grounding`, `rag-evaluation` |
| `rag-retrieval-and-grounding` | `rag-architecture-design`, `context-engineering`, `prompt-injection-defense`, `rag-evaluation` |
| `rag-evaluation` | `rag-architecture-design`, `rag-retrieval-and-grounding`, `factuality-and-hallucination-control` |
| `agentic-system-design` | `function-calling-and-tool-design`, `react-agent`, `rag-architecture-design`, `context-engineering`, `prompt-injection-defense`, `jailbreak-resistance` |
| `function-calling-and-tool-design` | `agentic-system-design`, `react-agent`, `context-engineering`, `prompt-injection-defense` |
| `react-agent` | `agentic-system-design`, `function-calling-and-tool-design`, `reasoning-and-deliberation`, `context-engineering` |
| `prompt-evaluation-and-optimization` | `prompt-design`, `few-shot-prompting`, `rag-evaluation`, `factuality-and-hallucination-control` |
| `factuality-and-hallucination-control` | `rag-retrieval-and-grounding`, `rag-evaluation`, `prompt-design`, `prompt-evaluation-and-optimization` |
| `prompt-injection-defense` | `jailbreak-resistance`, `context-engineering`, `factuality-and-hallucination-control` |
| `jailbreak-resistance` | `prompt-injection-defense`, `factuality-and-hallucination-control` |

Note some asymmetries are real and intentional, not errors: `context-engineering`
lists `rag-retrieval-and-grounding` as related, but `rag-retrieval-and-grounding`
also separately lists `context-engineering` back, so that pair is symmetric.
Others are one-directional as written: `agentic-system-design` lists
`react-agent`, and `react-agent` lists `agentic-system-design` back (symmetric),
but plenty of pairs below are one-directional exactly as each skill's own
author-written text states it, without being forced into artificial symmetry.

---

## Full dependency graph

```
prompt-design                              ← root; no upstream skill required
  │ hard-required by: few-shot-prompting, structured-output-and-extraction
  │
  └─↓ (used by, per explicit assumes-language)
        few-shot-prompting
        structured-output-and-extraction

context-engineering                        ← second root; no upstream skill required
reasoning-and-deliberation                 ← no upstream skill required
prompt-chaining-and-workflows              ← no upstream skill required
synthetic-data-generation                  ← no upstream skill required
rag-architecture-design                    ← root of RAG group; no upstream skill required
  │
  └─↓ rag-retrieval-and-grounding          (explicit: "an index already exists")
        │
        └─↓ rag-evaluation                 (explicit: "go to rag-architecture-design first";
                                              also requires rag-retrieval-and-grounding)

agentic-system-design                      ← root of Agents group; no upstream skill required
  │
  ├─↓ function-calling-and-tool-design     (explicit: "assumes... decided by agentic-system-design")
  │     │
  │     └─↓ react-agent                    (explicit: "assumes agentic-system-design... and that
  │                                           function-calling-and-tool-design has already defined
  │                                           the tools")
  │
  └── (react-agent's second hard dependency, shown above)

prompt-evaluation-and-optimization         ← no upstream skill required (evaluates prompt-design's
                                              output, but this is not stated as a hard dependency)
factuality-and-hallucination-control       ← no upstream skill required
prompt-injection-defense                   ← no upstream skill required
jailbreak-resistance                       ← no upstream skill required
```

Every complementary relationship from the table above still applies across
this graph; the graph shows only the six explicit hard dependencies so the
genuinely required order is visible without the complementary edges
crowding it.

---

## Why most skills have no listed hard dependency

Only six edges in this library are hard dependencies, and that's
deliberate, not an oversight: most skills are useful on their own, and
overstating a prerequisite (as the previous version of this file did in
several places) makes the library harder to use correctly, not easier. A
skill lists a hard dependency only when using it without the upstream
decision already made would produce an unreliable result, which is a
narrower bar than "these two skills often appear in the same system."

## Why the two roots

`prompt-design` and `context-engineering` are both roots rather than one
depending on the other, because they operate at different scopes:
`prompt-design` governs the content of any single prompt or segment,
`context-engineering` governs how many segments coexist in one window and
in what order. A single-turn prompt needs no context budget beyond itself,
which is why they aren't chained.

## Why security skills sit outside the main tree

`prompt-injection-defense` and `jailbreak-resistance` have no hard
dependency in either direction and are listed as complementary to several
skills rather than nested under one branch, because the risk they address
can appear at nearly any point in a system. The router's Layer 1 gate and
each affected skill's own `When NOT to Use` section enforce the pairing
independently of this file.

## What changed in this rebuild, and why it matters

An audit compared the previous version of this file line by line against
every skill's actual `Related:` line and prerequisite language, and found
two categories of error: relationships stated here that don't appear in
the skill's own text at all (for example, `react-agent` was shown as
complementary to `rag-retrieval-and-grounding`, which `react-agent` never
mentions), and real relationships the skill does state that were missing
from this file (for example, `rag-evaluation` explicitly appears in
`synthetic-data-generation`'s own Related line but was absent here). The
audit also found that `prompt-design` and `reasoning-and-deliberation`,
the two earliest-authored skills in this library, had never been given a
`Related:` line at all despite extensively cross-referencing other skills
in their body text; both have been given one now, transcribed from their
actual body mentions.

This file is now rebuilt to contain nothing that isn't directly verifiable
by opening the named skill and finding the same relationship in its own
text. If this file and a skill's own content ever disagree again, the
skill's own text is correct and this file is what needs fixing.

## A separate, more common failure mode: source vs. installed copies

This file describes the library's source content (the `lib/` directory and
the full archive built from it). It says nothing about which version is
actually installed on any given account. Across this project, the most
frequent real-world discrepancy has not been an error in the source, but
an installed skill lagging behind a fix already made to the source, most
often when several skills are updated in the same round and only some are
actually re-uploaded. Before trusting a claim in this file about a
specific skill's current wording, confirm that skill was actually
reinstalled after its last source change, not just that the source itself
is correct.
