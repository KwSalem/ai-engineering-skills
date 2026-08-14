---
name: prompt-chaining-and-workflows
description: >
  Splits a complex task into a sequence of smaller prompts where each step's
  output feeds the next, with a validation gate between stages, to improve
  reliability, transparency, and debuggability over one large prompt. Use when
  a single prompt is trying to do too much and quality suffers, when a task
  naturally decomposes into stages with different sub-goals, when debugging
  requires seeing which stage produced a bad result, or when different parts of
  a task need different context or examples. Use it even when the user just
  says "break this into steps" or "do this in stages" without saying chaining.
---

# Prompt Chaining and Workflows

## Purpose

Turn one overloaded prompt into a sequence of smaller, single-purpose prompts where each step's output becomes the next step's input, with a checkpoint between stages to catch a bad intermediate result before it compounds into a bad final one.

## When to Use

- A single prompt is asked to do multiple distinct things (extract, then reason, then format) and quality suffers on at least one of them.
- The task decomposes naturally into stages with different sub-goals, each better served by its own focused instruction.
- Debugging a complex task requires seeing which specific stage produced a bad result, not just the final output.
- Different stages benefit from different context, examples, or even different models.

## When NOT to Use

- The task is genuinely one step; splitting it adds latency and complexity for nothing. Go to `prompt-design`.
- Later steps can't be enumerated in advance because they depend on what's discovered during execution. That's an agent, not a chain; go to `agentic-system-design`.
- The output just needs a specific schema, not a sequence of transformations. Go to `structured-output-and-extraction`.
- The steps are stable but the routing between several possible paths is the real design question. Go to `agentic-system-design` for the routing pattern; a chain is one path, routing chooses between several.

## Required Inputs

- The overall task and why one prompt isn't serving it well.
- A rough sense of the natural stages, even if imperfect.

## Optional Inputs

- An existing single prompt that's underperforming, to decompose.
- Which stage(s) are suspected to be the weak point.

## Decision Tree

```
Can this task's stages be listed in advance and do they stay the same
regardless of input?
├── No  → this isn't a fixed chain, go to agentic-system-design
└── Yes
     │
     Does each stage's output map cleanly to the next stage's input?
     ├── Yes → build a linear chain (Step 1-3)
     └── No, stages branch or run independently → this is routing or
          parallelization, other workflow patterns in agentic-system-design
```

## Procedure

### Step 1: Identify the natural stages

Decompose the task into sub-tasks with a clear, single purpose each. A common and effective split for document-grounded tasks: one stage extracts the relevant material, a second stage composes the answer from what was extracted. The test for a good split: could each stage's prompt be handed to someone with no knowledge of the other stages, and would they still know what to do?

### Step 2: Design the handoff between stages

Each stage's output must be usable as the next stage's input with minimal reformatting. Specify the exact shape of what stage N produces so stage N+1 can consume it reliably: a delimited list, a labelled block, a specific field. An ill-defined handoff is the most common point of failure in a chain, more often than either stage's prompt being individually weak.

```
Stage 1 prompt: Extract relevant quotes from the document below, delimited
by ####. Output the quotes inside <quotes></quotes>. If none are found,
respond "No relevant quotes found."
####
{document}
####

Stage 2 prompt: Given the quotes below (delimited by <quotes></quotes>) and
the original document (delimited by ####), compose an accurate, helpful
answer to the question.
####
{document}
####
<quotes>
{stage 1 output}
</quotes>
```

### Step 3: Add a validation gate between stages

Insert a check after any stage whose failure would be expensive to discover only at the end: does the output match the expected shape, is it non-empty, does it pass a basic sanity check. On failure, branch to either retry that stage or route to a fallback (a manual-correction path, a simpler default) rather than letting a bad intermediate result silently propagate into the final generation.

### Step 4: Keep each stage's prompt focused

Resist folding a later stage's instructions into an earlier one just because they're both being written at the same time. A stage that does too much reintroduces the exact reliability problem chaining was meant to solve. If a stage's prompt is accumulating multiple unrelated instructions, that's a sign it should split into two stages.

### Step 5: Debug by isolating the failing stage

When the final output is wrong, don't immediately reword the whole chain. Run each stage individually and inspect its output against the expected handoff shape from Step 2; this is the direct benefit chaining provides over one large prompt, since a monolithic prompt's failure gives no such isolation.

## Decision Rules

- IF one prompt is producing inconsistent results because it's doing several distinct things → split along those distinct things, not along arbitrary length.
- IF a chain's final output is wrong → check each stage's actual output against the expected handoff shape before rewording any prompt; the failure is usually localized to one stage.
- IF a stage's prompt keeps growing to handle edge cases from a later stage → that's a sign the split is in the wrong place; move the concern to the stage it actually belongs to.
- IF the "next stage" varies depending on the current stage's result → this is routing, not a linear chain; the workflow pattern differs even though both live in `agentic-system-design`'s workflow patterns.
- IF validation between stages is skipped for cost reasons → weigh this against the cost of a bad final result reaching the user; a mid-chain check is usually far cheaper than the failure it prevents.

## Validation

1. Each stage has one clear purpose, statable independent of the other stages.
2. The handoff shape between every pair of consecutive stages is explicitly specified.
3. At least one validation gate exists after a stage whose failure would be costly.
4. Individual stages can be run and inspected in isolation for debugging.
5. No stage's prompt has silently absorbed responsibilities from another stage.

## Failure Conditions

- A task's stages can't be identified because the task itself isn't well specified yet. Get a clearer task definition before decomposing.
- Two stages have circular dependency (each needs the other's output). This isn't a chain; restructure the task or consider whether it's actually iterative and needs an agent loop instead.
- A validation gate has no defined fallback for failure. Add one; a gate that only detects failure without a recovery path just relocates the problem.

## Anti-Patterns

- Chaining a task that was genuinely one step, adding latency for no reliability gain.
- Leaving the handoff between stages implicit, causing formatting mismatches between what one stage outputs and what the next expects.
- Letting one stage's prompt grow to absorb another stage's responsibilities.
- Adding no validation between stages, so a bad intermediate result silently reaches the final generation.
- Rewording the entire chain when only one stage is actually failing.
- Using a fixed chain for a task whose steps genuinely depend on runtime discoveries; that calls for an agent, not a workflow.

## Output Format

Deliver:

1. The stages identified, each with a one-sentence purpose.
2. Each stage's prompt.
3. The handoff shape between consecutive stages.
4. Validation gates and their fallback behavior.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Stage clarity | Each stage has one statable purpose |
| Handoff explicitness | Output-to-input shape is specified, not implied |
| Gate coverage | Costly-to-fail stages have a validation gate with a fallback |
| Isolatability | A failure can be traced to one specific stage during debugging |
| Minimality | No stage does more than its one stated purpose |

## References

- `references/examples.md` for a worked document-QA chain and a debugging walkthrough.
- `references/sources.md` for traceability.
- Related: `prompt-design` for the content of any single stage's prompt, `agentic-system-design` for routing and parallelization (the other workflow patterns) and for when a fixed chain isn't flexible enough, `structured-output-and-extraction` for schema-level output requirements within a stage.
