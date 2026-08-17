# AI Engineering Skill Library

A modular library of **17 reusable, operational AI Agent Skills** for designing, building, evaluating, and securing modern LLM-powered systems.

Instead of treating AI engineering as a collection of prompt templates or reference notes, this library turns engineering knowledge into **structured, invokable procedures** that an AI agent can apply to real problems.

You can use **one skill by itself**, a **small group of related skills**, or the **entire library**. You do **not** need all 17 skills installed unless you want broad automatic routing and multi-skill composition.

---

## Quick Start for Beginners

If this is your first time using the library, start here.

### Option A — I only need one capability

Pick the skill that matches your problem and use it by itself **if it has no hard prerequisite**.

Examples:

```text
Need to improve a prompt?
→ prompt-design

Need to manage a long context window?
→ context-engineering

Need to decide workflow vs. agent?
→ agentic-system-design

Need to design a RAG system?
→ rag-architecture-design
```

### Option B — I do not know which skill I need

Use:

```text
SKILL_ROUTER.md
```

Describe the problem in plain language. The router is designed to map symptoms and architectural questions to the most appropriate capability.

### Option C — My task needs several capabilities

Use:

```text
SKILL_DEPENDENCIES.md
```

It shows which skills are true prerequisites and which are only complementary.

### Option D — I want the complete system

Install or expose the full library when you want the AI assistant to:

- choose among many capabilities automatically;
- combine skills when needed;
- move from architecture to implementation to evaluation;
- handle Prompt, Context, RAG, Agents, Evaluation, and Security in one environment.

---

## Do I Need All 17 Skills?

**No.**

The library supports four usage modes:

| Mode | What You Use | Best For |
|---|---|---|
| **Single Skill** | One standalone skill | One focused problem |
| **Skill + Dependencies** | One skill plus its required upstream skills | Capabilities with hard prerequisites |
| **Domain Pack** | A related group such as RAG, Agents, or Security | Specialized projects |
| **Full Library** | All 17 skills | Automatic routing and broad AI engineering workflows |

### Example: standalone use

`context-engineering` can be used independently because it has no hard prerequisite.

```text
User problem
   ↓
context-engineering
   ↓
Context layout + budgets + memory rules + validation
```

### Example: dependent use

`react-agent` should not be treated as an isolated starting point because it has hard prerequisites:

```text
agentic-system-design
        ↓
function-calling-and-tool-design
        ↓
react-agent
```

### Example: RAG chain

A complete RAG lifecycle may use:

```text
rag-architecture-design
        ↓
rag-retrieval-and-grounding
        ↓
rag-evaluation
```

You can stop after the first skill if all you need is the architecture. Use the later skills only when retrieval implementation or evaluation is required.

---

## Where Can These Skills Be Used?

The canonical skills are designed to be as platform-independent as practical.

### Claude.ai

Use the packaged ZIP files under:

```text
dist/claude-ai/
```

Each ZIP contains one upload-ready skill.

You may upload only the skills you need, or upload a larger set when you want Claude to choose among them.

### Claude Code

Use the canonical skill directories under:

```text
skills/
```

The canonical versions contain the full operational instructions and reference material.

### Custom AI Agents

A skill can be adapted as a reusable capability definition inside a custom agent system.

Typical pattern:

```text
User Task
   ↓
Capability Selection
   ↓
Selected SKILL.md
   ↓
Procedure Execution
   ↓
Validation
   ↓
Structured Output
```

### Agent Frameworks and Internal AI Systems

The skills can also be adapted into:

- agent routers;
- orchestration layers;
- RAG pipelines;
- evaluation systems;
- internal copilots;
- workflow automation;
- tool-using assistants;
- security and validation layers.

Platform-specific integration may require an adapter, but the underlying skill logic should remain reusable.

---

## How to Ask the AI to Use the Library

You do not need to know the skill name in advance.

A simple request can be:

```text
Select and apply the most appropriate capability from the installed AI Engineering Skills based on the problem below.

If multiple capabilities are required, use them in the documented dependency order.

Return an actionable, structured, and validated result.

Problem:
[describe your problem here]
```

Example:

```text
My AI assistant has 15 tools, RAG documents, user memory, and long conversation history.
As the conversation grows, it starts forgetting early constraints.
Design a reliable way to organize the context and define what should be kept, summarized, or discarded.
```

The user does not need to write `context-engineering`; the capability description and router are intended to support natural-language selection.

---

## What Should a Skill Produce?

A skill should not merely explain a concept. It should produce a usable engineering artifact.

Depending on the skill, the output may be:

- a redesigned prompt;
- an architecture decision;
- a context layout;
- a workflow;
- a RAG design;
- tool contracts;
- an agent loop;
- an evaluation plan;
- a security policy;
- validation criteria;
- a failure diagnosis and repair plan.

Every skill is intended to produce output that is:

```text
Actionable
Structured
Verifiable
Ready for handoff
```

---

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

This makes the skills suitable for AI assistants and agentic systems that need to select a capability, execute it consistently, validate the result, and hand the output to another skill or implementation layer.

---

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

---

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

> **Hard prerequisites** reflect explicit dependency requirements. Skills may also have complementary relationships that are useful in real systems but are not mandatory prerequisites. See `SKILL_DEPENDENCIES.md` for the complete relationship map.

---

## Beginner Decision Guide

If you are unsure where to start, use this simplified map:

```text
What is the main problem?
│
├─ The prompt itself is unclear or inconsistent
│  → prompt-design
│
├─ Instructions alone are not enough; examples would help
│  → few-shot-prompting
│
├─ Long context, history, tools, or memory are competing
│  → context-engineering
│
├─ The task needs difficult multi-step reasoning
│  → reasoning-and-deliberation
│
├─ One prompt is doing too many fixed stages
│  → prompt-chaining-and-workflows
│
├─ JSON / extraction / structured output keeps breaking
│  → structured-output-and-extraction
│
├─ Private or changing knowledge is needed
│  → rag-architecture-design
│
├─ Existing RAG retrieves poor evidence
│  → rag-retrieval-and-grounding
│
├─ Need to measure RAG quality
│  → rag-evaluation
│
├─ Need to decide workflow vs. autonomous agent
│  → agentic-system-design
│
├─ Agent calls the wrong tool or sends bad arguments
│  → function-calling-and-tool-design
│
├─ Agent loops or fails to adapt after tool results
│  → react-agent
│
├─ Need to compare prompts objectively
│  → prompt-evaluation-and-optimization
│
├─ Model makes unsupported factual claims
│  → factuality-and-hallucination-control
│
├─ External documents or tool results may contain malicious instructions
│  → prompt-injection-defense
│
└─ Users try to bypass system rules directly
   → jailbreak-resistance
```

For ambiguous cases, use `SKILL_ROUTER.md` instead of guessing.

---

## How the Library Is Used Internally

### 1. Route the problem

If the correct capability is not obvious:

```text
SKILL_ROUTER.md
```

### 2. Check dependencies

Before composing multiple capabilities:

```text
SKILL_DEPENDENCIES.md
```

### 3. Execute the selected skill

Each `SKILL.md` defines:

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

---

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

---

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

---

## Download and Build

### Clone the repository

```bash
git clone https://github.com/KwSalem/ai-engineering-skills.git
cd ai-engineering-skills
```

For a private repository, GitHub authentication is required.

### Build Claude.ai packages

Canonical source files live under `skills/`. Upload-ready Claude.ai packages are generated under:

```text
dist/claude-ai/
```

#### macOS / Linux

```bash
python3 scripts/build_claude_ai_dist.py
```

#### Windows

```bash
py scripts/build_claude_ai_dist.py
```

A successful build creates 17 ZIP files under `dist/claude-ai/`.

The build process replaces canonical long-form descriptions with Claude.ai-compatible short descriptions and verifies the configured description-length limit before packaging.

---

## Recommended Beginner Paths

### I want better prompting

```text
prompt-design
   ↓ if instructions are still insufficient
few-shot-prompting
   ↓ if objective comparison is needed
prompt-evaluation-and-optimization
```

### I want to build RAG

```text
rag-architecture-design
        ↓
rag-retrieval-and-grounding
        ↓
rag-evaluation
```

Add `prompt-injection-defense` when the system consumes untrusted or user-controlled documents.

### I want to build an agent

```text
agentic-system-design
        ↓
function-calling-and-tool-design
        ↓
react-agent
```

Then add relevant Context, Security, and Evaluation capabilities as required by the system.

### I want to secure an AI system

```text
External content risk
→ prompt-injection-defense

Direct user bypass attempts
→ jailbreak-resistance

Unsupported factual claims
→ factuality-and-hallucination-control
```

These may be used together because they address different failure sources.

---

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

---

## Provenance and Attribution

The first generation of this library was informed in part by practical material from the open-source **DAIR.AI Prompt Engineering Guide**.

The source material was not treated as a finished skill system. This project adds its own operational structure, capability boundaries, decision procedures, routing logic, dependency model, validation methods, packaging workflow, and project-specific engineering recommendations.

Within each skill, `references/sources.md` distinguishes between:

- **Source-derived** material — traced to the relevant source location; and
- **Architect recommendation** — project-specific additions that are not attributed to the original source.

Third-party copyrights and license terms remain with their respective owners. See `THIRD_PARTY_NOTICES.md` for the applicable notices, including the MIT License notice associated with DAIR.AI-derived material.

---

## Licensing

Original project contributions are governed by the proprietary terms in `LICENSE.md`.

Third-party and open-source material retains the rights and obligations of its original license. Nothing in the project's proprietary license is intended to override rights granted by an applicable third-party open-source license.

For commercial licensing or permissions beyond the terms provided with authorized access, contact the copyright holder identified in `LICENSE.md`.

---

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
