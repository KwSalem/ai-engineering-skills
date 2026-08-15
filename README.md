# AI Engineering Skill Library

A modular library of 17 reusable AI Agent Skills, converted from the practical
knowledge in [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
into operational, invokable procedures rather than reference notes.

Each skill answers one question: *when an agent hits problem X, can it invoke
this skill and follow a reliable procedure to solve it?* See `CONVENTIONS.md`
for the writing standard every skill follows, `SKILL_ROUTER.md` for how to
pick the right skill for a problem, and `SKILL_DEPENDENCIES.md` for how
skills compose.

## Status

All 17 skills are built, internally consistent, and live-tested on claude.ai
across every group. Every skill's `references/sources.md` traces each claim
to either the source repository or marks it explicitly as an architect
recommendation not present in the source material.

## Index

| Skill | Purpose | Trigger | Complexity | Prerequisites |
|---|---|---|---|---|
| `prompt-design` | Fix a single prompt's wording using the six prompt elements | Inconsistent/off-target output, ignored instructions | Foundational | None |
| `few-shot-prompting` | Teach a task by demonstration: select, format, order examples | Instructions alone don't stabilize format/style | Foundational | `prompt-design` |
| `context-engineering` | Budget and order everything entering the context window | Building/debugging an agent, quality decays with session length | Intermediate | `prompt-design` |
| `reasoning-and-deliberation` | Match deliberation technique to task difficulty | Wrong multi-step/arithmetic answers, unstable results | Intermediate | `prompt-design` |
| `prompt-chaining-and-workflows` | Split an overloaded task into sequential, validated prompt stages | One prompt doing too much, need to isolate a failing stage | Intermediate | `prompt-design` |
| `structured-output-and-extraction` | Reliable extraction, classification, QA, summarization formats | Inconsistent structured output across runs | Foundational | `prompt-design` |
| `synthetic-data-generation` | Generate diverse synthetic training/eval data via variable slots | Real data scarce, sensitive, or generated data is repetitive | Intermediate | `prompt-chaining-and-workflows` |
| `rag-architecture-design` | Decide if RAG is needed, then design the indexing pipeline | Private/changing knowledge needed, existing RAG retrieves poorly | Intermediate | `context-engineering` |
| `rag-retrieval-and-grounding` | Query-time retrieval and citation-grounded generation | Retrieved chunks wrong, or answers drift from sources | Advanced | `rag-architecture-design` |
| `rag-evaluation` | Measure RAG retrieval and generation quality separately | Need a RAG quality baseline or a before/after comparison | Intermediate | `rag-architecture-design`, `rag-retrieval-and-grounding` |
| `agentic-system-design` | Choose workflow vs. agent; design planning, memory, control | Building a multi-step assistant, existing agent misbehaves | Advanced | `context-engineering` |
| `function-calling-and-tool-design` | Define and debug an agent's tools and their selection | Wrong tool called, bad arguments, tool definitions bloated | Intermediate | `agentic-system-design` |
| `react-agent` | Design the Thought/Action/Observation loop, plus self-reflection | Agent loops, fails to adapt, or needs iterative reasoning+action | Advanced | `agentic-system-design`, `function-calling-and-tool-design` |
| `prompt-evaluation-and-optimization` | Prove a prompt works and compare variants with real test sets | Need to justify a prompt change or pick between variants | Intermediate | `prompt-design` |
| `factuality-and-hallucination-control` | Reduce confident fabrication, calibrate abstention | Model states wrong facts confidently, never admits uncertainty | Intermediate | `prompt-design` |
| `prompt-injection-defense` | Layered defense against untrusted content overriding instructions | System reads documents, tool results, or other external content | Advanced | `context-engineering` |
| `jailbreak-resistance` | Resist user attempts to bypass guidelines via reframing | User tries roleplay/hypothetical/persona framing to bypass rules | Intermediate | `prompt-design` |

## Groups

**Foundation** — `prompt-design`, `few-shot-prompting`, `context-engineering`, `reasoning-and-deliberation`
The root layer. Every other group assumes a competently built prompt and a managed context window underneath it.

**Workflows** — `prompt-chaining-and-workflows`, `structured-output-and-extraction`, `synthetic-data-generation`
Structuring multi-step and structured-output tasks without requiring an autonomous agent.

**RAG** — `rag-architecture-design`, `rag-retrieval-and-grounding`, `rag-evaluation`
Grounding a system in private or changing knowledge: indexing, query-time retrieval, and measurement.

**Agents** — `agentic-system-design`, `function-calling-and-tool-design`, `react-agent`
Autonomous, tool-using systems: the architecture decision, the tools themselves, and the reasoning loop that calls them.

**Evaluation** — `prompt-evaluation-and-optimization`, `factuality-and-hallucination-control`
Proving a change helped, and keeping output grounded in fact rather than confident fabrication.

**Security** — `prompt-injection-defense`, `jailbreak-resistance`
Defending against untrusted external content and against direct user attempts to bypass guidelines. Both are referenced as the closing layer by nearly every skill that touches external content or user-facing deployment.

## How to use this library

1. Not sure which skill fits? Start at `SKILL_ROUTER.md`.
2. Building something that needs several skills together? Check `SKILL_DEPENDENCIES.md` for the composed chains.
3. Writing a new skill for this library? Follow `CONVENTIONS.md` exactly, including the mandatory `references/sources.md` traceability table.

## Provenance

Every skill's `references/sources.md` separates claims into two types:

- **Source-derived**: traceable to a specific file in the DAIR.AI repository, cited by path.
- **Architect recommendation**: this library's own addition, not present in the source material, labelled explicitly rather than attributed to DAIR.AI.

This distinction is load-bearing, not decorative: it lets anyone auditing this library verify exactly which procedural claims come from the source guide and which are original design decisions layered on top of it.

## Licensing

Original contributions in this repository are distributed under the proprietary terms in `LICENSE.md`.
Third-party and open-source materials retain their original license rights and attribution requirements; see `THIRD_PARTY_NOTICES.md`, including the MIT License notice for DAIR.AI-derived material.

## Repository layout

```
skills/                  Canonical source, long-form descriptions (Claude Code / API)
dist/claude-ai/          Generated upload zips, short descriptions (claude.ai limit)
scripts/                 Packaging script + the short-description registry it reads
LICENSE.md               Proprietary license for this repository's original contributions
THIRD_PARTY_NOTICES.md   Attribution and license notices for third-party/open-source material
CONVENTIONS.md           Writing standard every skill in this library follows
SKILL_ROUTER.md          How to pick the right skill for a problem
SKILL_DEPENDENCIES.md    How skills depend on and complement each other
```

To regenerate `dist/claude-ai/` after editing anything under `skills/`:

```bash
python3 scripts/build_claude_ai_dist.py
```
