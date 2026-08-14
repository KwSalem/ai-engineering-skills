# Sources: factuality-and-hallucination-control

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| LLMs tend to generate coherent-sounding but fabricated responses; improving prompts can reduce this tendency | `pages/risks/factuality.en.mdx` | Source-derived |
| Three solution directions: providing ground truth as context, configuring lower diversity plus instructing "I don't know" admissions, and providing examples of both knowable and unknowable questions | `pages/risks/factuality.en.mdx` | Source-derived |
| Worked example: interleaving known and fabricated-entity questions, where in-context "?" responses to fabricated names teach the model to correctly abstain on a new fabricated name | `pages/risks/factuality.en.mdx` | Source-derived |
| RAG systems partially resist fabrication because correct retrieved information fixes most model errors, though a strong internal prior can still override contradicting retrieved content | `pages/research/rag-faithfulness.en.mdx`, cross-referenced from [[rag-retrieval-and-grounding]] in this library | Source-derived |
| Requirement to build a test set with both known-answerable and known-unknown halves, and to re-check both after any fix | none | Architect recommendation |
| Distinction between shallow abstention (pattern-matching obvious absurdity) and genuine calibration (correctly handling subtle, plausible fabrications) | none | Architect recommendation |
| Explicit overcorrection failure mode: a fabrication fix causing unhelpful evasiveness on genuinely answerable questions | none | Architect recommendation |
| Decision rule redirecting retrieval-grounded systems to rag-retrieval-and-grounding and rag-evaluation instead of this skill's general-purpose techniques | none, cross-referenced from [[rag-evaluation]] in this library | Architect recommendation |
