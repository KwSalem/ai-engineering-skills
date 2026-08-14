# Sources: prompt-injection-defense

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Prompt injection is a vulnerability from concatenating trusted prompts with untrusted input, described as a form of security exploit | `pages/risks/adversarial.en.mdx` (Prompt Injection) | Source-derived |
| Task-hijacking pattern demonstrated via translation and classification examples, where injected text overrides the original instruction | `pages/risks/adversarial.en.mdx` (Prompt Injection) | Source-derived |
| Prompt leaking is a distinct injection outcome, exposing confidential prompt content such as few-shot examples that may represent proprietary IP | `pages/risks/adversarial.en.mdx` (Prompt Leaking) | Source-derived |
| Defense tactic: adding explicit instruction hardening, telling the model to disregard override attempts and perform the original task | `pages/risks/adversarial.en.mdx` (Defense Tactics: Add Defense in the Instruction) | Source-derived |
| Defense tactic: parameterizing prompt components, separating instructions from input by analogy to SQL injection defenses, with a flexibility trade-off | `pages/risks/adversarial.en.mdx` (Defense Tactics: Parameterizing Prompt Components) | Source-derived |
| Defense tactic: quoting, escaping, and structured formatting (e.g. JSON fields) as additional layers, with inconsistent robustness reported | `pages/risks/adversarial.en.mdx` (Defense Tactics: Quotes and Additional Formatting) | Source-derived |
| Defense tactic: a dedicated adversarial-prompt detector model call, evaluating whether an incoming prompt is safe before it reaches the main system | `pages/risks/adversarial.en.mdx` (Defense Tactics: Adversarial Prompt Detector) | Source-derived |
| Defense tactic: avoiding instruction-tuned models for narrow tasks in favor of k-shot prompting or fine-tuning, still not immune to injection | `pages/risks/adversarial.en.mdx` (Defense Tactics: Model Type) | Source-derived |
| No widely accepted, complete technique exists to prevent prompt injection; defenses raise the bar rather than closing the gap entirely | `pages/risks/adversarial.en.mdx` (Defense Tactics, introduction) | Source-derived |
| Six-step layered procedure combining the documented defense tactics with explicit escalation criteria | none | Architect recommendation |
| Requirement to test against both hijacking and leaking attempts, and against paraphrased/reformatted variants of a known successful attempt | none | Architect recommendation |
| Guidance to pair injection defenses with least-privilege scoping elsewhere in the system to limit blast radius of an eventual successful injection | none | Architect recommendation |
