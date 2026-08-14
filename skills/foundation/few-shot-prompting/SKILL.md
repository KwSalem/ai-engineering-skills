---
name: few-shot-prompting
description: >
  Teaches a model a task by demonstration: selects, formats, orders, and balances
  in-context examples, then verifies the examples actually improved behaviour.
  Use when instructions alone fail to produce a consistent format or style, when
  the task has an implicit convention that is easier to show than describe, when
  labels or categories are domain-specific, or when output must imitate an existing
  corpus. Use it whenever the user says "here is how it should look" or pastes
  samples of the desired output, even if they never mention examples or few-shot.
---

# Few-Shot Prompting

## Purpose

Convert a hard-to-describe convention into demonstrations the model can imitate, without the demonstrations themselves introducing bias or drift.

## When to Use

- Three instruction revisions have not stabilized the output. This is the handoff point from `prompt-design`.
- The desired style, tone, or label taxonomy is domain-specific.
- The output convention is easier to show than to state, such as an internal report layout or a labelling rule with exceptions.
- Formatting must match an existing corpus exactly.

## When NOT to Use

- The instruction was never made specific in the first place. Fix that first in `prompt-design`; examples are expensive and they hide sloppy instructions rather than repairing them.
- The failure is arithmetic or multi-step logic. Demonstrations of answers do not teach a procedure. Go to `reasoning-and-deliberation`.
- The failure is missing facts. Go to `rag-architecture-design`.
- Examples would need to carry sensitive or customer data. Redact or synthesize first; see `synthetic-data-generation`.

## Required Inputs

- The task and its correct-output definition.
- At least two genuinely correct examples.
- The full label set, when the task is classification.

## Optional Inputs

- Known hard cases and near-misses.
- Real class distribution, when it differs from the example distribution.
- A token budget.

## Decision Tree

```
Does the task have a fixed label set?
├── Yes → cover every label at least once, and keep the order shuffled
└── No
     ├── Style or format imitation → 2 to 5 examples, maximum format consistency
     └── Nuanced judgement task    → include 1 near-miss with the correct call

Are examples pushing the prompt past the budget?
├── Yes → cut examples before cutting instruction or input
└── No  → proceed
```

## Procedure

### Step 1: Confirm examples are the right tool

State in one sentence what the examples will teach that instructions could not. If that sentence describes something a clearer instruction would fix, return to `prompt-design`. Examples cost tokens on every call forever, so they should be buying something instructions cannot.

### Step 2: Select examples

- Start with 2 to 5. More is not better: past a handful, added examples mostly narrow the model onto their surface features.
- Cover the range of inputs the prompt will see, not just the easy centre.
- Include at least one boundary case where the correct answer is not obvious, since the boundary is where the model will actually fail.
- For classification, include every label. A label never demonstrated is systematically underpredicted.

### Step 3: Format identically

Every example uses the same delimiters, key names, casing, and field order, and the final format matches the format demanded of the model. Inconsistency across examples is worse than having no examples, because the model then infers that format is optional.

```
Input: <text>
Label: <label>

Input: <text>
Label: <label>

Input: <the real input>
Label:
```

### Step 4: Order and balance

- Shuffle labels so they do not appear in blocks. Consecutive identical labels create a recency bias toward that label.
- Match the example distribution to the real distribution unless a rare class is being deliberately boosted, in which case say so in the instruction.
- Place the most representative example last. It sits closest to generation and carries the most weight.

### Step 5: Verify the examples earned their place

Run the prompt with examples and without, on the same 5 to 10 inputs that were not used as examples. Keep the examples only if they improve a stated metric. If the gain is invisible, delete them and reclaim the budget. For a rigorous comparison, use `prompt-evaluation-and-optimization`.

## Decision Rules

- IF the model copies an example verbatim into its answer → the examples are too close to the real input or too few. Diversify or reduce.
- IF one label dominates the output → check example balance and label ordering first, before touching the instruction.
- IF adding examples degrades performance → the task is reasoning-bound, not convention-bound. Go to `reasoning-and-deliberation`.
- IF examples exceed roughly a third of the prompt budget → cut to the most representative subset.
- IF the model handles demonstrated cases well and undemonstrated cases badly → coverage is the gap, not count.
- IF only one correct example exists → ship one-shot and record the limitation rather than inventing a second. An invented example teaches an invented convention.

## Validation

1. Every example is correct. One wrong example teaches the wrong rule with full confidence.
2. Formatting is byte-identical across examples.
3. Every label appears at least once.
4. Labels are not clustered in order.
5. Held-out inputs, never shown as examples, are handled correctly.
6. The with-versus-without comparison shows a measurable gain.

## Failure Conditions

- Correct examples cannot be produced. Stop; the task specification is incomplete.
- Examples contain confidential data that cannot be redacted. Stop and synthesize instead.
- Performance is unchanged with and without examples across two selection attempts. The bottleneck is elsewhere; return to the router.
- The model reproduces example content as if it were input data. Delimiting has failed; return to `prompt-design` Step 2.

## Anti-Patterns

- Adding examples to compensate for a vague instruction.
- Twenty examples when five would do, spending budget for no measured gain.
- Examples drawn only from easy inputs, leaving the boundary undemonstrated.
- Inconsistent formatting between examples.
- All examples sharing a label, or labels appearing in sorted blocks.
- Demonstrating answers for tasks that need a demonstrated procedure.
- Never re-checking whether the examples still help after the instruction was rewritten.

## Output Format

Deliver:

1. The prompt with examples in final position and format.
2. The selection rationale: what each example covers.
3. Coverage table: label or case type against example count.
4. With-versus-without result on held-out inputs.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Format compliance | 100 percent on held-out inputs |
| Coverage | Every label and every known case type demonstrated |
| Generalization | Held-out accuracy within a small margin of demonstrated cases |
| Efficiency | No example removable without measurable loss |
| Bias | No label overpredicted relative to true distribution |

## References

- `references/examples.md` for worked selection, ordering, and failure walkthroughs.
- `references/sources.md` for traceability.
- Related: `prompt-design` upstream, `structured-output-and-extraction` when the demonstrated convention is a schema, `prompt-evaluation-and-optimization` for the comparison method.
