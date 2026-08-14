# RAG Patterns

## Contents
1. Naive, Advanced, Modular in detail
2. Augmentation stages, source, and process
3. RAG vs. fine-tuning
4. Chunking heuristics
5. Modular RAG's extended modules

## 1. Naive, Advanced, Modular in detail

**Naive RAG** is the baseline pipeline: chunk documents, embed, index, retrieve top-k for a query, concatenate with the prompt, generate. Its two chronic failure modes are low precision (retrieved chunks are topically related but not actually useful) and low recall (a genuinely relevant chunk is never retrieved because of a chunking or embedding mismatch). A third failure mode appears at generation time: the model either ignores the retrieved content and answers from memory, or leans on it so heavily that it just reiterates the passage without synthesis.

**Advanced RAG** targets the naive pipeline's weak points directly, split into pre-retrieval and post-retrieval optimization:
- Pre-retrieval (data indexing quality): enhancing data granularity, optimizing index structure, adding metadata, alignment optimization between chunks, mixed retrieval strategies.
- Post-retrieval (after chunks are retrieved, before generation): reranking to reorder by true relevance, prompt compression to fit more useful content in the same budget, and addressing the "lost in the middle" effect by relocating the most relevant chunks toward the edges of the prompt.

**Modular RAG** treats Naive and Advanced RAG as special cases of a more flexible architecture built from swappable modules: search, memory, fusion, routing, predict, and task adapter. Modules can be rearranged per task. This is the right choice once a single fixed pipeline can't serve the range of queries the system needs to handle.

## 2. Augmentation stages, source, and process

**Stages**: retrieval augmentation can happen at pre-training (building retrieval into the base model), fine-tuning, or inference (the common case for most applications). Most RAG systems built on top of an existing LLM operate purely at the inference stage.

**Source**: augmentation data is unstructured (raw text), structured (tables, knowledge graphs), or LLM-generated (synthetic passages, hypothetical documents). The source type constrains which retrieval and chunking strategies are viable.

**Process**, for problems a single retrieval pass can't resolve:
- Iterative retrieval: multiple retrieval cycles to progressively deepen relevance.
- Recursive retrieval: the output of one retrieval step feeds the next, useful for multi-step queries like legal or academic research where each answer narrows the next question.
- Adaptive retrieval: the system decides when and what to retrieve dynamically rather than always retrieving once up front.

## 3. RAG vs. fine-tuning

RAG and fine-tuning solve different problems and are not competitors for the same slot:

| | RAG | Fine-tuning |
|---|---|---|
| Adds | New or changing facts | Behavior: format, tone, instruction-following |
| Update cost | Re-index, cheap and fast | Retrain, slower and costlier |
| Best for | Knowledge-intensive, fast-changing, private data | Stable domain patterns, consistent style, complex instruction-following |

They compose well: a system can be fine-tuned to output a specific structured format while retrieving the facts that go inside that format from a RAG pipeline. Neither replaces careful prompt design; prompting remains the layer that shapes how retrieved or fine-tuned capability gets expressed in a single response.

## 4. Chunking heuristics

There is no universally correct chunk size. Two concrete data points worth calibrating against: sentence-transformer-style embeddings tend to perform best on single sentences, while embeddings trained on larger context windows (roughly ada-002 class) perform better with 256 to 512 token blocks. Beyond the embedding model, consider: typical user question length, the application's tolerance for context padding, and the corpus's natural structural units (paragraphs, sections, list items). Chunking that ignores document structure and instead cuts at a fixed character count is the single most common cause of a fact being split across two unretrievable halves.

## 5. Modular RAG's extended modules

- **Hybrid search**: combining keyword-based and semantic search to cover both exact-match and conceptual queries.
- **Recursive retrieval and query engine**: start with small chunks, progressively retrieve larger ones to enrich context once the small chunk indicates relevance.
- **StepBack prompting**: have the model abstract to a general principle before answering, which grounds responses better when the immediate retrieved passage is narrow.
- **Sub-queries**: decompose a complex query into several simpler ones, each potentially hitting a different data source.
- **Hypothetical Document Embeddings (HyDE)**: generate a hypothetical answer first, embed that, and retrieve documents similar to the hypothetical rather than to the raw query. Useful when the query itself is too sparse to embed well.
