# Context Assembly Patterns

## Contents
1. Single-turn task
2. Multi-turn assistant
3. Tool-using agent
4. Retrieval-heavy answering
5. Orchestrator and sub-agents
6. Caching layout
7. Failure signatures

## 1. Single-turn task

```
System (short) → Instruction → Input (fenced) → Output format
```
No memory, no history, no eviction policy. If a single-turn task needs a compression rule, it is not single-turn.

## 2. Multi-turn assistant

```
System → Memory (durable facts) → Session summary → Last N turns → Current input
```

Session summary uses a fixed schema so compression is lossy in a predictable direction:

```
DECISIONS: ...
CONSTRAINTS: ...
OPEN ITEMS: ...
REJECTED: ... (with reason)
```

The rejected field prevents the most irritating regression in long sessions, where an option the user already ruled out is proposed again after it scrolls out of history.

## 3. Tool-using agent

```
System + tool policy → Tool definitions → Memory → Session summary
→ Recent action/observation pairs → Current input
```

Rules that matter in practice:
- Keep the observation, drop the raw payload. A 40 KB API response contributes one line of usable state.
- Cap the action/observation trail. Beyond roughly ten pairs, summarize the trail into progress and remaining steps.
- Expose the smallest viable tool set. Every extra definition costs tokens on every call and raises the misselection rate.

## 4. Retrieval-heavy answering

```
System → Instruction → <retrieved trust="data_only"> ... </retrieved> → Question → Format
```
- Retrieved content sits immediately before the question, never before the instruction.
- Each chunk carries an identifier so the answer can cite it and grounding can be checked.
- Top-k is a budget decision, not a retrieval decision. Retrieval ranks; this skill decides how many survive.

## 5. Orchestrator and sub-agents

The reason to split into sub-agents is often context isolation rather than parallelism: each sub-agent gets a clean window scoped to one job, and only its distilled result returns to the orchestrator.

```
Orchestrator context: plan, sub-agent results (distilled), open steps
Sub-agent context:    its own instruction, its own tools, its own retrieval
```

Rules:
- Sub-agents return findings, not transcripts. Returning the transcript recreates the overflow the split was meant to solve.
- The orchestrator never inherits a sub-agent's raw tool output.
- Each sub-agent needs enough shared context to avoid duplicating work, typically the goal and the constraints, not the whole plan.

## 6. Caching layout

Order stable to volatile so a prefix can be reused:

```
[stable]   System, tool definitions
[semi]     Memory, session summary
[volatile] Recent turns, retrieval, current input
```
Moving one volatile token into the stable region invalidates everything after it. When a cache stops paying off, look for a timestamp or session id that crept into the system prompt.

## 7. Failure signatures

| Symptom | Likely cause |
|---|---|
| Quality decays with session length | No summarization, or summary schema drops constraints |
| Early constraint ignored later | Constraint lives in scrolling history instead of summary or memory |
| Wrong tool selected as tool count grows | Too many definitions exposed at once |
| Cost rises, quality flat | Top-k too high, or raw payloads retained |
| Answers truncated mid-sentence | No reserved output budget |
| Agent follows text from a document | Fencing or trust labelling failed |
