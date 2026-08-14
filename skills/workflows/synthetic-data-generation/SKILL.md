---
name: synthetic-data-generation
description: >
  Generates diverse synthetic training or evaluation data with an LLM by
  injecting controlled randomness (entity slots, feature toggles) rather than
  repeating one fixed template, including iterative generation where earlier
  outputs seed later ones. Use when training or evaluation data is needed but
  real data is scarce, sensitive, or can't leave a private environment, when a
  generated dataset turns out repetitive despite high temperature, or when
  building query-document pairs to fine-tune a retriever. Use it even when the
  user just says "make me a bunch of realistic examples" without saying
  synthetic data.
---

# Synthetic Data Generation

## Purpose

Produce a synthetic dataset diverse enough to be useful for training or evaluation, by deliberately injecting structured randomness into generation rather than relying on temperature alone, which reliably produces repetitive output even when turned up.

## When to Use

- Real training or evaluation data is scarce, expensive to collect, or would take too long to gather before a decision is needed.
- Data is sensitive or can't leave a private environment, ruling out sending it to an external API for labeling or augmentation.
- A previously generated synthetic dataset turned out repetitive or low-diversity despite generation settings that should have helped.
- Building query-document pairs to fine-tune a local retriever model, or similar paired synthetic data for a downstream training task.

## When NOT to Use

- Real representative data is available in sufficient quantity. Use it; synthetic data is a substitute for scarcity, not a default preference over real examples.
- The need is a handful of demonstration examples for a prompt, not a training or evaluation dataset. Go to `few-shot-prompting`; that's example selection from real or hand-written cases, not dataset generation at scale.
- The generated data will be used to evaluate a system without any independent check against real distribution. See Failure Conditions; synthetic data that never gets validated against reality risks testing the wrong thing entirely.
- The goal is measuring a system's quality, not producing training data for it. Go to `prompt-evaluation-and-optimization` or `rag-evaluation` depending on what's being measured.
- The goal is building or indexing an actual RAG system's knowledge base, not generating training pairs for a retriever model. Go to `rag-architecture-design`; that skill builds the production index, this skill only prepares synthetic data to fine-tune the retriever that later serves it.

## Required Inputs

- What the synthetic data needs to represent, and why real data isn't sufficient right now.
- The target task the data will support (classification training, retriever fine-tuning, general instruction data).

## Optional Inputs

- A small seed set of real examples, if any exist, to calibrate realism.
- Known dimensions along which real data varies (vocabulary level, topic, tone, label distribution).

## Decision Tree

```
Does a repeatable structure exist that a large dataset should follow
(a story format, a query-document pair, a labelled example)?
├── No  → define the structure first; unstructured "generate examples"
│         requests are exactly what produces repetitive output
└── Yes
     │
     Can the structure be broken into variable slots (entities, features,
     labels) that differ between samples?
     ├── Yes → Step 1-3: slot-based generation
     └── No, later samples need earlier ones as context → Step 4: iterative
          generation
```

## Procedure

### Step 1: Identify what should vary between samples

List the parameters or entities that differ across the dataset: for a text-generation task, this might be topic nouns, verbs, adjectives, or narrative features; for a classification training set, it's the class label plus enough varying content that the classifier learns the underlying pattern rather than memorizing a fixed template. High generation temperature alone does not reliably produce this variation; a model given the same prompt repeatedly tends toward similar structure and content regardless of temperature, because temperature affects token-level sampling, not structural diversity.

### Step 2: Build or compile a pool of values for each variable slot

Assemble a list of possible values for each identified slot; for a vocabulary-constrained task, this might be a few hundred to a couple thousand entries split by type (nouns, verbs, adjectives). This doesn't need to be exhaustive, but it needs to be large enough that random combinations don't repeat within the target dataset size.

### Step 3: Generate by randomly sampling slots into the template

Construct each generation request by randomly filling the template's slots from the pools built in Step 2, and set generation temperature higher than default (but below maximum) to add sampling-level variation on top of the structural variation the slots already provide.

```
Write a short story (3-5 paragraphs) using very simple words a 3 year old
child would understand. The story should use the verb "{random.choice(verbs)}",
the noun "{random.choice(nouns)}", and the adjective "{random.choice(adjectives)}".
The story should include: {random.choice(features)}, {random.choice(features)}.
```

When the target task is classification training, include the class label itself as one of the slots: mentioning "positive" or "negative" directly in the generation prompt produces text pre-labelled for that class, which a local classifier can then train on directly.

### Step 4: Use iterative generation when samples benefit from intermediate structure

For more complex outputs, generate in stages where an earlier LLM call produces intermediate content (a summary, a key sentence, a set of facts) that seeds a later call, rather than generating the full final output in one pass. This is `prompt-chaining-and-workflows` applied specifically to dataset generation: each stage's output becomes the next stage's input, same as any other chain, with the specific goal here being richer, more coherently structured synthetic samples than single-pass slot-filling alone produces.

```
Stage 1: Generate a one-sentence summary and one sentence that must appear
in the story, given: {features}, {words}.

Stage 2: Summary: {stage 1 summary}
         Features: {features}
         Sentence: {stage 1 sentence}
         Words: {words}
         Story:
```

### Step 5: Validate diversity and realism before using the dataset

Before training or evaluating on generated data, check it against two failure modes: repetition (do samples cluster into a small number of near-duplicate shapes despite varying slot values) and unrealism (does the generated distribution actually resemble what real data would look like, or does it systematically differ in ways that would mislead a model trained on it). Spot-check a sample against any available real examples if they exist, even a small seed set; synthetic data validated only against itself can look internally consistent while still being systematically unrepresentative.

## Decision Rules

- IF a generated dataset is repetitive despite high temperature → the fix is structural (add or expand variable slots), not a settings adjustment; temperature alone doesn't solve structural repetition.
- IF the target task is classification training → include the label as a generation slot directly rather than generating unlabeled text and labeling it separately afterward; this produces cleanly paired text-label training data in one pass.
- IF outputs need internal coherence beyond what one-pass slot-filling provides (a plot that holds together, facts that don't contradict within one sample) → use iterative generation (Step 4), generating structure first and content second.
- IF no real data exists at all to validate against → be explicit that the dataset's realism is unverified, and treat conclusions drawn from a model trained on it as provisional until real data becomes available for even a small validation check.
- IF the dataset is meant to evaluate a system's quality rather than train one → this skill isn't the right tool for the evaluation set itself; go to `prompt-evaluation-and-optimization` or `rag-evaluation`, since an evaluation set has different integrity requirements (independence from the system under test) than training data does.

## Validation

1. Variable slots are identified and populated with a pool large enough to avoid near-duplicate samples at the target dataset size.
2. Generation temperature is set above default to add sampling variation on top of structural variation.
3. For classification data, labels are generated directly as part of each sample, not attached in a separate pass.
4. Iterative generation is used where sample coherence benefits from intermediate structure.
5. The dataset has been spot-checked for repetition and, where any real data exists, for realism against it.

## Failure Conditions

- No variable dimensions can be identified for the target data type. Get a clearer picture of what the data needs to represent before generating anything; generation without defined variation dimensions reliably produces low-diversity output.
- The dataset will be used to evaluate the same or a related system with no independent real-data check. Flag this explicitly; a system evaluated only against data generated by a similar process risks a circular, overly favorable measurement.
- Generated samples are found to systematically diverge from real data in a way that would bias downstream training. Stop and adjust the generation approach rather than proceeding on data known to be unrepresentative.

## Anti-Patterns

- Relying on temperature alone to produce dataset diversity instead of designing variable slots.
- Generating unlabeled text and hoping a separate labeling pass produces consistent labels, instead of generating the label as part of the sample.
- Using synthetic data as a default choice when sufficient real data is actually available.
- Treating a fully synthetic, self-validated dataset as equivalent to one checked against any real examples.
- Using this skill to build an evaluation set for the same system whose outputs informed the generation process, without accounting for the circularity.

## Output Format

Deliver:

1. The template structure and identified variable slots.
2. The value pools used for each slot (or a description of how they were compiled).
3. Whether generation was single-pass (Step 3) or iterative (Step 4), and why.
4. Diversity and realism spot-check results.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Structural diversity | Samples don't cluster into a small number of near-duplicate shapes |
| Label integrity | Classification labels are generated as part of each sample, verified against content |
| Coherence | Iterative generation used where single-pass would produce internally inconsistent samples |
| Realism check | Spot-checked against real data where any exists |
| Task fit | Dataset purpose (training vs. evaluation) matches how it was generated and validated |

## References

- `references/sources.md` for traceability.
- Related: `prompt-chaining-and-workflows` for the iterative generation pattern in Step 4, `few-shot-prompting` for example selection rather than dataset-scale generation, `rag-architecture-design` for building the production index this skill's retriever training data eventually serves, `prompt-evaluation-and-optimization` and `rag-evaluation` for building evaluation sets rather than training data.
