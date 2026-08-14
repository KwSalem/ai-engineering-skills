# Sources: prompt-design

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| A prompt decomposes into named elements: instruction, context, input data, output indicator | `pages/introduction/elements.en.mdx` | Source-derived |
| Start simple and iterate; specificity improves adherence; avoid impreciseness; prefer saying what to do over what not to do | `pages/introduction/tips.en.mdx` | Source-derived |
| Instructions benefit from a leading position and separation from context with a marker such as `###` | `pages/introduction/tips.en.mdx` | Source-derived |
| Temperature and top_p control determinism; low temperature suits factual and extraction tasks, higher suits creative tasks; adjust one, not both | `pages/introduction/settings.en.mdx` | Source-derived |
| Zero-shot prompting is the default starting point before adding examples | `pages/techniques/zeroshot.en.mdx` | Source-derived |
| Task categories including summarization, extraction, QA, classification, and code generation | `pages/introduction/examples.en.mdx` | Source-derived |
| Prompt design considerations for reliability and iteration | `pages/guides/optimizing-prompts.en.mdx` | Source-derived |
| Role, constraints, and output format treated as first-class slots alongside the four documented elements | none | Architect recommendation |
| Fixed diagnostic order by fault frequency in Step 6 | none | Architect recommendation |
| One-element-at-a-time diagnosis rule | none | Architect recommendation |
| Three-run structural stability check and the empty / oversized / out-of-domain edge case triad | none | Architect recommendation |
| Escalate rather than reword when two requirements are mutually unsatisfiable | none | Architect recommendation |
| System prompt versus user prompt allocation rule | none | Architect recommendation |
