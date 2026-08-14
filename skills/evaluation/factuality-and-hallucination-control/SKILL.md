---
name: factuality-and-hallucination-control
description: >
  Reduces made-up, coherent-sounding but false output by grounding prompts in
  provided truth, calibrating the model to admit uncertainty, and testing with
  known-unknown questions designed to reveal fabrication. Use when a model states
  confident-sounding claims that turn out to be wrong, when a system needs to
  answer "I don't know" instead of guessing, when factual accuracy matters more
  than fluency, or when validating that a fix actually reduced fabrication rather
  than just changed its style. Use it even when the user just says "it's making
  things up" or "it never admits when it doesn't know" without saying hallucination.
---

# Factuality and Hallucination Control

## Purpose

Reduce a model's tendency to produce fluent, confident, and false output, and give it a working way to say "I don't know" instead of fabricating a plausible-sounding answer. This is a general-purpose skill for any prompt where factual accuracy matters; for the retrieval-specific version of this problem (a RAG system's answer not matching what it retrieved), use `rag-retrieval-and-grounding`'s grounding step and `rag-evaluation`'s faithfulness metric instead, since those have retrieval-specific tooling this skill doesn't.

## When to Use

- The model states something confidently that turns out to be false, especially names, dates, citations, or specific figures.
- A system needs to reliably decline to answer rather than guess when it genuinely lacks the information.
- Factual accuracy is the primary quality bar for a task, ahead of fluency or completeness.
- Verifying that a fix (e.g., a new instruction, added context) actually reduced fabrication rather than just changed the model's confidence phrasing while still being wrong.

## When NOT to Use

- The system retrieves from documents and the question is whether the answer matches what was retrieved. Go to `rag-retrieval-and-grounding` for grounding technique and `rag-evaluation` for the faithfulness metric; both are built specifically for the retrieval case.
- The problem is prompt wording generally, not specifically factual reliability. Go to `prompt-design`.
- The task needs systematic comparison of prompt variants beyond just factuality. Go to `prompt-evaluation-and-optimization`.
- The concern is adversarial manipulation (a user trying to extract false or harmful content deliberately) rather than ordinary fabrication. Go to `jailbreak-resistance` or `prompt-injection-defense`.

## Required Inputs

- The task or domain where factual accuracy matters.
- Whether ground-truth material (documents, a knowledge source) is available to provide as context.
- Examples of past fabrication, if debugging an existing system.

## Optional Inputs

- A set of questions the system should know the answer to, and a set it genuinely shouldn't.
- Current decoding settings (temperature, top_p).

## Decision Tree

```
Is ground-truth source material available for this task?
├── Yes → provide it as context directly (Step 1); this is the strongest lever
└── No  → rely on calibration and decoding settings (Step 2, Step 3)

Is the failure "confidently wrong" or "vague/evasive even when it knows"?
├── Confidently wrong  → this skill's calibration and testing procedure
└── Vague/evasive       → likely an over-correction from a prior fix;
                           recheck the known-answerable half of the test set (Step 4)
```

## Procedure

### Step 1: Provide ground truth as context when it exists

The single strongest lever against fabrication is giving the model the actual source material to work from rather than asking it to recall from training: a relevant article paragraph, a reference entry, or any authoritative text related to the question. This reduces the model's need to fill a knowledge gap with a plausible guess, because there's no gap left to fill from memory. When this is systematic rather than occasional, the task has likely become a RAG problem; go to `rag-architecture-design` to build that properly rather than ad-hoc pasting context into individual prompts.

### Step 2: Lower decoding diversity for factual tasks

Configure the model to produce less varied output on factual tasks: lower temperature and top_p reduce the chance of the model wandering into a confident-sounding but unsupported claim. This is the same setting guidance as in `prompt-design`, applied here specifically because diversity and factual reliability trade off directly on this class of task.

### Step 3: Explicitly instruct abstention

Tell the model directly to admit uncertainty rather than guess: instruct it to answer "I don't know" or equivalent when it genuinely lacks the information, rather than leaving abstention as an unstated option it has to infer it's allowed to take. Models default toward producing an answer because that's what most of their training reinforces; an explicit, direct permission and instruction to decline measurably changes this default.

### Step 4: Test with a known-unknown pair, not just known questions

Build a small test set with both halves deliberately present: questions the model should be able to answer correctly, and questions about things that don't exist or that the model has no way of knowing, including ones with plausible-sounding but fabricated names. A model that only abstains on obviously nonsensical questions but still fabricates on subtly fabricated ones (a plausible-sounding fake name or invented citation) hasn't actually learned to admit uncertainty, it's learned to recognize obvious absurdity, which is a much weaker property.

### Step 5: Watch for the opposite failure after fixing abstention

An abstention instruction applied too broadly or too bluntly can make a model that used to fabricate confidently start declining questions it actually could answer correctly, trading one failure mode for another. After any fix, re-run the known-answerable half of the Step 4 test set, not just the known-unknown half, to confirm the fix didn't overcorrect into unhelpful evasiveness.

## Decision Rules

- IF ground-truth material for the domain exists and isn't being provided → this is the first and cheapest fix; apply it before touching decoding settings or instructions.
- IF the model fabricates on subtly fake questions but correctly abstains on obviously nonsensical ones → the abstention behavior is shallow (pattern-matching absurdity, not genuine uncertainty recognition); the test set needs harder known-unknown cases, and the fix likely needs to be stronger than a one-line instruction.
- IF a fabrication fix causes the model to decline questions it used to answer correctly → this is overcorrection (Step 5); the fix needs to be more targeted, not stronger in the same direction.
- IF the task is retrieval-based and grounding, not general recall, is the actual mechanism → redirect to `rag-retrieval-and-grounding` and `rag-evaluation` rather than continuing with this skill's general-purpose techniques.
- IF fabrication is being measured only by spot-checking a few outputs → this isn't a reliable signal; build the Step 4 test set before concluding a fix worked.

## Validation

1. Ground-truth context is provided wherever it's available for the task.
2. Decoding settings are appropriate for a factual task (low temperature/top_p).
3. The prompt explicitly permits and instructs abstention.
4. The test set includes both known-answerable and known-unknown questions, with the unknowns including subtly plausible fabrications, not only obvious absurdities.
5. After any fix, both halves of the test set are re-checked, not just the half the fix targeted.

## Failure Conditions

- No ground-truth material exists for the domain and the task fundamentally requires factual precision. State this limitation explicitly rather than attempting to prompt-engineer around a genuine knowledge gap.
- A fabrication test set can't distinguish subtle fabrications from genuine facts without a domain expert's input. Get that input before concluding the test set is adequate; a weak test set will pass fixes that don't actually work.
- Abstention and fabrication rates move together in the same direction after a fix (both improve, or both worsen) instead of trading off as expected. This suggests the fix changed something unrelated to factuality (tone, verbosity) rather than actually addressing it.

## Anti-Patterns

- Asking a model to be more accurate through general encouragement ("be careful," "double-check") instead of providing ground truth or an explicit abstention instruction.
- Testing factuality only on questions the model is likely to know, never on plausible-sounding unknowns.
- Declaring a fabrication fix successful after checking only a handful of outputs rather than a real test set.
- Fixing fabrication so aggressively that the model starts declining questions it could have answered correctly.
- Treating a retrieval-grounded system's faithfulness problem as a general factuality problem and skipping the retrieval-specific tools built for it.

## Output Format

Deliver:

1. Ground-truth context strategy, if applicable.
2. Decoding settings recommended for the task.
3. The abstention instruction added to the prompt.
4. Test set: known-answerable and known-unknown halves, with results for both.
5. If this was a fix to an existing fabrication problem: before/after results on both halves.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Grounding | Ground-truth context supplied wherever available |
| Calibration | Model correctly abstains on known-unknown questions, including subtle fabrications |
| Helpfulness retained | Known-answerable questions still answered correctly after any abstention fix |
| Test rigor | Test set includes both halves, not just one |
| Settings fit | Decoding parameters match a factual task's low-diversity requirement |

## References

- `references/sources.md` for traceability.
- Related: `rag-retrieval-and-grounding` and `rag-evaluation` for the retrieval-specific version of this problem, `prompt-design` for decoding settings in general, `prompt-evaluation-and-optimization` for systematic before/after comparison methodology.
