# Retrieval and Grounding Techniques

## Contents
1. Query transformation methods
2. Reranking and position bias
3. Compression approaches
4. Grounding enforcement patterns
5. The faithfulness problem

## 1. Query transformation methods

| Method | What it does | Use when |
|---|---|---|
| Query rewriting | Reformulates the query into phrasing closer to document style | Query uses different vocabulary than the corpus |
| HyDE | Generates a hypothetical answer, embeds that instead of the raw query | Query is too short or sparse to embed meaningfully |
| Sub-queries | Splits a compound question into separate retrievable parts | Query asks about multiple things at once |
| Embedding transformation | Optimizes query embedding alignment to a task-specific latent space | Systematic mismatch across many queries, not a one-off |

Query transformation adds a model call before retrieval even starts, so it is a diagnosed fix, not a default. Apply it after confirming (via the decision tree in SKILL.md) that the query itself, not the index, is the bottleneck.

## 2. Reranking and position bias

Retrieve more candidates than the final top-k (over-fetch, e.g., retrieve 20 to keep 5), then rerank the larger set by a relevance signal more precise than the initial embedding similarity: a cross-encoder, an LLM-based relevance judgment, or a fine-tuned reranker.

Position bias is a separate, well-documented effect: models make measurably worse use of information placed in the middle of a long context than information at the start or end. Practical response: order retrieved chunks so the most relevant ones sit at the edges of the retrieved block, not buried in the middle regardless of their rank.

## 3. Compression approaches

- **Extractive**: keep only the sentences or passages within a chunk that are actually relevant to the query, discard the rest of the chunk.
- **Abstractive**: summarize a chunk or set of chunks into a shorter passage that preserves the answer-relevant content.
- **Deduplication**: when multiple chunks from overlapping or near-duplicate sources are retrieved, merge or drop redundant ones before they consume budget twice.

Compression trades completeness for budget efficiency. Always compress after confirming, by spot-check, that the answer-bearing passage survives compression; automatic summarization can drop the one specific fact a query needed while preserving the general topic.

## 4. Grounding enforcement patterns

Minimal pattern:
```
Answer only using the documents below. If they don't contain the answer, say so.

<documents>
[1] ...
[2] ...
</documents>
```

Pattern with citation requirement:
```
Answer using only the numbered documents below. After each claim, cite the
document number in brackets, e.g. [1]. If a claim can't be supported by any
document, remove it rather than stating it without a citation.

<documents>
[1] source: ..., section: ...
    "..."
</documents>
```

Pattern with explicit abstention:
```
If the documents below are insufficient to answer confidently, respond with
"The available documents don't cover this" instead of completing the answer
from other knowledge.
```

All three patterns depend on the fencing and trust-labelling described in `context-engineering`; grounding instructions are ineffective if the model cannot tell where retrieved data ends and the rest of the prompt begins.

## 5. The faithfulness problem

Correct retrieved information fixes most model errors when the model's internal prior is weak or absent on that fact. But when the model holds a strong internal prior that contradicts the retrieved content, it partially resists the retrieved information, especially as the retrieved content deviates further from what the model already "believes." This means grounding enforcement is not purely a prompting problem solvable once and left alone: the same grounding instruction can succeed on facts the model is neutral about and fail on facts the model is confidently, incorrectly certain of.

Practical implication for Step 6 (verify grounding after generation): spot-checks should specifically include cases where the retrieved content contradicts common knowledge or a plausible default assumption, since these are exactly the cases most likely to leak an ungrounded, memory-based answer despite a correctly engineered prompt.
