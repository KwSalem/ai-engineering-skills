---
name: rag-evaluation
description: >
  Measures RAG system quality on both retrieval and generation using context
  relevance, answer faithfulness, and answer relevance, plus the four robustness
  abilities: noise robustness, negative rejection, information integration, and
  counterfactual robustness. Builds an evaluation set and a regression-safe
  measurement process. Use when a RAG system needs a quality baseline before or
  after changes, when comparing two retrieval or grounding configurations, when
  deciding if a change actually helped, or when someone asks "is our RAG any
  good" without a way to answer it. Use it even if the user only says "how do I
  know if this is working" about a system that retrieves and answers from documents.
---

# RAG Evaluation

## Purpose

Give a RAG system a measurable, repeatable quality score so that changes to indexing, retrieval, or grounding can be judged by evidence instead of impression. This skill produces the numbers that `rag-architecture-design` and `rag-retrieval-and-grounding` both depend on before optimizing anything.

## When to Use

- Establishing a baseline before optimizing a RAG pipeline (required by Step 6 of `rag-architecture-design`).
- Comparing two configurations: chunking strategies, rerankers, prompts, or models.
- Verifying that a change (new embedding model, new reranker, new grounding prompt) actually improved quality rather than just changed behavior.
- No evaluation process exists yet and one is needed before further RAG work is trustworthy.

## When NOT to Use

- The system doesn't exist yet and there's nothing to measure. Go to `rag-architecture-design` first.
- The complaint is about one specific bad answer, not systematic quality. Diagnose that single case with `rag-retrieval-and-grounding` directly; build the eval set once the pattern recurs.
- The question is about a non-RAG system's output quality. Go to `prompt-evaluation-and-optimization`.
- Only factuality/hallucination in a non-retrieval context is at issue. Go to `factuality-and-hallucination-control`.

## Required Inputs

- A working RAG pipeline to evaluate (index, retrieval, generation).
- A set of representative queries, ideally with known-correct answers or known-relevant source chunks.
- What "good" means for this system: is exact answer match required, or is faithful paraphrase acceptable.

## Optional Inputs

- An existing eval set from a prior round, for regression comparison.
- Access to an LLM-as-judge setup, if manual grading of every case isn't feasible.
- A specific configuration change under test, if this evaluation is a before/after comparison.

## Decision Tree

```
Does an evaluation set exist?
├── No  → Step 1, build one first
└── Yes → Step 2 onward, run and score

What's being evaluated?
├── Retrieval quality alone      → context relevance metrics (Step 3)
├── Generation quality alone     → faithfulness + answer relevance (Step 4)
└── End-to-end system health     → both, plus the four abilities (Step 5)

Is this a before/after comparison?
├── Yes → run both configurations on the identical eval set (Step 6)
└── No  → single-configuration baseline is sufficient
```

## Procedure

### Step 1: Build the evaluation set

- Collect 20 to 50 representative queries spanning the query types the system actually receives: simple lookup, multi-part, ambiguous, and out-of-corpus (queries the knowledge base cannot answer).
- For each query, record either the expected answer, the expected supporting source chunk(s), or both. Without this, later scoring has nothing to compare against.
- Deliberately include queries with no good answer in the corpus. A RAG system's ability to correctly say "I don't know" is as important as its ability to answer, and most eval sets built only from answerable queries never test it.
- Hold this set out; do not use any of its queries as few-shot examples or prompt-tuning material elsewhere in the system, or the evaluation stops being independent.

### Step 2: Choose manual or automatic scoring

- Manual grading is more reliable at small scale (under ~30 cases) and for establishing what "correct" means before automating.
- Automatic scoring, often LLM-as-judge, scales past that but needs its own validation: spot-check the judge's scores against manual grades on a subset before trusting it at scale.
- Frameworks in this space (RAGAS, ARES, TruLens-style triads) automate this loop; using one is a legitimate alternative to a hand-built judge, not a replacement for having an eval set and knowing what it measures.

### Step 3: Score retrieval quality (context relevance)

Measure whether the retrieved chunks are actually useful for the query, using ranking-quality metrics from information retrieval: NDCG, Hit Rate, or a simpler relevant/not-relevant judgment per retrieved chunk if ground-truth chunks are known. This is scored independently of what the model eventually generates; a system can retrieve perfectly and still generate poorly, or vice versa, and conflating the two hides which layer needs fixing.

### Step 4: Score generation quality

Two distinct scores, not one blended "quality" number:

- **Answer faithfulness**: does the generated answer actually follow from the retrieved context, without contradicting it or adding unsupported claims? This is checkable independent of whether the answer is factually true in the world; a faithful answer can still be wrong if the retrieved context itself was wrong, which is a retrieval problem, not a faithfulness problem.
- **Answer relevance**: does the answer actually address the question asked, independent of faithfulness? An answer can be perfectly faithful to the retrieved context and still fail to answer what was asked.

### Step 5: Score the four robustness abilities

These test system behavior under conditions the basic relevance/faithfulness scores don't capture:

- **Noise robustness**: does the system ignore irrelevant retrieved chunks rather than being distracted by them?
- **Negative rejection**: when no retrieved content answers the query, does the system correctly decline rather than inventing an answer?
- **Information integration**: when the answer requires synthesizing multiple retrieved chunks, does the system actually combine them rather than answering from just one?
- **Counterfactual robustness**: when retrieved content is wrong or contradictory, does the system handle it sensibly (flag the conflict, prefer the more authoritative source) rather than confidently reproducing the error?

Score these using eval-set queries specifically constructed to trigger each condition; they will not be exercised by ordinary lookup queries.

### Step 6: Compare configurations, if applicable

Run both the old and new configuration on the identical eval set, score both with the same method, and report the delta per metric, not just an aggregate. A change that improves context relevance while degrading answer faithfulness is a real, reportable trade-off, not a wash.

## Decision Rules

- IF no eval set exists → building one is not optional groundwork, it is Step 1. Do not attempt to score anything without it.
- IF retrieval scores well but generation scores poorly → the fix belongs in `rag-retrieval-and-grounding`'s grounding step, not in re-indexing.
- IF generation scores well but retrieval scores poorly → the fix belongs in `rag-architecture-design` or `rag-retrieval-and-grounding`'s retrieval step, not in prompt tuning.
- IF negative rejection scores poorly → this is a common blind spot; most eval sets never test it because they only contain answerable queries. Add out-of-corpus queries to the eval set before concluding anything else.
- IF an LLM-judge's scores are being trusted without validation → spot-check against manual grades first. An unvalidated judge can silently drift and produce a false sense of stability.
- IF comparing two configurations without a held-out identical eval set → the comparison is not valid; re-run on the same set.

## Validation

1. Eval set covers simple, multi-part, ambiguous, and out-of-corpus queries.
2. Retrieval and generation are scored separately, not blended into one number.
3. All four robustness abilities have at least a few eval-set cases designed to trigger them.
4. If using an LLM judge, its scores have been spot-checked against manual grades.
5. Before/after comparisons run on the identical eval set with the same scoring method.

## Failure Conditions

- No representative queries are available to build an eval set. Stop and get real query examples before evaluating; synthetic queries invented without user data risk testing the wrong distribution.
- The definition of "correct" cannot be agreed on for a sample of cases. Resolve this before scoring at scale; disagreement here invalidates every downstream number.
- The eval set's queries were reused as prompt-tuning material. Discard results and rebuild an independent set; the scores are no longer meaningful.

## Anti-Patterns

- Evaluating generation quality alone and treating it as whole-system evaluation.
- Building an eval set only from answerable queries, leaving negative rejection completely untested.
- Trusting an LLM-as-judge without ever spot-checking it against manual grades.
- Reporting one blended quality score instead of separate retrieval and generation numbers.
- Comparing two configurations on different eval sets or with different scoring methods.
- Reusing eval-set queries as few-shot examples elsewhere in the same system.

## Output Format

Deliver:

1. Eval set summary: size, query type coverage, source of ground truth.
2. Context relevance score.
3. Answer faithfulness score.
4. Answer relevance score.
5. Four robustness ability scores, each with example cases.
6. If comparing configurations: a per-metric delta table.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Eval set coverage | Includes simple, multi-part, ambiguous, and out-of-corpus queries |
| Score separation | Retrieval and generation scored independently |
| Robustness coverage | All four abilities have dedicated test cases |
| Judge validation | Automatic scoring spot-checked against manual grades |
| Comparison validity | Before/after runs use the identical eval set and method |

## References

- `references/metrics.md` for metric definitions, benchmark and tool references, and worked scoring examples.
- `references/sources.md` for traceability.
- Related: `rag-architecture-design` and `rag-retrieval-and-grounding` for what this skill measures, `factuality-and-hallucination-control` for factuality checks outside a retrieval context.
