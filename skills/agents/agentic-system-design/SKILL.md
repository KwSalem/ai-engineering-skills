---
name: agentic-system-design
description: >
  Decides whether a task needs a workflow (predefined code paths) or an agent
  (dynamic, self-directed tool use), and designs the resulting system's planning,
  memory, and control structure, including when to decompose into an orchestrator
  with sub-agents. Use when building an assistant that must take multiple steps or
  call tools, when deciding between a fixed pipeline and an autonomous loop, when
  an existing agent behaves unpredictably or a workflow feels too rigid, or when
  scoping a multi-agent system. Use it even when the user just says "make this
  automatic" or "have it figure out the steps itself" without using the word agent.
---

# Agentic System Design

## Purpose

Decide whether a task calls for a workflow or an agent, then design the control structure: how the system plans, what it remembers, and whether one execution loop is enough or the work should be split across an orchestrator and sub-agents. This is the architectural layer above individual tool calls; it decides the shape of the system before `function-calling-and-tool-design` and `react-agent` fill in how any single loop actually calls tools and reasons.

## When to Use

- Building any assistant that must take more than one step, call external tools, or adapt its approach based on intermediate results.
- Deciding between a fixed, code-orchestrated pipeline and an LLM-directed autonomous loop.
- An existing agent is unpredictable, expensive, or hard to debug, and the fix might be structural (it should have been a workflow) rather than a prompting fix.
- A workflow feels too rigid for a task whose steps can't be fully enumerated in advance.
- Scoping whether a task needs a single agent or an orchestrator coordinating multiple sub-agents.

## When NOT to Use

- The task is a single prompt with no tool use and no multi-step decision-making. Go to `prompt-design`.
- The architecture (workflow vs. agent, single vs. multi-agent) is already decided and the question is how to define or debug specific tools. Go to `function-calling-and-tool-design`.
- The architecture is decided as a single reasoning-and-acting loop and the question is how that loop should interleave thought and action. Go to `react-agent`.
- The system needs private knowledge, not autonomous action. Go to `rag-architecture-design`; an agent that only retrieves and answers doesn't need autonomy, it needs grounding.
- The gap is context management within an already-decided architecture (budget, memory, history). Go to `context-engineering`.

## Required Inputs

- What the task needs to accomplish, end to end.
- Whether the steps required can be enumerated in advance or only discovered during execution.
- Tolerance for unpredictability: is this a production path needing reliability, or an exploratory task where flexibility matters more.

## Optional Inputs

- Existing workflow or agent behavior that's unsatisfactory, with specific failure examples.
- Cost and latency constraints, since agent loops cost more per task than fixed workflows.
- Whether multiple distinct knowledge domains or tool sets are involved.

## Decision Tree

```
Can the steps to complete this task be enumerated in advance?
├── Yes, and they're stable across inputs → build a WORKFLOW (Step 2)
└── No, the steps depend on what's discovered along the way → build an AGENT (Step 3)

If building an agent, does the task span multiple distinct domains,
tool sets, or need parallel independent investigation?
├── No  → single agent loop, go to react-agent for the loop design
└── Yes → orchestrator + sub-agents (Step 5)

Is predictability or flexibility the priority?
├── Predictability, reliability, auditability → workflow, or an agent with
│    narrow tool access and tight guardrails
└── Flexibility, open-ended exploration → agent with broader autonomy
```

## Procedure

### Step 1: Classify the task before designing anything

Answer directly: can every step this task requires be listed today, or does step N depend on what step N-1 discovers? A task where the sequence is knowable in advance is a workflow even if it involves several LLM calls and conditional branches. A task where the model must decide what to do next based on intermediate results is an agent. This classification, not the number of steps or the sophistication of the prompts, is what determines the architecture.

### Step 2: Design a workflow when the path is known

Workflows compose from a small set of patterns; pick the one that matches the task shape rather than defaulting to a single long prompt:

- **Prompt chaining**: sequential steps where each output feeds the next, often with a validation gate between steps. Fits multi-stage generation or processing with clear quality checkpoints. See `prompt-chaining-and-workflows` for the full procedure, handoff design, and debugging method for this pattern specifically.
- **Routing**: a classification step directs the request to one of several specialized downstream chains. Fits requests that fall into a few known categories needing different handling.
- **Parallelization**: independent sub-tasks run concurrently and results are combined. Fits multi-criteria evaluation or independent verification where sub-tasks don't depend on each other.

Workflows earn their predictability by keeping control flow in code, not in the model's discretion. Do not let a workflow's LLM steps quietly start making routing decisions the code was supposed to make; that's an agent wearing a workflow's name.

### Step 3: Design an agent when the path isn't known

An agent needs three components working together, and a weakness in any one undermines the others:

- **Planning**: the reasoning engine that decomposes the task, tracks progress, and adapts. This is what `react-agent` operationalizes for a single loop.
- **Tools**: the interface to external systems and actions. This is what `function-calling-and-tool-design` specifies.
- **Memory**: short-term (working context for the current task) and, when tasks span sessions, long-term (retrieval over past interactions or results).

Design all three deliberately before implementation; an agent with strong tool definitions but no memory strategy will repeat work, and one with memory but weak planning will accumulate context without making progress.

### Step 4: Set guardrails proportional to autonomy

The more autonomous the agent, the more explicit the boundaries need to be, stated in the system prompt and enforced where possible in code, not left to the model's judgment alone:

- Which tools are available, and which actions require confirmation versus running freely.
- What counts as task completion, so the agent doesn't loop indefinitely refining an already-acceptable result.
- A maximum step or iteration count, so a stuck agent fails loudly instead of consuming budget silently.

### Step 5: Decide on orchestrator and sub-agents

Split into an orchestrator coordinating sub-agents when the task spans genuinely distinct domains or tool sets, or needs independent parallel investigation that a single context can't hold cleanly. Each sub-agent should get its own scoped context (its own instructions, its own relevant tools) and return a distilled result, not its full working transcript, to the orchestrator. This is a `context-engineering` concern as much as an architecture one: the reason to split is often context isolation, not just parallelism. See `context-engineering`'s multi-agent pattern for the context-handling half of this design.

### Step 6: Plan for observability from the start

Whichever architecture is chosen, plan to log what the system actually did: which tools were called, with what arguments, and what came back. This is not optional polish added after something breaks; debugging an agent without this trail means guessing at a decision the model made from context that's no longer inspectable.

## Decision Rules

- IF the steps can be listed today and stay stable across different inputs → workflow, regardless of how many LLM calls it involves.
- IF two people would reasonably expect different tool sequences for the same input → agent, not a workflow with more branches.
- IF an agent is being built for a task with a small number of known categories → routing (a workflow pattern) is very likely simpler, cheaper, and more predictable, and might be the actual answer.
- IF the agent's tool set spans genuinely unrelated domains (e.g., customer database queries and image generation) → consider whether this is really one agent or should be an orchestrator delegating to two narrower ones.
- IF reliability and auditability matter more than flexibility → favor a workflow, or an agent with a narrow tool set and required confirmation on consequential actions, over broad autonomy.
- IF debugging an agent is difficult because its decisions can't be traced → this is an observability gap, fix it before concluding the architecture itself is wrong.
- IF cost or latency is a concern → workflows are cheaper and faster per task than agent loops; don't default to an agent when a workflow would satisfy the requirement.

## Validation

1. The workflow-vs-agent classification is stated with the reason (steps knowable in advance, or not).
2. If a workflow, the pattern (chaining, routing, parallelization) is named and matches the task shape.
3. If an agent, all three components (planning, tools, memory) are addressed, not just tool access.
4. Guardrails (tool scope, confirmation requirements, iteration limits) are explicit, not implied.
5. If multi-agent, each sub-agent has a scoped context and returns distilled results, not raw transcripts.
6. A logging or observability plan exists before the system is considered done.

## Failure Conditions

- The task's steps can't be classified as knowable-in-advance or not, because the requirement itself is unclear. Get a clearer specification before choosing an architecture.
- An agent is being requested for a task that a routing workflow would handle, and the stakeholder insists on agent-level flexibility anyway. State the trade-off (cost, predictability, debuggability) explicitly rather than silently building the heavier system.
- A multi-agent design is proposed with no clear division of domains between sub-agents. Collapse back to a single agent until a genuine domain split is identified.

## Anti-Patterns

- Building an agent for a task whose steps were knowable in advance, paying autonomy's cost and unpredictability for no benefit.
- Building a rigid workflow for a task that genuinely needs adaptive tool selection, then patching its inflexibility with ever-more conditional branches.
- Letting an LLM step inside a "workflow" quietly make routing decisions that were supposed to live in code.
- Granting an agent broad tool access and unlimited iterations with no guardrails, then being surprised by cost or unpredictable behavior.
- Splitting into multiple agents without a real domain boundary between them, multiplying complexity without isolating anything.
- Treating memory as an afterthought rather than a designed component alongside planning and tools.
- Shipping an agent with no logging, then being unable to diagnose its first production failure.

## Output Format

Deliver:

1. Classification: workflow or agent, with the one-sentence reason.
2. If workflow: the pattern used (chaining/routing/parallelization) and its structure.
3. If agent: the planning approach, tool set, and memory strategy.
4. Guardrails: tool scope, confirmation requirements, iteration limits.
5. If multi-agent: orchestrator and sub-agent roles, and what each sub-agent returns.
6. Observability plan.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Architecture fit | Workflow/agent choice matches whether steps were knowable in advance |
| Pattern match | Workflow pattern (if used) matches the task shape |
| Component completeness | Agent design addresses planning, tools, and memory, not tools alone |
| Guardrail explicitness | Tool scope, confirmation rules, and iteration limits are stated, not implied |
| Observability | A logging plan exists before deployment, not added after the first failure |

## References

- `references/patterns.md` for workflow patterns in more depth, agent component design, and the orchestrator/sub-agent pattern.
- `references/sources.md` for traceability.
- Related: `function-calling-and-tool-design` for defining the tools an agent uses, `react-agent` for the single-loop reasoning-and-acting cycle, `rag-architecture-design` for private-knowledge needs that don't require autonomy, `context-engineering` for context allocation and multi-agent context isolation, `prompt-injection-defense` for securing an agent that acts on external content, `jailbreak-resistance` for securing an agent's system prompt against user-driven guideline circumvention.
