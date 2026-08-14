# Sources: structured-output-and-extraction

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Text summarization example showing progressive instruction refinement (explain, then explain in one sentence) | `pages/introduction/examples.en.mdx` (Text Summarization) | Source-derived |
| Information extraction example: extracting the LLM product mentioned in a paragraph via direct instruction | `pages/introduction/examples.en.mdx` (Information Extraction) | Source-derived |
| Question answering example demonstrating structured prompt with context, instruction to keep answers short, and an explicit "Unsure about answer" fallback | `pages/introduction/examples.en.mdx` (Question Answering) | Source-derived |
| Text classification example showing that adding one labelled example fixes an output-casing mismatch that instruction alone didn't | `pages/introduction/examples.en.mdx` (Text Classification) | Source-derived |
| Worked model-name extraction prompt with explicit array output format and an explicit "NA" fallback for the no-match case | `pages/prompts/information-extraction/extract-models.en.mdx` | Source-derived |
| Collections of classification and extraction prompt examples as a recognized prompt-engineering task category | `pages/prompts/classification.en.mdx`, `pages/prompts/information-extraction.en.mdx` | Source-derived |
| Being specific about desired output format, and providing examples to demonstrate desired behavior, improves output consistency | `pages/introduction/tips.en.mdx`, cross-referenced from [[prompt-design]] in this library | Source-derived |
| Four-task-type organizing structure (extraction, classification, QA, summarization) as this skill's procedure backbone | none | Architect recommendation |
| Requirement to test QA abstention specifically against a genuinely unanswerable context-question pair, not only answerable ones | none | Architect recommendation |
| Decision rule distinguishing format-specification failures from task-comprehension failures in classification | none | Architect recommendation |
| Guidance on combining task types within one prompt, and the signal to split into a chain instead | none, cross-referenced from [[prompt-chaining-and-workflows]] in this library | Architect recommendation |
