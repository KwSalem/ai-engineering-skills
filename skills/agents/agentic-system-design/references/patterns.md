# Agentic System Patterns

## Contents
1. Workflow patterns in depth
2. Agent components in depth
3. Orchestrator and sub-agent pattern
4. Workflow vs. agent comparison table
5. Hybrid systems

## 1. Workflow patterns in depth

**Prompt chaining**: break a complex task into sequential LLM calls where each step's output feeds the next, typically with a validation gate between stages. Example shape: generate an outline, evaluate it against criteria, branch to either expand the outline or route back for manual correction, then refine the final output. The validation gate is what makes chaining more reliable than one long generation: catching a bad intermediate result before it compounds is cheaper than fixing a bad final result.

**Routing**: a classification step directs the request to one of several specialized downstream handlers. Example shape: a query classifier categorizes an incoming request, then a switch sends it to a general handler, a refund handler, or a technical-support handler, each independently tuned for its category. Routing is often the simpler alternative to giving one general-purpose agent every possible tool and hoping it picks correctly.

**Parallelization**: independent sub-tasks run concurrently and their results are combined, rather than run in sequence. Fits multi-criteria evaluation (checking content against several independent policies at once) or independent verification tasks where sub-tasks share no dependency. The benefit is latency and throughput, not capability; parallelization doesn't help a task whose steps genuinely depend on each other.

## 2. Agent components in depth

**Planning** is the reasoning engine: task decomposition, self-reflection on past actions, and adaptive replanning as new information arrives. This is necessarily imperfect even in capable models, which is why Step 4's guardrails (iteration limits, explicit completion criteria) matter: a planning loop with no bound can continue "improving" indefinitely without ever being told it's done.

**Tools** turn a planned action into a real-world effect: code execution, search, calculators, image generation, database access, or any external API. The agent's tool utilization ability includes not just calling a tool but recognizing when a tool is needed and which one fits; poor tool definitions (see `function-calling-and-tool-design`) degrade this recognition even when the underlying model's reasoning is sound.

**Memory** comes in two forms with different roles:
- Short-term/working memory: the in-context buffer for the current task, sufficient for most single-session task completions, and what enables the agent to build on its own intermediate results within one run.
- Long-term memory: externalized, typically in a vector store or similar retrieval system, for information that needs to persist and be retrieved across sessions or tasks. Less commonly implemented than short-term memory but increasingly relevant as agents take on longer-running or recurring work.

## 3. Orchestrator and sub-agent pattern

Split a single agent into an orchestrator plus sub-agents when the task spans domains or tool sets distinct enough that one shared context would either force irrelevant tools into every decision or grow the working context past what's useful. Each sub-agent operates in its own scoped context: its own instructions, its own relevant tool subset, and its own working memory for its slice of the task. The orchestrator holds the overall plan and the distilled results sub-agents report back, not their full transcripts.

This is a context-isolation technique as much as a task-decomposition one: returning a sub-agent's raw transcript to the orchestrator defeats the purpose of splitting in the first place, since it just relocates the context-growth problem rather than solving it. See `context-engineering`'s orchestrator/sub-agent context pattern for the specific handling of what crosses that boundary.

## 4. Workflow vs. agent comparison table

| Aspect | Workflow | Agent |
|---|---|---|
| Control flow | Predefined, explicit, lives in code | Dynamic, decided by the model at runtime |
| Decision making | Hard-coded logic | LLM-driven reasoning |
| Tool usage | Orchestrated by code | Self-selected by the model |
| Predictability | High | Lower, trades predictability for flexibility |
| Debugging | Straightforward, steps are enumerable | Harder, requires logged reasoning traces |
| Cost per task | Lower, fixed number of calls | Higher, variable number of calls |
| Fits | Well-defined, stable-shape tasks | Open-ended tasks where steps can't be enumerated |

## 5. Hybrid systems

Many production systems are not purely one or the other. A common shape: a workflow (often a routing pattern) handles intake and directs requests to the right specialized agent, which then operates with full autonomy within its narrower domain. This captures a workflow's predictability at the entry point while still allowing agent-level flexibility for the genuinely open-ended part of the task. When designing a system that feels like it needs "a bit of both," this decomposition (workflow at the boundary, agent within a scoped domain) is usually the right shape rather than building one system that's uneasily in between.
