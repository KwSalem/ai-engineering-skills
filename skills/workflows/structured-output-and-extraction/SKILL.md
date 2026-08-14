---
name: structured-output-and-extraction
description: >
  Gets reliable structured output from a model for extraction, classification,
  question answering, and summarization tasks: exact output formats, label
  specificity, and handling of missing or ambiguous fields. Use when a task
  needs to pull specific fields out of unstructured text, assign a fixed-label
  category, answer strictly from a given context, or condense text to a
  required length, and the current output format is inconsistent or too loose.
  Use it even when the user just says "pull out X, Y, Z from this text" or
  "give me one of these three labels" without naming extraction or classification.
---

# Structured Output and Extraction

## Purpose

Get an LLM to reliably perform one of four common structured tasks, extraction, classification, question answering, or summarization, with an output format precise enough to consume programmatically or present consistently, rather than a loosely-shaped answer that varies between runs.

## When to Use

- Pulling specific named fields out of unstructured text (names, dates, entities, amounts).
- Assigning one label from a fixed, known set of categories.
- Answering strictly from a given context, including correctly declining when the context doesn't contain the answer.
- Condensing text to a required length or focus.
- An existing extraction or classification prompt returns inconsistent field names, casing, or structure across runs.

## When NOT to Use

- The full six-element prompt design (role, constraints, settings) hasn't been established yet. Go to `prompt-design` first; this skill assumes a working prompt and focuses specifically on output shape and task-type conventions.
- The task needs example-driven convention teaching beyond a shown format (style imitation, a nuanced judgment call needing demonstrated boundary cases). Go to `few-shot-prompting`.
- The source of truth is a large or private document set, not a single passage already in context. Go to `rag-architecture-design` and `rag-retrieval-and-grounding`.
- The task is one stage inside a larger multi-step pipeline. Go to `prompt-chaining-and-workflows` for how this stage connects to others; this skill defines what one stage's output looks like.

## Required Inputs

- The task type: extraction, classification, QA, or summarization.
- For classification: the complete, fixed label set.
- For extraction: the exact fields needed.
- For QA: the context the answer must be grounded in.

## Optional Inputs

- Known ambiguous or missing-data cases that need defined behavior.
- A required output schema (JSON, specific delimiters) for downstream parsing.

## Decision Tree

```
What's the task type?
├── Extraction      → Step 1: define fields and missing-value behavior
├── Classification   → Step 2: define the exact label set and format
├── Question Answering → Step 3: ground strictly in context, define abstention
└── Summarization    → Step 4: define length and focus explicitly

Does output need to be machine-parsed downstream?
├── Yes → show the exact schema with a filled example (this skill's core technique)
└── No  → looser prose is acceptable, but still name required fields explicitly
```

## Procedure

### Step 1: Extraction — define fields and missing-value behavior explicitly

State exactly which fields to extract and what to do when a field isn't present. An extraction prompt with no defined missing-value behavior tends to either fabricate a plausible value or produce structurally inconsistent output across runs, both of which are worse than a clearly-marked absence.

```
Extract the following fields from the abstract below: model_name (array).
If no model names are found, return ["NA"].

Abstract: {text}
```

For extracting several distinct fields, show the exact output shape with a filled example rather than only naming the fields; a named-but-unshown format is the single most common cause of structurally inconsistent extraction output.

### Step 2: Classification — fix the label set and specify the exact output format

State the complete label set explicitly rather than describing categories in prose, and state the exact casing and format expected in the output.

```
Classify the text into exactly one of: positive, neutral, negative.
Respond with only the lowercase label, nothing else.

Text: {text}
Sentiment:
```

If the model returns output close to but not matching the required format (wrong casing, extra words), this is a format-specification gap, not a task-comprehension failure; tightening the exact output instruction fixes it faster than restating the classification task itself. When simple instruction tightening doesn't stabilize the format, showing one or two labelled examples is the next step; see `few-shot-prompting` for how to select and order those examples.

### Step 3: Question answering — ground strictly and define abstention

Instruct the model to answer only from the provided context, keep the answer appropriately concise, and explicitly state what to say when the context doesn't contain the answer.

```
Answer the question based on the context below. Keep the answer short and
concise. Respond "Unsure about answer" if the context doesn't contain
enough information to answer confidently.

Context: {context}

Question: {question}

Answer:
```

The abstention instruction is not optional polish; without it, a model asked to answer from context it doesn't actually contain the answer in will often produce a plausible-sounding answer from general knowledge instead, which is a grounding failure dressed up as a successful response. For abstention behavior beyond this single-prompt level, especially calibrating it systematically, see `factuality-and-hallucination-control`. A short context is not automatically a safe one: if it comes from a user or an external source rather than being written by the developer, treat it the same as a long document for injection purposes and apply `prompt-injection-defense`.

### Step 4: Summarization — define length and focus, not just "summarize"

State the required length concretely (a number of sentences, a word cap) and the focus if the source material covers more than what's needed. "Summarize this" produces wildly inconsistent length and focus across runs; "summarize the above in one sentence, focusing on X" does not.

```
Explain the following in one sentence, focusing on how it works
rather than its history:

{text}
```

## Decision Rules

- IF classification output is close to the right format but not exact (wrong case, extra text) → tighten the exact-format instruction before adding examples; this is usually a faster and cheaper fix.
- IF extraction output has inconsistent field names or structure across runs → the format was named, not shown; add a filled example.
- IF a QA prompt answers confidently on questions the context doesn't cover → the abstention instruction is missing or too weak; add it explicitly and test with a context-question pair designed to have no answer.
- IF summarization length or focus varies unpredictably → the instruction stated "summarize" without a concrete length or focus target; add both.
- IF the label set for classification isn't fully known in advance → get the complete set before writing the prompt; an incomplete label set produces predictably poor results on the missing categories regardless of prompt quality.
- IF the same structured task is needed repeatedly with format still unstable after these steps → this is the handoff point to `few-shot-prompting` for demonstrated convention.

## Validation

1. Extraction: missing-field behavior is explicitly defined and tested.
2. Classification: the complete label set is stated, and output format (case, delimiters) is exact.
3. QA: an abstention instruction exists and has been tested against a genuinely unanswerable context-question pair.
4. Summarization: length and focus are both concretely specified, not left to "summarize."
5. For machine-parsed output: the schema is shown with a filled example, not only named.

## Failure Conditions

- The complete label set for a classification task can't be determined. Get it before shipping; an undefined label space produces unpredictable behavior on uncovered categories.
- Required fields for extraction aren't agreed on. Resolve this before writing the prompt; a shifting field list invalidates any format testing already done.
- A QA system needs to answer from context that frequently doesn't contain the answer, and abstention still isn't reliable after Step 3. This has likely become a `factuality-and-hallucination-control` calibration problem, not a single-prompt fix.

## Anti-Patterns

- Naming an output format ("return JSON") instead of showing it with a filled example.
- Classifying against a described-in-prose category set instead of an explicit, fixed label list.
- Asking a model to "summarize" with no length or focus constraint and being surprised by inconsistent results.
- Omitting an abstention instruction from a QA prompt and treating the resulting fabrications as a separate, unrelated bug.
- Treating structurally inconsistent output as an example-selection problem before checking whether the format was ever actually shown.

## Output Format

Deliver:

1. Task type identified (extraction / classification / QA / summarization).
2. The prompt, with format shown via a filled example where machine parsing matters.
3. Defined behavior for missing fields, unknown labels, or unanswerable questions, as applicable.
4. For classification: the complete label set used.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Format consistency | Identical structure across repeated runs on similar input |
| Missing-value handling | Defined and tested, not left to model discretion |
| Label completeness | Full label set stated for classification tasks |
| Grounding | QA answers reflect only the provided context, with tested abstention |
| Length/focus control | Summarization output matches a concretely stated target |

## References

- `references/task-patterns.md` for further worked examples across all four task types.
- `references/sources.md` for traceability.
- Related: `prompt-design` for the underlying prompt this skill's format requirements sit within, `few-shot-prompting` for demonstrated-convention tasks beyond a shown format, `factuality-and-hallucination-control` for systematic abstention calibration, `prompt-chaining-and-workflows` for using this skill's output as one stage in a larger pipeline.
