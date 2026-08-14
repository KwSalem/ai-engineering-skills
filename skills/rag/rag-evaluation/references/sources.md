# Sources: rag-evaluation

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| RAG evaluation targets both retrieval and generation quality | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| Retrieval quality uses metrics from recommendation/information-retrieval domains such as NDCG and Hit Rate | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| Generation quality evaluated on relevance and harmfulness (unlabeled content) or accuracy (labeled content) | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| Three primary quality scores: context relevance, answer faithfulness, answer relevance | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| Four abilities: noise robustness, negative rejection, information integration, counterfactual robustness | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| RGB and RECALL as evaluation benchmarks | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| RAGAS, ARES, and TruLens as automated RAG evaluation tools; some rely on LLMs to determine quality scores | `pages/research/rag.en.mdx` (RAG Evaluation) | Source-derived |
| RaLLe as a framework for developing and evaluating retrieval-augmented LLMs on knowledge-intensive tasks | `pages/research/rag.en.mdx` (RAG Evaluation, citing RaLLe paper) | Source-derived |
| Evaluation is a key research direction requiring nuanced metrics and better interpretability tools as RAG applications grow more complex | `pages/research/rag.en.mdx` (Challenges & Future of RAG) | Source-derived |
| RAGAS specifically evaluates retrieval-context relevance, faithful exploitation of context, and generation quality without requiring ground-truth human annotations | `pages/research/rag.en.mdx` (References, citing RAGAS paper) | Source-derived |
| Six-step evaluation procedure (build eval set, choose scoring method, score retrieval, score generation, score four abilities, compare configurations) | none | Architect recommendation |
| Requirement to include out-of-corpus/unanswerable queries in the eval set specifically to test negative rejection | none | Architect recommendation |
| Requirement to spot-check LLM-as-judge scores against manual grades before trusting them at scale | none | Architect recommendation |
| Requirement to hold eval-set queries out from prompt-tuning and few-shot use elsewhere in the system | none | Architect recommendation |
| Worked example demonstrating why blended single-score evaluation can hide a faithfulness failure | none | Architect recommendation |
