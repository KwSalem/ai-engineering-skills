# Sources: prompt-evaluation-and-optimization

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Reliability of LLM applications is a distinct concern from getting a prompt to work once, covering generalizability, calibration, biases, and factuality | `pages/guides/prompts-reliability.md` (Reliability) | Source-derived |
| APE frames instruction generation as black-box search: an inference model proposes candidates from demonstrations, candidates are executed and scored, best is selected | `pages/techniques/ape.en.mdx` | Source-derived |
| APE discovered a zero-shot CoT instruction ("Let's work this out in a step by step way...") that outperformed the human-written "Let's think step by step" on MultiArith and GSM8K | `pages/techniques/ape.en.mdx` | Source-derived |
| Related optimization directions: Prompt-OIRL, OPRO, AutoPrompt, Prefix Tuning, Prompt Tuning | `pages/techniques/ape.en.mdx` (references) | Source-derived |
| Meta-prompting is structure-oriented and syntax-focused rather than content-driven, using abstracted examples over fully worked ones | `pages/techniques/meta-prompting.en.mdx` (Introduction, Key Characteristics) | Source-derived |
| Meta-prompting advantages over few-shot: token efficiency, fairer comparison across methods, zero-shot-like behavior | `pages/techniques/meta-prompting.en.mdx` (Advantages over Few-Shot Prompting) | Source-derived |
| Meta-prompting assumes the model has innate task knowledge; performance may degrade on novel/unique tasks similar to zero-shot prompting | `pages/techniques/meta-prompting.en.mdx` (Applications) | Source-derived |
| Distribution of few-shot exemplars can affect or bias model output depending on task difficulty | `pages/risks/biases.en.mdx` (Distribution of Exemplars) | Source-derived |
| Order of few-shot exemplars can affect model behavior | `pages/risks/biases.en.mdx` (Order of Exemplars) | Source-derived |
| Seven-step evaluation and optimization procedure (test set, criteria, run/score, compare, APE, meta-prompting, exemplar confound check) | none | Architect recommendation |
| Explicit requirement to report per-case results rather than aggregate scores | none | Architect recommendation |
| Decision rule gating automatic candidate generation behind a stalled hand-tuning attempt rather than as a default first step | none | Architect recommendation |
| Framing exemplar order/distribution as a confound specifically in variant comparisons | none | Architect recommendation |
