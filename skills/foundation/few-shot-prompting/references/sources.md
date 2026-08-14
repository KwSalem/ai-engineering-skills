# Sources: few-shot-prompting

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Few-shot prompting enables in-context learning by conditioning on demonstrations | `pages/techniques/fewshot.en.mdx` | Source-derived |
| Label space and input distribution of demonstrations matter, and format consistency matters even when individual labels are imperfect | `pages/techniques/fewshot.en.mdx` | Source-derived |
| Few-shot prompting has limits on tasks requiring multi-step reasoning, where chain-of-thought style prompting is needed instead | `pages/techniques/fewshot.en.mdx` | Source-derived |
| Zero-shot is the baseline to try before adding demonstrations | `pages/techniques/zeroshot.en.mdx` | Source-derived |
| Sentiment classification with and without demonstrations as a worked pattern | `pages/prompts/classification/sentiment-fewshot.en.mdx`, `pages/prompts/classification/sentiment.en.mdx` | Source-derived |
| Bias arising from example selection and distribution | `pages/risks/biases.en.mdx` | Source-derived |
| Specific count guidance of 2 to 5 examples as a default | none | Architect recommendation |
| Requirement to include at least one boundary case and to cover every label | none | Architect recommendation |
| Shuffling label order and placing the most representative example last | none | Architect recommendation |
| Mandatory with-versus-without comparison on held-out inputs before shipping | none | Architect recommendation |
| One-third of budget ceiling for examples | none | Architect recommendation |
| Distinct delimiters for the example block versus the live input to prevent leakage | none | Architect recommendation |
