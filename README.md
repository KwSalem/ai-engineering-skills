# AI Engineering Skill Library

A modular library of **17 reusable, operational AI Agent Skills** for designing, building, evaluating, and securing modern LLM-powered systems.

Instead of treating AI engineering as a collection of prompt templates or reference notes, this library turns engineering knowledge into **structured, invokable procedures** that an AI agent can apply to real problems.

Each skill is designed to answer four practical questions:

1. **When should this capability be used?**
2. **What inputs are required before execution?**
3. **What procedure and decision rules should be followed?**
4. **How is the result validated, and when should the skill stop or escalate?**

The current library covers Prompt Engineering, Context Engineering, Workflows, RAG, Agent Design, Evaluation, and AI Security.

## Why This Library

Most AI engineering material explains concepts. This project focuses on **operational behavior**.

A typical skill provides:

```text
Trigger / Problem
      ↓
Required Inputs
      ↓
Decision Tree
      ↓
Procedure
      ↓
Decision Rules
      ↓
Validation
      ↓
Failure Conditions
      ↓
Output Contract
      ↓
Evaluation Criteria
```

This makes the skills suitable for use by AI assistants and agentic systems that need to select a capability, execute it consistently, validate the result, and hand the output to another skill or implementation layer.

## Current Scope

The repository currently contains **17 skills across 6 domains**.

### Foundation

- `prompt-design`
- `few-shot-prompting`
- `context-engineering`
- `reasoning-and-deliberation`

### Workflows

- `prompt-chaining-and-workflows`
- `structured-output-and-extraction`
- `synthetic-data-generation`

### RAG

- `rag-architecture-design`
- `rag-retrieval-and-grounding`
- `rag-evaluation`

### Agents

- `agentic-system-design`
- `function-calling-and-tool-design`
- `react-agent`

### Evaluation

- `prompt-evaluation-and-optimization`
- `factuality-and-hallucination-control`

### Security

- `prompt-injection-defense`
- `jailbreak-resistance`

## Skill Index

| Skill | Primary Capability | Typical Trigger | Hard Prerequisites |
|---|---|---|---|
| `prompt-design` | Design or repair a single prompt | Off-target output, ignored instructions, unstable format | None |
| `few-shot-prompting` | Stabilize behavior through demonstrations | Instructions alone do not reliably teach the task | `prompt-design` |
| `context-engineering` | Design and manage the complete context window | Long sessions degrade, constraints are forgotten, context competes for space | None |
| `reasoning-and-deliberation` | Match reasoning strategy to task difficulty | Multi-step, arithmetic, or reasoning-heavy failures | None |
| `prompt-chaining-and-workflows` | Decompose fixed multi-stage tasks | One prompt is doing too much | None |
| `structured-output-and-extraction` | Produce reliable structured outputs | JSON, extraction, classification, or output shape is unstable | `prompt-design` |
| `synthetic-data-generation` | Design diverse synthetic datasets | Real data is scarce, sensitive, or insufficiently diverse | None |
| `rag-architecture-design` | Design the RAG indexing architecture | Private, large, or changing knowledge is required | None |
| `rag-retrieval-and-grounding` | Improve query-time retrieval and grounding | Retrieved chunks are weak or answers drift from evidence | `rag-architecture-design` |
| `rag-evaluation` | Measure retrieval and generation quality separately | Need a RAG baseline or before/after comparison | `rag-architecture-design`, `rag-retrieval-and-grounding` |
| `agentic-system-design` | Decide workflow vs. agent and design control structure | Steps depend on runtime discoveries or autonomous tool use is being considered | None |
| `function-calling-and-tool-design` | Design and debug tool interfaces | Wrong tool, poor arguments, ambiguous tool definitions | `agentic-system-design` |
| `react-agent` | Design an adaptive reasoning-and-action loop | Agent repeats failed actions or must adapt after tool observations | `agentic-system-design`, `function-calling-and-tool-design` |
| `prompt-evaluation-and-optimization` | Compare prompts using repeatable tests | Need evidence that a prompt change improved performance | None |
| `factuality-and-hallucination-control` | Reduce unsupported factual claims | Confident fabrication or poor uncertainty calibration | None |
| `prompt-injection-defense` | Protect systems from untrusted instructions in external content | Documents, webpages, tool outputs, or user-controlled content enter context | None |
| `jailbreak-resistance` | Resist direct attempts to bypass system rules | Roleplay, reframing, or instruction-override attempts | None |

> **Hard prerequisites** above reflect explicit dependency requirements. Skills may also have complementary relationships that are useful in real systems but are not mandatory prerequisites. See `SKILL_DEPENDENCIES.md` for the complete relationship map.

## How the Library Is Used

### 1. Route the problem

If the correct capability is not obvious, start with:

```text
SKILL_ROUTER.md
```

The router maps architectural questions and real-world symptoms to the most appropriate skill or skill chain.

### 2. Compose capabilities when needed

For systems that require multiple skills, use:

```text
SKILL_DEPENDENCIES.md
```

It distinguishes **hard dependencies** from **complementary relationships** so skills can be composed without inventing unnecessary prerequisites.

### 3. Execute the selected skill

Each `SKILL.md` defines its own:

- purpose and trigger;
- required and optional inputs;
- decision tree;
- execution procedure;
- decision rules;
- validation criteria;
- failure conditions;
- anti-patterns;
- output format;
- evaluation criteria.

### 4. Validate before handoff

A skill should produce an output that is **actionable, structured, verifiable, and ready to hand off** to another skill or implementation layer.

## Design Principles

### Operational over theoretical

Skills tell an agent what to do and how to verify it. Background material belongs in `references/` and is loaded only when needed.

### Composable

Skills are designed to work independently where possible and compose cleanly where a real dependency exists.

### Traceable

Each skill includes `references/sources.md` so source-derived material can be distinguished from project-specific engineering recommendations.

### Model-aware, not model-locked

Canonical skill logic is kept as platform-independent as practical. Platform-specific packaging belongs under `dist/` rather than inside the source skills.

### Validation-first

A skill is incomplete if it only gives advice. It must define how success is checked and when execution should stop, fail, or escalate.

## Repository Structure

```text
ai-engineering-skills/
│
├── skills/                  Canonical skill source
│   ├── foundation/
│   ├── workflows/
│   ├── rag/
│   ├── agents/
│   ├── evaluation/
│   └── security/
│
├── dist/
│   └── claude-ai/           Generated Claude.ai upload packages
│
├── scripts/                 Build and packaging utilities
│
├── CONVENTIONS.md           Skill authoring and quality standard
├── SKILL_ROUTER.md          Capability selection and routing rules
├── SKILL_DEPENDENCIES.md    Hard dependencies and complementary relationships
├── LICENSE.md               Proprietary terms for original project contributions
└── THIRD_PARTY_NOTICES.md   Third-party attribution and license notices
```

## Skill Authoring Standard

`CONVENTIONS.md` defines the contract used across the library.

Canonical skills use frontmatter for discovery and follow a consistent operational structure. New skills should represent a **distinct capability**, not merely a topic, example collection, or renamed version of an existing skill.

A new skill should have:

- a distinct trigger;
- distinct required inputs;
- a distinct procedure;
- checkable validation;
- explicit failure conditions;
- minimal overlap with existing skills.

If a concept only adds background, examples, or implementation patterns to an existing capability, it normally belongs under that skill's `references/` directory instead of becoming a new skill.

## Claude.ai Distribution

Canonical source files live under `skills/`. Upload-ready Claude.ai packages are generated under:

```text
dist/claude-ai/
```

To rebuild all 17 packages after editing the canonical skills:

### macOS / Linux

```bash
python3 scripts/build_claude_ai_dist.py
```

### Windows

```bash
py scripts/build_claude_ai_dist.py
```

The build process replaces canonical long-form descriptions with Claude.ai-compatible short descriptions and verifies the configured description-length limit before packaging.

## Provenance and Attribution

The first generation of this library was informed in part by practical material from the open-source **DAIR.AI Prompt Engineering Guide**.

The source material was not treated as a finished skill system. This project adds its own operational structure, capability boundaries, decision procedures, routing logic, dependency model, validation methods, packaging workflow, and project-specific engineering recommendations.

Within each skill, `references/sources.md` distinguishes between:

- **Source-derived** material — traced to the relevant source location; and
- **Architect recommendation** — project-specific additions that are not attributed to the original source.

Third-party copyrights and license terms remain with their respective owners. See `THIRD_PARTY_NOTICES.md` for the applicable notices, including the MIT License notice associated with DAIR.AI-derived material.

## Licensing

Original project contributions are governed by the proprietary terms in `LICENSE.md`.

Third-party and open-source material retains the rights and obligations of its original license. Nothing in the project's proprietary license is intended to override rights granted by an applicable third-party open-source license.

For commercial licensing or permissions beyond the terms provided with authorized access, contact the copyright holder identified in `LICENSE.md`.

## Project Direction

The goal is not to create the largest possible collection of AI skills. The goal is to build a **coherent, auditable, composable AI Engineering Skill System**.

Future expansion is expected to focus on genuine capability gaps such as:

```text
Prompt Engineering
        ↓
Context Engineering
        ↓
Workflow Engineering
        ↓
RAG Engineering
        ↓
Agent Engineering
        ↓
Harness Engineering
        ↓
Memory Engineering
        ↓
Evaluation
        ↓
Security
        ↓
Observability & Reliability
```

New domains or skills should be added only when they introduce a clearly distinct operational capability and can satisfy the same validation and traceability standards as the existing library.
