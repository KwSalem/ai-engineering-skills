# Sources: synthetic-data-generation

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Synthetic dataset generation is useful when real data is unavailable, sensitive, or can't be sent to an external API, requiring a locally trained model instead | `pages/applications/generating_textbooks.en.mdx` (introduction) | Source-derived |
| Ensuring dataset diversity is the main challenge; high generation temperature alone can still produce repetitive datasets | `pages/applications/generating_textbooks.en.mdx` (introduction) | Source-derived |
| Diversity technique: build a vocabulary pool split by type (nouns, verbs, adjectives), randomly select one of each per sample, and prompt the model to integrate them | `pages/applications/generating_textbooks.en.mdx` (Tackling Diversity) | Source-derived |
| Adding randomly selected feature toggles (dialogue, plot twist, bad ending) alongside entity slots further increases diversity | `pages/applications/generating_textbooks.en.mdx` (Tackling Diversity) | Source-derived |
| General procedure: identify varying parameters, compile a pool of entities, generate by random selection at higher-than-default temperature, then train a local model on the results | `pages/applications/generating_textbooks.en.mdx` (Tackling Diversity, summary steps) | Source-derived |
| A class label can itself be one of the generation entities, directly producing labelled synthetic data for classifier training | `pages/applications/generating_textbooks.en.mdx` (Tackling Diversity) | Source-derived |
| Iterative/hierarchical synthetic data generation: an earlier LLM call generates intermediate content (e.g. a summary and a required sentence) that seeds a later, more complex generation call | `pages/applications/generating_textbooks.en.mdx` (Iterative (Hierarchical) Synthetic Data Generation) | Source-derived |
| Synthetic query-document pair generation from unlabeled documents to fine-tune a local retriever model | `pages/applications/synthetic_rag.en.mdx`, cross-referenced from [[rag-architecture-design]] in this library | Source-derived |
| Framing iterative generation (Step 4) as prompt-chaining applied specifically to dataset generation | none, cross-referenced from [[prompt-chaining-and-workflows]] in this library | Architect recommendation |
| Explicit decision rule distinguishing training-data generation from evaluation-set generation, and the circularity risk of self-validated synthetic evaluation data | none | Architect recommendation |
| Requirement to spot-check generated data for both repetition and realism against any available real examples before use | none | Architect recommendation |
