# RAG Evaluation Metrics

## Contents
1. The three quality scores
2. The four robustness abilities
3. Retrieval-quality metrics
4. Benchmarks and tools
5. Worked scoring example

## 1. The three quality scores

| Score | Question it answers | Scored against |
|---|---|---|
| Context relevance | Are the retrieved chunks precise and specific to the query? | The query and retrieved chunks, before generation |
| Answer faithfulness | Does the generated answer follow from the retrieved context without contradiction or unsupported addition? | The generated answer against the retrieved context |
| Answer relevance | Does the generated answer address the question actually asked? | The generated answer against the original query |

These are deliberately independent. A system can score high on context relevance and low on faithfulness (good retrieval, model ignores it), or high on faithfulness and low on relevance (accurately reflects the context but doesn't answer the question), or high on both individually while the retrieved context itself was wrong (a context relevance failure masquerading as a faithfulness pass, since the answer faithfully reflects incorrect source material). Scoring all three separately is what makes the failure locatable.

## 2. The four robustness abilities

| Ability | What it tests | How to construct eval cases |
|---|---|---|
| Noise robustness | Ignoring irrelevant retrieved chunks | Deliberately include a distractor chunk alongside the correct one and confirm the answer isn't corrupted by it |
| Negative rejection | Correctly declining when no retrieved content answers the query | Include queries with no answer anywhere in the corpus, confirm the system says so |
| Information integration | Synthesizing multiple retrieved chunks into one answer | Construct queries whose answer requires combining facts from at least two different chunks |
| Counterfactual robustness | Handling wrong or contradictory retrieved content sensibly | Inject a deliberately incorrect or outdated chunk alongside a correct one, check whether the system flags the conflict or picks the more authoritative source |

These four require purpose-built eval cases. Ordinary lookup queries against a clean corpus will not exercise any of them, which is why an eval set built only from "normal" queries systematically under-tests exactly the failure modes that matter most in production.

## 3. Retrieval-quality metrics

Borrowed from information retrieval and recommendation systems, since ranking relevant results is the same underlying problem:

- **NDCG (Normalized Discounted Cumulative Gain)**: rewards relevant results appearing higher in the ranked list, with diminishing credit for relevance further down. Needs graded relevance judgments (not just relevant/not-relevant) to use fully.
- **Hit Rate**: simpler binary measure of whether at least one relevant chunk appears in the top-k retrieved. Easier to compute when only relevant/not-relevant judgments exist, but less informative about ranking quality within the top-k.
- **F1 / Exact Match**: task-specific metrics for the final generated answer when a canonical correct answer exists, more common for closed-domain QA evaluation than for open-ended RAG.

## 4. Benchmarks and tools

- **RGB** and **RECALL**: published benchmarks for evaluating RAG models against standardized query sets.
- **RAGAS**: automated evaluation framework covering context relevance, faithfulness, and answer relevance without requiring ground-truth human annotations for every metric.
- **ARES**: another automated RAG evaluation framework in the same space.
- **TruLens**: implements a "RAG triad" evaluation pattern, scoring the same three dimensions (context relevance, groundedness, answer relevance) as a structured triad.
- **RaLLe**: a framework specifically for developing and evaluating retrieval-augmented LLMs on knowledge-intensive tasks.

Adopting one of these tools is a reasonable substitute for hand-building a scoring pipeline, but it does not substitute for Step 1 of the parent skill: an eval set with known-relevant chunks or known-correct answers still has to exist and be held out, regardless of which tool scores it.

## 5. Worked scoring example

Query: "What's our refund window for damaged items?"

Retrieved: [1] general return policy (30-day window), [2] damaged-item-specific policy (14-day window, requires photo evidence).

Generated answer: "You have 30 days to request a refund for damaged items."

Scoring:
- Context relevance: high. Both chunks are genuinely relevant to a refund question.
- Answer faithfulness: fails. The answer states 30 days, but the more specific, more authoritative chunk [2] states 14 days for damaged items specifically. The model used the general policy and ignored the more relevant specific one.
- Answer relevance: high in isolation (it does answer "what's the refund window"), which is exactly why blended scoring would have hidden the faithfulness failure. A single combined "quality" score might have landed acceptably despite the answer being materially wrong.
- Information integration: fails. The correct answer required recognizing that [2] overrides [1] for this specific case, not averaging or picking one arbitrarily.

This is a case where a single-number evaluation would have shipped a wrong answer with a passing grade; separated scoring is what surfaces the actual defect.
