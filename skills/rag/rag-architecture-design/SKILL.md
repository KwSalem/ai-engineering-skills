---
name: rag-architecture-design
description: >
  Decides whether a task needs Retrieval Augmented Generation at all, and if so,
  designs the indexing pipeline: chunking strategy, embedding choice, metadata,
  and index structure, choosing between Naive, Advanced, and Modular RAG
  patterns. Use when an assistant needs private, large, or frequently changing
  knowledge that does not fit in a single prompt, when deciding between RAG,
  long-context, and fine-tuning, or when an existing RAG system retrieves poorly
  because the indexing itself is wrong. Use it even when the user just says "hook
  the model up to our documents" or "it needs to know our internal stuff" without
  using the word RAG.
---

# RAG Architecture Design

## Purpose

Decide if retrieval is the right tool for a knowledge problem, and if so, design how the knowledge gets indexed so that later retrieval has something good to retrieve from. Indexing quality is a ceiling: no retrieval or grounding technique downstream can recover relevance that was never captured at indexing time.

## When to Use

- An assistant needs knowledge that is private, too large for the context window, or that changes faster than a model could be retrained on.
- Deciding between RAG, a longer context window, and fine-tuning for a knowledge problem.
- An existing RAG system retrieves irrelevant or incomplete chunks, and the cause traces back to how documents were chunked, embedded, or indexed rather than to the query itself.
- Standing up a new knowledge base from scratch.

## When NOT to Use

- The knowledge fits comfortably in a single prompt already. Go to `prompt-design`; adding retrieval to a problem context-engineering already solves is pure overhead.
- The knowledge base exists and indexing is sound, but queries return the wrong chunks or the answer isn't grounded in what was retrieved. Go to `rag-retrieval-and-grounding`.
- The question is how to measure an existing RAG system's quality. Go to `rag-evaluation`.
- The gap is behavioural (output format, tone, following complex instructions) rather than knowledge. Fine-tuning or `prompt-design` fits better; RAG adds new facts, it does not change how the model behaves.
- The system needs to take external action, not just answer from documents. Go to `function-calling-and-tool-design`.

## Required Inputs

- What knowledge the system needs, and why the model doesn't already have it.
- Approximate corpus size and how often it changes.
- Whether documents are structured, unstructured, or mixed.

## Optional Inputs

- Query examples the system must handle well.
- Latency and cost constraints.
- Whether fine-tuning is already in use or under consideration.

## Decision Tree

```
Does the model need this knowledge to answer correctly?
├── No → this is a phrasing problem, go to prompt-design
└── Yes
     │
     Does it fit in the context window with room to spare?
     ├── Yes → skip RAG, use context-engineering to place it directly
     └── No
          │
          Does the knowledge change faster than retraining cycles allow,
          or is it private/per-customer?
          ├── Yes → RAG is very likely the right tool
          └── No, it's stable domain knowledge or a style/format gap
               → consider fine-tuning instead, or alongside RAG

Building the index:
Corpus size and update frequency
├── Small, stable, single domain     → Naive RAG (index once, retrieve, generate)
├── Larger or noisier, precision matters → Advanced RAG (pre/post-retrieval optimization)
└── Multiple knowledge sources, routing,
    or retrieval needs to compose with other steps → Modular RAG
```

## Procedure

### Step 1: Confirm RAG is the right tool

State in one sentence why the model cannot already answer this: the knowledge is private, post-cutoff, too voluminous, or changes too fast to retrain against. If the honest answer is "the prompt just doesn't include it," this is a context-engineering placement problem, not a retrieval problem, and building an index would be solving the wrong layer.

### Step 2: Choose the RAG paradigm

- **Naive RAG**: index, retrieve top-k, concatenate, generate. Default starting point for a small or single-domain corpus. Known weaknesses: low precision (misaligned chunks), low recall (relevant chunks missed), and generation that either ignores retrieved content or over-relies on it.
- **Advanced RAG**: adds pre-retrieval optimization (better chunking, metadata, index structure) and post-retrieval optimization (reranking, compression) around the naive pipeline. Choose this once naive RAG's precision or recall is measurably insufficient.
- **Modular RAG**: composes retrieval with other modules (routing across sources, iterative or recursive retrieval, a memory module, a task-specific adapter). Choose this when a single retrieval pass cannot serve the query, such as multi-step questions or multiple heterogeneous knowledge sources that need different retrieval strategies.

Start at Naive RAG even when Advanced or Modular is the likely end state. It is the cheapest way to get a measurable baseline before adding complexity, and Step 6 of this skill exists specifically to prevent skipping that baseline.

### Step 3: Choose a chunking strategy

- Chunk size is corpus- and embedding-model-dependent; there is no universal correct size. Short, semantically dense embeddings favour smaller chunks (roughly sentence-level); embeddings trained on larger windows tolerate 256 to 512 token blocks.
- Chunk boundaries should respect document structure (headings, sections, list items) rather than cutting at a fixed character count, because a chunk that splits a fact across the boundary is unretrievable by either half.
- Plan to experiment: chunking strategy is one of the few decisions in this skill that is validated empirically (Step 6), not chosen analytically and left alone.

### Step 4: Design metadata and index structure

- Attach metadata that retrieval or filtering will need later: source, section, date, document type, access level. Metadata decided after indexing means a full re-index to add it.
- Decide the granularity of indexing: one flat index, or an index per source/type with routing. Flat indexing is simpler; segmented indexing is necessary once sources have different retrieval characteristics (different chunk sizes, different embedding models, different freshness).
- If the embedding model is generic and the domain is specialized (legal, medical, internal jargon), plan for a fine-tuned or domain-adapted embedding model. A generic embedding model on specialized text is a common silent cause of poor retrieval that looks like a query problem but isn't.

### Step 5: Decide RAG vs. fine-tuning vs. both

These are not mutually exclusive. RAG is for supplying knowledge the model lacks; fine-tuning is for changing how the model behaves (format, tone, instruction-following) or for teaching stable domain patterns cheaply at inference time. A system needing both a private knowledge base and a consistent specialized output format may need both, applied to different layers of the same problem.

### Step 6: Establish a baseline before optimizing

Ship Naive RAG on a representative slice of the corpus and measure retrieval quality on real queries before adding reranking, query rewriting, or a second retrieval pass. Optimizing an unmeasured pipeline is the most common way this skill's output becomes unfalsifiable. For how to measure, go to `rag-evaluation` once the pipeline exists.

## Decision Rules

- IF the corpus fits in context with room for the rest of the prompt → skip RAG entirely, this is a context-engineering placement task.
- IF retrieval quality is the complaint but indexing has never been evaluated → measure before restructuring. A chunking change made on intuition is as likely to hurt as help.
- IF the domain has specialized vocabulary and a generic embedding model is in use → suspect the embedding model before suspecting the chunking strategy or the query.
- IF the task needs facts assembled from multiple documents in sequence (multi-step, comparative, or synthesis queries) → Naive RAG's single retrieval pass is insufficient, move to Modular RAG with iterative or recursive retrieval.
- IF the gap is behavioural rather than factual → this is not a RAG problem regardless of how it's phrased. Redirect to fine-tuning or `prompt-design`.
- IF metadata needs are discovered after indexing → treat this as a signal to re-plan metadata now rather than patch around its absence in the retrieval layer.

## Validation

1. The one-sentence justification from Step 1 is written down and holds up.
2. The chosen paradigm (Naive/Advanced/Modular) is named explicitly with the reason.
3. Chunking strategy is stated with its rationale, not left as a framework default.
4. Metadata schema is defined before the first full index build.
5. A baseline retrieval measurement exists before any optimization layer is added.

## Failure Conditions

- The knowledge requirement cannot be stated in one sentence. Get a clearer specification before indexing anything.
- The corpus is not accessible in a form that can be chunked and indexed (scanned images with no OCR, proprietary formats). Solve the extraction problem first.
- Metadata requirements are unknown and undiscoverable before building. Ship a minimal schema and plan for a re-index; do not block indefinitely.
- Two stakeholders disagree on what counts as the authoritative source for the same fact. Escalate; indexing conflicting sources silently produces inconsistent answers later.

## Anti-Patterns

- Reaching for RAG when the knowledge already fits in the context window.
- Choosing Advanced or Modular RAG's complexity before measuring whether Naive RAG's simpler pipeline is already insufficient.
- Fixed-size chunking with no regard for document structure.
- Treating chunking as a one-time decision instead of an experimentally validated one.
- Skipping metadata design and retrofitting it after the first index build.
- Using RAG to fix a behavioural or formatting gap that fine-tuning or prompt design would solve more directly.
- Building the full pipeline before establishing any retrieval baseline.

## Output Format

Deliver:

1. One-sentence justification for using RAG.
2. Chosen paradigm (Naive/Advanced/Modular) with reasoning.
3. Chunking strategy and rationale.
4. Metadata schema.
5. Index structure (flat vs. segmented, routing if any).
6. Plan for the Step 6 baseline measurement.

## Evaluation Criteria

| Criterion | Passing |
|---|---|
| Necessity | RAG is justified over long-context or fine-tuning with a stated reason |
| Paradigm fit | Naive/Advanced/Modular choice matches corpus size and query complexity |
| Chunking rationale | Stated and tied to content structure and embedding model, not a default |
| Metadata completeness | Covers filtering and provenance needs known at design time |
| Baseline existence | A retrieval-quality number exists before any optimization is added |

## References

- `references/rag-patterns.md` for the Naive/Advanced/Modular taxonomy in full, augmentation strategies, and RAG vs. fine-tuning trade-offs.
- `references/sources.md` for traceability.
- Related: `context-engineering` for placing retrieved content once retrieval exists, `rag-retrieval-and-grounding` for query-time retrieval and grounding, `rag-evaluation` for measuring what this skill designed.
