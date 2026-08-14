# ReAct Loop Design

## Contents
1. Trajectory exemplar pattern
2. ReAct + CoT combination
3. Self-reflection architecture
4. Worked trajectory
5. Known limitations

## 1. Trajectory exemplar pattern

For tasks needing few-shot guidance, exemplars show complete Thought/Action/Observation trajectories, not just input/output pairs:

```
Question: What is the elevation range for the area that the eastern
sector of the Colorado orogeny extends into?
Thought 1: I need to search Colorado orogeny, find the area that the
eastern sector extends into, then find that area's elevation range.
Action 1: Search[Colorado orogeny]
Observation 1: The Colorado orogeny was an episode of mountain building
in Colorado and surrounding areas.
Thought 2: It does not mention the eastern sector. I need to look that up.
Action 2: Lookup[eastern sector]
Observation 2: The eastern sector extends into the High Plains, called
the Central Plains orogeny.
Thought 3: The eastern sector extends into the High Plains. I need its
elevation range.
Action 3: Search[High Plains]
Observation 3: High Plains refers to one of two distinct land regions.
Thought 4: I need to search High Plains (United States) specifically.
Action 4: Search[High Plains (United States)]
Observation 4: The High Plains rise in elevation from around 1,800 to
7,000 ft.
Thought 5: The answer is 1,800 to 7,000 ft.
Action 5: Finish[1,800 to 7,000 ft]
```

Note the free-form thoughts serve several distinct functions across the trajectory: decomposing the original question, extracting relevant information, redirecting after an uninformative observation (Thought 4 pivots after Observation 3 turns out ambiguous), and synthesizing the final answer. A good exemplar set shows more than one of these functions, not just the happy path.

## 2. ReAct + CoT combination

Reported results show CoT alone suffers from fact hallucination since it has no access to external information, while pure ReAct's structural constraint (always acting, always grounding) can reduce its flexibility in formulating reasoning and makes it dependent on the quality of what it retrieves: an uninformative search result can derail reasoning that has no internal fallback to lean on. Prompting methods that combine and allow switching between ReAct and CoT (with self-consistency) generally outperform either alone. Practically, this means the agent's thought steps should be allowed to draw on internal reasoning when retrieval is uninformative, rather than being forced to always act next regardless of what the last observation actually contained.

## 3. Self-reflection architecture

Three roles, each with a distinct job:

- **Actor**: the ReAct loop itself (optionally CoT-augmented), generating thoughts and actions based on state and its own memory. Produces a trajectory.
- **Evaluator**: scores the completed (or failed) trajectory. The scoring function is task-dependent: an LLM judge for open-ended tasks, or a rule-based heuristic for tasks with a checkable outcome (e.g., did the code pass its tests).
- **Self-reflection**: takes the reward signal, the trajectory, and prior stored reflections, and generates a specific verbal lesson for the next attempt. This is what actually improves behavior across attempts; the evaluator alone only scores, it doesn't produce an actionable correction.

Process: define task → generate trajectory → evaluate → reflect → generate the next trajectory with the reflection in context. Reflections are stored in memory (commonly a bounded sliding window; more complex tasks may warrant a proper retrieval store) and re-supplied on subsequent attempts.

This is worth its added complexity specifically for tasks involving trial and error, where traditional fine-tuning-based reinforcement learning would be impractical (expensive, needs extensive data) and where the verbal, interpretable form of feedback is more useful for debugging than a scalar reward would be.

## 4. Worked trajectory

Query: "Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?"

```
Thought: I need to find Olivia Wilde's boyfriend, then calculate his
age raised to the 0.23 power.
Action: Search["Olivia Wilde boyfriend"]
Observation: Olivia Wilde started dating Harry Styles...
Thought: I need Harry Styles' age.
Action: Search["Harry Styles age"]
Observation: 29 years
Thought: I need to calculate 29 raised to the 0.23 power.
Action: Calculator[29^0.23]
Observation: 2.169459462491557
Thought: I now have the final answer.
Final Answer: Harry Styles is 29 years old; 29^0.23 ≈ 2.169459462491557.
```

Notice the task combined a knowledge-retrieval sub-task (finding the boyfriend, finding his age) with an exact-computation sub-task (the power calculation), and the loop correctly routed the second to a calculator tool rather than attempting it in prose. This is the same principle as delegating arithmetic to code in `reasoning-and-deliberation`, applied here as a tool call within an agent loop rather than a standalone technique.

## 5. Known limitations

- ReAct's flexibility trades off against its structural constraint: always grounding in an action can reduce the model's freedom to formulate reasoning that would benefit from more internal deliberation.
- Heavy dependence on retrieval quality: non-informative search results derail reasoning and are difficult to recover from within the same trajectory.
- Self-reflection depends on the model's own self-evaluation capability, which is imperfect and improves as underlying models improve, not something this loop design can fully compensate for.
- Sliding-window memory for reflections has a bounded capacity; complex, long-running tasks may need a proper retrieval-based memory store instead of relying on a fixed window of recent reflections.
