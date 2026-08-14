# Sources: prompt-chaining-and-workflows

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Prompt chaining splits a complex task into subtasks, using one prompt's response as input to the next, to improve reliability and performance | `pages/techniques/prompt_chaining.en.mdx` (Introduction) | Source-derived |
| Chaining is useful for tasks an LLM struggles with when given one very detailed prompt, and chain steps perform transformations before reaching a final desired state | `pages/techniques/prompt_chaining.en.mdx` (Introduction) | Source-derived |
| Chaining boosts transparency, controllability, and reliability, and makes debugging model responses easier by isolating stages | `pages/techniques/prompt_chaining.en.mdx` (Introduction) | Source-derived |
| Chaining is particularly useful for conversational assistants and personalization | `pages/techniques/prompt_chaining.en.mdx` (Introduction) | Source-derived |
| Worked two-stage document QA example: stage 1 extracts relevant quotes delimited from the source document, stage 2 composes an answer from the quotes and the original document | `pages/techniques/prompt_chaining.en.mdx` (Prompt Chaining for Document QA) | Source-derived |
| Chaining is one of three core workflow patterns alongside routing and parallelization, contrasted with agents where control flow isn't predefined | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (Common AI Workflow Patterns), cross-referenced from [[agentic-system-design]] in this library | Source-derived |
| Explicit handoff-shape requirement between consecutive stages as the primary failure point to design against | none | Architect recommendation |
| Validation-gate-with-fallback requirement between costly-to-fail stages | none | Architect recommendation |
| Debugging procedure of isolating and running stages independently before rewording the whole chain | none | Architect recommendation |
| Over-split vs. under-split diagnostic examples and the "hand it to someone with no other context" test for stage boundaries | none | Architect recommendation |
