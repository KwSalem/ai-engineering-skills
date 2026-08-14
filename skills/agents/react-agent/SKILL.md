---
name: react-agent
description: >
  Designs and debugs a single reasoning-and-acting loop where an agent
  interleaves explicit thoughts with tool calls and observations (Thought,
  Action, Observation), including when to add self-reflection for iterative
  improvement. Use when an agent needs to reason about what it's doing between
  tool calls rather than calling tools blindly, when a multi-step task requires
  the agent to adapt its plan based on what earlier tool calls returned, or when
  an agent loop degrades into repeated failed actions with no visible recovery.
  Use it even when the user just says "have it think before each step" or "it
  keeps repeating the same failed search" without naming ReAct.
---

# ReAct Agent

## Purpose

Design the internal loop of a single agent: how it interleaves reasoning traces with tool calls and the observations that come back, so it can track progress, adapt its plan, and recover from a bad result instead of either acting blindly or reasoning without ever checking the world. This skill assumes `agentic-system-design` has already decided an agent (not a workflow) is the right architecture, and that `function-calling-and-tool-design` has already defined the tools available; this skill designs how the loop between them actually runs.

## When to Use

- An agent needs to decide what to do next based on what previous tool calls returned, not just execute a fixed sequence.
- A task combines reasoning (deciding what information is needed) with acting (retrieving it), where neither alone is sufficient.
- An agent loop is producing repeated failed actions with no visible adaptation, and the fix is likely in how thoughts and actions are structured, not in the tools themselves.
- Deciding whether to add self-reflection so an agent improves across attempts at the same or similar tasks.

## When NOT to Use

- The architecture decision (workflow vs. agent) hasn't been made yet. Go to `agentic-system-design` first.
- The tools themselves are the problem: wrong tool selected, bad arguments, unclear descriptions. Go to `function-calling-and-tool-design`; fix the tools before tuning the loop that calls them.
- The task needs no tool calls at all, just better reasoning within a single response. Go to `reasoning-and-deliberation`.
- The problem is fitting the growing thought/action/observation history into the context budget. Go to `context-engineering`.

## Required Inputs

- The task the agent needs to accomplish through iterative reasoning and tool use.
- The tool set already available to it (from `function-calling-and-tool-design`).
- Whether the task is primarily knowledge-intensive (reasoning-heavy, few actions) or primarily decision-making (action-heavy, sparser reasoning).

## Optional Inputs

- A failing trace, if debugging an existing loop.
- Whether the agent will face the same or similar task repeatedly, which affects whether self-reflection is worth adding.
- A maximum iteration budget.

## Decision Tree

```
Does the task need reasoning interleaved with tool calls, or is one call enough?
├── One call is enough → this doesn't need a loop; a single tool call answers it
└── Needs iteration
     │
     Is the task knowledge-intensive (research, multi-hop QA) or
     decision-making (navigating a process, sequential actions)?
     ├── Knowledge-intensive → dense thought steps between actions (Step 2)
     └── Decision-making      → sparser thoughts, more action-heavy trajectory (Step 2)

Will the agent face this same or a similar task again?
├── Yes → consider adding self-reflection (Step 5)
└── No  → a plain ReAct loop without reflection is sufficient
```

## Procedure

### Step 1: Structure the loop as Thought, Action, Observation

Each cycle is: the agent generates a **thought** (what it needs to do and why), takes an **action** (a tool call), and receives an **observation** (the tool's result), which becomes part of the context for the next thought. This interleaving is what lets the agent both track and update its plan as it learns things a purely upfront plan couldn't have anticipated, and what lets it interface with external information rather than reasoning from static training knowledge alone. The action and observation here are the same events `function-calling-and-tool-design` traces for debugging tool selection; this skill adds the explicit thought around them and is the place to look when the loop itself, not a specific tool call, needs designing.

```
Thought: I need to find X before I can determine Y.
Action: search(query="...")
Observation: [result]
Thought: That didn't give me what I need; I should refine the query.
Action: search(query="...")
Observation: [result]
Thought: I now have enough to answer.
Action: finish(answer="...")
```

### Step 2: Calibrate thought density to task type

- **Knowledge-intensive tasks** (multi-hop question answering, research, fact verification): use dense reasoning, with a thought before and after nearly every action, since the primary value is in decomposing the question and deciding what to search next based on partial results.
- **Decision-making tasks** (navigating a multi-step process, sequential actions in an environment): use sparser thoughts, reasoning mainly at decision points rather than before every single action, since the trajectory is action-heavy and constant narration adds cost without adding useful adaptation.

Defaulting to one style for every task type is a common source of either wasted tokens (over-narrating simple action sequences) or under-adaptation (acting without enough reasoning on genuinely hard multi-hop questions).

### Step 3: Provide trajectory exemplars for complex or unfamiliar tasks

For tasks where the model's default reasoning pattern doesn't match what's needed, show a few complete Thought/Action/Observation trajectories as examples, not just instructions. This is `few-shot-prompting` applied specifically to trajectories rather than to input/output pairs: the examples teach the shape of good intermediate reasoning, not just the final answer format. Reserve this for genuinely complex tasks; simple ones don't need exemplars and the added tokens are pure cost.

### Step 4: Combine with chain-of-thought when purely internal reasoning also matters

The strongest reported results combine ReAct's tool-grounded reasoning with chain-of-thought's internal reasoning, letting the agent draw on both what it already knows and what it retrieves. Pure ReAct depends heavily on the quality of what it retrieves; if search results are uninformative, reasoning can derail with no internal fallback. Pure chain-of-thought has no access to external information and is more exposed to fact hallucination on knowledge-intensive tasks. Combining them, and letting the agent switch between grounded and internal reasoning as needed, outperforms either alone on most reported benchmarks.

### Step 5: Add self-reflection when the agent will retry or repeat similar tasks

For agents that attempt a task more than once, either retrying after failure within a session or facing similar tasks repeatedly, add a reflection step: after a trajectory completes (or fails), generate a verbal self-critique of what went wrong and store it as context for the next attempt. This requires three roles: an actor (the ReAct loop itself), an evaluator (scores the trajectory, via a reward signal or task-specific check), and a self-reflection step (converts the evaluation into a specific, storable lesson for the next attempt). This is a meaningful addition in cost and complexity; reserve it for tasks where repeated attempts are expected, not as a default addition to every agent loop.

### Step 6: Trace and debug stalled or looping agents

When an agent repeats the same failing action, or reasoning drifts and never recovers, get the full Thought/Action/Observation trace rather than guessing from the final output. A common pattern: one uninformative or wrong observation early in the trajectory derails everything downstream, because each subsequent thought is conditioned on it. Fixing this is often a tool-definition or retrieval-quality problem surfacing inside the loop, not a flaw in the loop structure itself; trace back to where the derailment started before deciding where to fix it.

## Decision Rules

- IF a single tool call would answer the request → skip the loop entirely; ReAct is for iterative, adaptive tasks, not a wrapper around one action.
- IF the task is knowledge-intensive and reasoning derails after an uninformative search result → this is often a retrieval-quality problem, not a reasoning problem; check `rag-retrieval-and-grounding` or the search tool's quality before restructuring the loop.
- IF the task is action-heavy (many sequential steps, few genuine decision points) → reduce thought density; narrating every action adds cost without adding adaptation.
- IF the agent will face this task or similar ones again → add self-reflection (Step 5); otherwise the added complexity isn't earning its cost.
- IF debugging a stalled loop → trace back to the first bad observation rather than assuming the most recent failing thought is the root cause.
- IF pure ReAct is derailing on tasks that also need solid internal reasoning → combine with chain-of-thought rather than adding more tool calls to compensate.

## Validation

1. Every action in the trajectory is preceded by a thought stating why, at a density appropriate to the task type.
2. Observations are demonstrably used in the next thought, not ignored or merely acknowledged.
3. The trajectory terminates in a bounded number of steps rather than looping indefinitely.
4. If self-reflection is used, each new attempt's trace shows evidence of incorporating the prior reflection, not repeating the same mistake.
5. A full trace (thoughts, actions, arguments, observations) is available for any debugging session.

## Failure Conditions

- The agent repeats the same failing action more than twice with no adaptation. Halt and trace back to the originating bad observation or tool definition rather than letting the loop continue.
- Reasoning is fluent but consistently disconnected from what the observations actually returned. This indicates the observation isn't being incorporated into context correctly, not a reasoning-quality problem.
- Self-reflection is added but successive attempts show no behavioral change. The evaluator or reflection step likely isn't producing specific, actionable feedback; check that its output is being stored and re-supplied, not just generated and discarded.

## Anti-Patterns

- Wrapping a single tool call in a full ReAct loop when one action was always going to suffice.
- Uniform thought density regardless of task type, over-narrating action-heavy tasks or under-reasoning knowledge-intensive ones.
- Adding self-reflection to every agent by default rather than to tasks that genuinely involve repeated or retried attempts.
- Debugging a stalled loop from the final output alone instead of tracing back through the full thought/action/observation history.
- Treating a derailed trajectory as a reasoning failure when the actual cause was an uninformative or wrong observation earlier in the chain.
- Providing trajectory exemplars for simple tasks that didn't need them, paying token cost for no behavioral gain.

## Output Format

Deliver:

1. The loop structure: thought density appropriate to task type, with a sample trajectory.
2. Whether chain-of-thought is combined in, and why.
3. Whether self-reflection is included, and the evaluator/reflection design if so.
4. For a debugging request: the traced trajectory with the derailment point identified.
5. Iteration or step bound, so the loop fails loudly rather than running indefinitely.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Adaptation | Later thoughts demonstrably incorporate earlier observations |
| Density fit | Thought frequency matches task type (dense for knowledge-intensive, sparse for action-heavy) |
| Termination | Trajectory ends within a bounded number of steps |
| Debuggability | Full trace available; failures traceable to a specific step |
| Reflection value (if used) | Successive attempts show measurable behavioral change |

## References

- `references/loop-design.md` for trajectory exemplar patterns, the ReAct-plus-CoT combination in more depth, and the self-reflection architecture.
- `references/sources.md` for traceability.
- Related: `agentic-system-design` for the architecture decision this loop implements, `function-calling-and-tool-design` for the tools this loop calls, `reasoning-and-deliberation` for internal-only reasoning without tool use, `context-engineering` for managing a growing thought/action/observation history.
