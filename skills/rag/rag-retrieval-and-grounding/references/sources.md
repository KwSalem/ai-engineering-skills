# Sources: rag-retrieval-and-grounding

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Query rewriting, HyDE, and embedding transformation as methods for aligning queries and documents in semantic space | `pages/research/rag.en.mdx` (Retrieval: Aligning Queries and Documents) | Source-derived |
| Sub-queries and recursive/tree query strategies for decomposing complex questions | `pages/research/rag.en.mdx` (Modular RAG) | Source-derived |
| Reranking reorders retrieved documents to prioritize the most relevant at the top; information compression reduces noise and addresses context length limits | `pages/research/rag.en.mdx` (Generation: Post-retrieval with Frozen LLM) | Source-derived |
| Relocating relevant context to the edges of the prompt as a reranking approach, and recalculating semantic similarity post-retrieval | `pages/research/rag.en.mdx` (Advanced RAG) | Source-derived |
| Models make worse use of information placed in the middle of a long context ("Lost in the Middle") | `pages/research/rag.en.mdx` (References, citing Liu et al.) | Source-derived |
| Retrieved evidence enhances accuracy, controllability, and relevancy, and helps reduce hallucination | `pages/research/rag.en.mdx` (Introduction to RAG) | Source-derived |
| Correct retrieved information fixes most model mistakes (94% accuracy in the cited study), but models with a strong internal prior partially resist retrieved information that contradicts it, more so as it deviates further from the prior | `pages/research/rag-faithfulness.en.mdx` | Source-derived |
| RAG mitigates hallucination in structured-output generation even with small retrievers | `pages/research/rag_hallucinations.en.mdx` | Source-derived |
| Fine-tuning retrievers and adapters to align retriever output with LLM preferences | `pages/research/rag.en.mdx` (Retrieval: Aligning Retriever and LLM) | Source-derived |
| Explicit fencing and trust-labelling of retrieved content as data, not instruction | none, cross-referenced from [[context-engineering]] in this library | Architect recommendation |
| Six-step diagnostic procedure separating retrieval problems from generation problems | none | Architect recommendation |
| Mandatory post-generation grounding verification step (Step 6), specifically targeting prior-contradicting facts | none | Architect recommendation |
| Explicit citation-format patterns and abstention-instruction patterns | none | Architect recommendation |
| Decision rule to route back to rag-architecture-design when a well-formed query still retrieves irrelevant chunks | none | Architect recommendation |
