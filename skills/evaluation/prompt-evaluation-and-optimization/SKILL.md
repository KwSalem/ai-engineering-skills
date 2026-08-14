---
name: prompt-evaluation-and-optimization
description: >
  Proves whether a prompt actually works and whether one version is better than
  another, using regression-safe test sets, systematic optimization (automatic
  candidate generation and structural meta-prompting), and clear pass/fail
  criteria. Use when a prompt change needs to be justified with evidence, when
  comparing two prompt variants, when a prompt that worked starts failing after
  an edit, or when scaling a prompt from one example to production reliability.
  Use it even when the user just says "did that actually help" or "prove this
  new version is better" without using the words evaluation or testing.
---

# Prompt Evaluation and Optimization

## Purpose

Give prompt changes the same evidentiary standard as code changes: a test set, a pass/fail criterion, and a regression check, so "this is better" is a measured claim rather than an impression. This skill also covers systematic prompt optimization, generating and searching over candidate phrasings rather than hand-tuning by intuition alone.

## When to Use

- A prompt change (wording, examples, settings) needs to be justified with evidence before shipping.
- Comparing two or more prompt variants to pick the better one.
- A prompt that worked previously starts failing after an unrelated edit, and the cause needs isolating.
- Scaling a prompt validated on a few examples to something that needs to hold up across a production-scale input distribution.
- Generating or searching over candidate prompt phrasings systematically rather than by hand.

## When NOT to Use

- The prompt hasn't been built yet, or the question is how to word it well in the first place. Go to `prompt-design`.
- The problem is example selection for few-shot prompting specifically. Go to `few-shot-prompting`; this skill evaluates the result, that skill builds the examples.
- The system under test is a RAG pipeline. Go to `rag-evaluation`; retrieval and grounding need their own metrics (context relevance, faithfulness), not prompt-level pass/fail.
- The concern is specifically factual accuracy or hallucination, not general prompt quality. Go to `factuality-and-hallucination-control`.

## Required Inputs

- The prompt (or prompt variants) to evaluate.
- A definition of correct or acceptable output.
- Representative input examples, ideally more than the handful used during initial design.

## Optional Inputs

- A prior version's known-good outputs, for regression comparison.
- Whether the task has one objectively correct answer or requires quality judgment.
- Budget for systematic optimization (multiple candidate generations and evaluations cost more than one hand-tuned prompt).

## Decision Tree

```
Is this a single prompt's correctness, or a comparison between variants?
├── Single prompt   → build a test set, define pass/fail, run it (Steps 1-3)
└── Comparison       → run both on the identical test set (Step 4)

Does the task have one objectively correct answer per input?
├── Yes → exact-match or rule-based scoring
└── No  → quality criteria scored by rubric or judge (Step 2)

Is hand-tuning the prompt no longer improving results?
└── Yes → consider systematic optimization: automatic candidate generation
          (Step 5) or restructuring toward meta-prompting (Step 6)
```

## Procedure

### Step 1: Build a test set before evaluating anything

Collect representative inputs beyond the one or two examples used while first drafting the prompt: typical cases, known edge cases, and at least one case similar to a documented past failure. A prompt validated only on the examples used to write it is unvalidated; those examples are exactly the ones it's most likely to have been unconsciously tuned toward.

### Step 2: Define what counts as correct

- If the task has one objectively correct answer per input (extraction, classification, exact computation), define exact-match or rule-based scoring before running anything.
- If the task requires quality judgment (drafting, summarization, tone), define explicit criteria a rubric or a judge can apply consistently: what makes an answer good, not just "good judgment" left implicit. Vague criteria produce vague, unreproducible scores regardless of how the scoring itself is executed.

### Step 3: Run and score

Run the prompt across the full test set, not a sample chosen after seeing early results. Record pass/fail or the rubric score per case, not just an aggregate; an aggregate hides whether failures cluster on a specific input type, which is exactly the information needed to fix the prompt.

### Step 4: Compare variants on the identical test set

When comparing two prompt versions, run both on the same test set with the same scoring method, and report the difference per case, not just an aggregate delta. A variant that fixes one failure mode while introducing another is a real trade-off worth surfacing, not a wash that cancels out in an average.

### Step 5: Consider automatic candidate generation for hard-to-word tasks

When manual iteration has stalled, generate multiple candidate instructions systematically rather than continuing to hand-tune one at a time: have a model propose several candidate phrasings from a small set of demonstrations, run each candidate against the test set, and keep the best-scoring one. This search-based approach has found effective instructions that weren't the obvious human-written phrasing, including for common reasoning-elicitation prompts. Reserve this for cases where hand-tuning has plateaued; it costs more calls than direct iteration and isn't worth it when a prompt is already meeting its bar.

### Step 6: Consider meta-prompting for structurally repetitive tasks

When many prompts in the same family share structure but differ in content, restructure toward emphasizing the pattern and syntax of the problem rather than content-specific detail, using abstracted examples that illustrate structure rather than fully worked content. This can reduce token cost and make comparisons across problem instances fairer, since the specific content driving few-shot examples no longer dominates the result. This depends on the model already having reliable knowledge of the task domain; it degrades on genuinely novel task types the same way zero-shot prompting does, since there's no content-specific demonstration to fall back on.

### Step 7: Watch for the exemplar-order and distribution effects during evaluation

When the prompt under test uses few-shot examples, note that the order and label distribution of those examples can measurably shift model behavior independent of the instruction wording itself. If a comparison shows a difference between two variants that also differ in example order or balance, that confound needs to be controlled before attributing the difference to the wording change being tested.

## Decision Rules

- IF a prompt was only ever tested on the examples used to write it → build a real test set before trusting it; this is not evaluation, it's confirmation.
- IF two variants are compared on different test sets or with different scoring methods → the comparison is invalid regardless of which one scores higher; rerun on the same set.
- IF failures cluster on one input type rather than spreading evenly → fix that specific gap first rather than continuing to reword the whole prompt.
- IF hand-tuning has stopped improving results after several iterations → this is the trigger for automatic candidate generation (Step 5), not a signal to give up or keep guessing.
- IF the task is genuinely novel or the model lacks reliable domain knowledge → meta-prompting's structure-over-content approach will underperform; a fully worked few-shot approach fits better.
- IF a variant comparison also changed few-shot example order or distribution → control for that separately before attributing a score difference to the wording change under test.

## Validation

1. The test set includes cases beyond the examples used during initial prompt design.
2. Correctness or quality criteria are defined before scoring, not inferred after seeing results.
3. Scores are recorded per case, not only as an aggregate.
4. Comparisons run on an identical test set with an identical scoring method.
5. Any confound (example order, distribution, model settings) between compared variants is identified and controlled.

## Failure Conditions

- No representative test set can be assembled because the task's inputs aren't yet known. Get real or realistic examples before evaluating; synthetic guesses risk testing the wrong distribution.
- Correctness criteria can't be agreed on even for a small sample. Resolve this before scoring at scale; disagreement here invalidates every downstream number.
- A regression appears after an edit and can't be isolated to a specific change. Revert to the last known-good version and reintroduce changes one at a time rather than debugging blind.

## Anti-Patterns

- Treating "it worked on my one example" as validation.
- Reporting only an aggregate score, hiding which input types are actually failing.
- Comparing two prompt variants on different test sets or scoring methods.
- Running automatic candidate generation as a default first step instead of after hand-tuning has genuinely plateaued.
- Applying meta-prompting's structure-first approach to a genuinely novel task the model doesn't already know well.
- Attributing a score difference to wording when example order or distribution differed between the compared variants too.

## Output Format

Deliver:

1. The test set: size and what it covers (typical, edge, known-failure cases).
2. Correctness/quality criteria used.
3. Per-case results, not just an aggregate.
4. For comparisons: a per-case delta table between variants.
5. If optimization was used: the candidates considered and why the winner was selected.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Test set independence | Includes cases beyond initial design examples |
| Criteria clarity | Correctness/quality defined before scoring |
| Granularity | Results reported per case, not only aggregated |
| Comparison validity | Identical test set and scoring method across variants |
| Confound control | Example order/distribution isolated from wording changes under test |

## References

- `references/optimization-methods.md` for automatic prompt engineering and meta-prompting in more depth, and the exemplar-order/distribution effects.
- `references/sources.md` for traceability.
- Related: `prompt-design` for building the prompt this skill evaluates, `few-shot-prompting` for example selection, `rag-evaluation` for RAG-specific metrics, `factuality-and-hallucination-control` for factuality-specific checks.
