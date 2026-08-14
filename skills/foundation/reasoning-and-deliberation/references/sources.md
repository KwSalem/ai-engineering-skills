# Sources: reasoning-and-deliberation

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Chain-of-thought prompting elicits intermediate reasoning steps and improves multi-step tasks | `pages/techniques/cot.en.mdx` | Source-derived |
| Zero-shot chain-of-thought via an instruction to reason step by step | `pages/techniques/cot.en.mdx` | Source-derived |
| Self-consistency samples multiple reasoning paths and selects the most consistent answer, aimed at arithmetic and commonsense reasoning | `pages/techniques/consistency.en.mdx` | Source-derived |
| Generated knowledge prompting elicits knowledge first and conditions the answer on it | `pages/techniques/knowledge.en.mdx` | Source-derived |
| Program-aided language models offload computation to a code interpreter rather than computing in natural language | `pages/techniques/pal.en.mdx`, `notebooks/pe-pal.ipynb` | Source-derived |
| Tree of Thoughts explores and evaluates multiple reasoning branches with search and backtracking | `pages/techniques/tot.en.mdx` | Source-derived |
| Reflexion adds self-reflection and revision over prior attempts | `pages/techniques/reflexion.en.mdx` | Source-derived |
| Reasoning models have distinct usage patterns, and explicit step-by-step instructions are generally unnecessary for them | `pages/guides/reasoning-llms.en.mdx` | Source-derived |
| Reasoning limitations and failure modes in LLMs | `pages/research/llm-reasoning.en.mdx`, `pages/research/guided-cot.en.mdx` | Source-derived |
| Fixed 7-level escalation ladder with a stop-at-sufficient rule | none | Architect recommendation |
| Mandatory baseline measurement before applying any technique | none | Architect recommendation |
| Requirement to separate reasoning from the answer into distinct fields | none | Architect recommendation |
| Trace-level validity checking rather than final-answer grading only | none | Architect recommendation |
| Requirement of a scoring function before branch exploration | none | Architect recommendation |
| Using self-consistency spread as a confidence signal | none | Architect recommendation |
| Explicit guidance to remove deliberation when it shows no measured gain | none | Architect recommendation |
