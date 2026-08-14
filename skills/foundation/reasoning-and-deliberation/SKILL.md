---
name: reasoning-and-deliberation
description: >
  Chooses and applies the right amount of deliberation for a task that needs more
  than one prompt's wording to fix: chain-of-thought, self-consistency sampling,
  generated knowledge, tree-style exploration, code delegation for exact
  computation, and self-critique. Also decides when extra reasoning is wasted and
  should be removed. Use when a model reaches wrong answers on multi-step
  problems, when arithmetic or logic fails, when answers vary across runs on a
  deterministic question, when a task needs planning before answering, or when
  reasoning is on and it is unclear whether it is helping. This is about the
  amount of intermediate computation a task needs, not about how a single prompt
  is phrased; for that, see prompt-design. Use it whenever the user says the model
  "gets confused halfway" or "skips steps", even if they never say reasoning or
  chain-of-thought.
---

# Reasoning and Deliberation

## Purpose

Match compute to problem difficulty. Add deliberation only where a task actually requires intermediate work, choose the cheapest form that solves it, and remove deliberation where it adds latency and noise without accuracy.

## When to Use

- Multi-step problems: arithmetic, logic, planning, comparison against several criteria.
- Answers vary across runs on a question with one correct answer.
- The model reaches a plausible conclusion by a wrong route.
- A task needs facts assembled or a plan drafted before answering.
- Reasoning mode is enabled and its value is unverified.

## When NOT to Use

- Lookup, extraction, classification, formatting, or translation. Deliberation on these mainly adds cost and drift.
- The failure is missing knowledge. Go to `rag-architecture-design`.
- The failure is format instability. Go to `structured-output-and-extraction`.
- The task needs external actions or live data. Go to `function-calling-and-tool-design`.
- The steps are known and fixed in advance. That is a pipeline, not deliberation. Go to `prompt-chaining-and-workflows`.

## Required Inputs

- The task and its correct-answer definition.
- Whether the answer is verifiable, and by what check.
- Latency and cost tolerance, since every option here trades cost for accuracy.

## Optional Inputs

- Failing traces showing where the reasoning breaks.
- Whether the model is a reasoning model with built-in deliberation.
- Whether a code interpreter is available.

## Decision Tree

```
Is the answer exactly computable (arithmetic, dates, set logic, parsing)?
├── Yes → delegate the computation to code, do not reason it in prose
└── No
     │
     Does the task need intermediate steps at all?
     ├── No  → single prompt, no deliberation
     └── Yes
          │
          Is there one correct answer that varies across runs?
          ├── Yes → chain-of-thought plus self-consistency (sample N, take majority)
          └── No
               │
               Does it need facts the model has but does not surface?
               ├── Yes → generate knowledge first, then answer conditioned on it
               └── No
                    │
                    Are there several viable approaches to compare?
                    ├── Yes → explore branches, score, select
                    └── No  → plain chain-of-thought

Is the model already a reasoning model?
└── Yes → do not add explicit chain-of-thought instructions.
          Give it the goal, the constraints, and the success criteria instead.
```

## Procedure

### Step 1: Classify the difficulty

Answer three questions before choosing a technique:
1. Does solving it require intermediate results the final answer does not contain?
2. Is any part exactly computable?
3. Does the same input give the same answer across runs today?

A no to question 1 means stop here and return to `prompt-design`. Adding reasoning to a task that does not need it is the most common waste in this area.

### Step 2: Establish the baseline

Run the task without deliberation on 5 to 10 cases and record accuracy. Every technique below is judged against this number. Without a baseline there is no way to tell whether reasoning helped or whether the prompt merely changed. This full baseline applies when building or auditing a task from scratch; when the user instead arrives with a single existing failure to fix, see the lightweight alternative in Decision Rules.

### Step 3: Apply the cheapest sufficient technique

Escalate in this order and stop as soon as the target is met.

| Level | Technique | Apply when | Cost |
|---|---|---|---|
| 1 | Zero-shot chain-of-thought: ask for steps before the answer | Simple multi-step | Low |
| 2 | Demonstrated reasoning: examples that show the steps, not just answers | The model's step pattern is wrong | Medium |
| 3 | Generated knowledge: elicit relevant facts, then answer conditioned on them | The model knows it but does not recall it unprompted | Medium |
| 4 | Code delegation: emit code, execute, use the result | Anything exactly computable | Medium, needs an interpreter |
| 5 | Self-consistency: sample N reasoning paths, take the majority answer | One correct answer, unstable across runs | High, N times |
| 6 | Branch exploration: generate several approaches, score, expand the best | Several viable strategies, early choices matter | Highest |
| 7 | Self-critique: draft, critique against explicit criteria, revise | Quality is judged rather than computed | Medium |

Details and prompt shapes for each level are in `references/patterns.md`.

### Step 4: Separate reasoning from the answer

Fence the reasoning and require the final answer in a defined field. Mixed reasoning and answer breaks downstream parsing, and it invites the model to keep revising past its own conclusion.

```
<reasoning> ... </reasoning>
<answer> ... </answer>
```

### Step 5: Verify against the baseline

Measure the same 5 to 10 cases. Keep the technique only if accuracy improves enough to justify the added cost and latency. Record both numbers. If accuracy is unchanged, revert to the cheaper level.

### Step 6: Check the reasoning, not only the answer

Sample several traces and confirm the answer follows from the steps. A correct answer reached by wrong reasoning will fail on the next input, and it is invisible if only final answers are graded.

## Decision Rules

- IF the task is arithmetic, date maths, sorting, or parsing → delegate to code. Prose reasoning over exact computation is unreliable regardless of technique.
- IF answers vary across runs on a deterministic question → self-consistency, and set temperature above zero so paths actually differ.
- IF the reasoning is fluent but the conclusion does not follow → the model is rationalizing. Add step-level verification or switch to code delegation.
- IF reasoning is long and accuracy is unchanged → remove it and reclaim latency.
- IF the model is a reasoning model → give it goals, constraints, and success criteria, not step instructions. Prescribing steps to a model that plans internally usually shortens its own planning.
- IF the task needs a fact the model does not have → no amount of deliberation supplies it. Go to `rag-architecture-design`.
- IF branch exploration is being considered → confirm first that a scoring function exists. Without a way to compare branches it degrades into expensive sampling.
- IF the user arrives with one existing failing case rather than a task being built from scratch → do not demand the full 5-to-10-case baseline before helping. Offer a lightweight version instead: apply the fix to the failing case, then propose running it against 2 to 3 similar cases the user already has on hand to confirm the fix generalizes. Reserve the full baseline in Step 2 for building or auditing a task, not for triaging a single reported failure.

## Validation

1. Baseline accuracy recorded before any technique was applied.
2. Post-technique accuracy measured on the same cases.
3. Cost and latency delta recorded alongside the accuracy delta.
4. Sampled traces show the answer following from the steps.
5. Final answer is machine-extractable from its own field.
6. Removing the technique measurably degrades accuracy.

## Failure Conditions

- No baseline exists. Stop and measure one; otherwise no claim about improvement is meaningful.
- Accuracy fails to improve after two escalation levels. The bottleneck is knowledge, tooling, or specification, not reasoning. Return to the router.
- Reasoning traces contradict each other across runs on the same input while confidence stays high. Do not ship; the task needs verification against an external source.
- Exact computation is required and no interpreter is available. State the limitation rather than approximating it in prose.

## Anti-Patterns

- Adding "think step by step" to every prompt by default.
- Doing arithmetic in prose when a two-line script is exact.
- Self-consistency at temperature 0, which samples the same path N times and pays N times for nothing.
- Grading only final answers, letting wrong reasoning survive until it changes the answer.
- Prescribing explicit steps to a reasoning model.
- Branch exploration with no scoring function.
- Leaving reasoning in the user-facing output when only the answer was requested.
- Treating longer reasoning as better reasoning.

## Output Format

Deliver:

1. Difficulty classification and the technique chosen, with the reason.
2. The prompt, with reasoning and answer fields separated.
3. Baseline versus post-technique accuracy.
4. Cost and latency delta.
5. Any part delegated to code, with the code.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Accuracy gain | Measurable against baseline on the same cases |
| Step validity | Sampled traces support their conclusions |
| Stability | Same input gives the same answer across runs |
| Cost discipline | Cheapest sufficient level in use |
| Extractability | Final answer parseable without reading the reasoning |

## References

- `references/patterns.md` for prompt shapes at each escalation level and their trade-offs.
- `references/examples.md` for worked cases, including one where reasoning was correctly removed.
- `references/sources.md` for traceability.
- Related: `prompt-design` when the gap is wording rather than the amount of intermediate computation needed, `rag-architecture-design` when the model lacks the knowledge outright, `structured-output-and-extraction` when the output format itself is the problem, `prompt-chaining-and-workflows` when a task's steps are fixed and known rather than needing in-context deliberation, `function-calling-and-tool-design` for delegating exact computation to a real tool call rather than a code-in-prose pattern.
