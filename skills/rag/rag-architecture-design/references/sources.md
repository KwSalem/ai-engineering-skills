# Sources: rag-architecture-design

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| RAG augments LLMs with external knowledge for knowledge-intensive or domain-specific tasks that need continually updating information, without retraining | `pages/research/rag.en.mdx` (Introduction to RAG) | Source-derived |
| RAG workflow: input, indexing (chunk, embed, index), retrieval, generation | `pages/research/rag.en.mdx` (Introduction to RAG) | Source-derived |
| Naive, Advanced, and Modular RAG as an evolutionary taxonomy, with Naive and Advanced as special cases of Modular | `pages/research/rag.en.mdx` (RAG Paradigms) | Source-derived |
| Naive RAG's known limitations: low precision, low recall, outdated information, redundancy, and over-reliance on retrieved content | `pages/research/rag.en.mdx` (Naive RAG) | Source-derived |
| Advanced RAG's pre-retrieval (data granularity, index structure, metadata, alignment, mixed retrieval) and post-retrieval (reranking, compression) optimization | `pages/research/rag.en.mdx` (Advanced RAG) | Source-derived |
| Modular RAG's extended modules: search, memory, fusion, routing, predict, task adapter | `pages/research/rag.en.mdx` (Modular RAG) | Source-derived |
| Hybrid search, recursive retrieval, StepBack prompting, sub-queries, and HyDE as Modular RAG optimization techniques | `pages/research/rag.en.mdx` (Modular RAG) | Source-derived |
| Chunking strategy is content- and embedding-model-dependent; sentence-transformer models favour single sentences, ada-002-class embeddings favour 256-512 token blocks | `pages/research/rag.en.mdx` (Retrieval: Enhancing Semantic Representations) | Source-derived |
| Fine-tuned or domain-adapted embedding models improve retrieval relevance for specialized domains | `pages/research/rag.en.mdx` (Retrieval: Fine-tuned Embedding Models) | Source-derived |
| Augmentation stages (pre-training, fine-tuning, inference), source (unstructured, structured, LLM-generated), and process (iterative, recursive, adaptive retrieval) | `pages/research/rag.en.mdx` (Augmentation) | Source-derived |
| RAG and fine-tuning are complementary rather than mutually exclusive; RAG for new knowledge, fine-tuning for internal knowledge, output format, and instruction-following | `pages/research/rag.en.mdx` (RAG vs. Fine-tuning) | Source-derived |
| RAG combines an information retrieval component with a text generator, and can be updated without retraining the whole model | `pages/techniques/rag.en.mdx` | Source-derived |
| RAG mitigates hallucination and improves factual consistency in knowledge-intensive tasks | `pages/techniques/rag.en.mdx` | Source-derived |
| Correct retrieved information corrects most model errors, but LLMs partially resist retrieved information that strongly contradicts a confident internal prior | `pages/research/rag-faithfulness.en.mdx` | Source-derived |
| RAG can mitigate hallucination in structured-output tasks even with small models and small retrievers in resource-limited settings | `pages/research/rag_hallucinations.en.mdx` | Source-derived |
| Six-step decision tree (necessity check, fit check, volatility/privacy check, paradigm selection by corpus size) | none | Architect recommendation |
| Mandating Naive RAG as the required starting point before Advanced or Modular, regardless of anticipated end state | none | Architect recommendation |
| Requirement to define metadata schema before the first full index build | none | Architect recommendation |
| Requirement of a measured baseline before any optimization layer is added | none | Architect recommendation |
| Explicit decision rule to redirect behavioural (non-factual) gaps away from RAG | none | Architect recommendation |
