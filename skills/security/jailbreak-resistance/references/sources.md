# Sources: jailbreak-resistance

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Modern LLMs are aligned to avoid unethical or harmful output via safety policies, but jailbreaking techniques can still bypass these guardrails | `pages/risks/adversarial.en.mdx` (Jailbreaking) | Source-derived |
| Jailbreaking attempts have been observed bypassing content policy through indirect or reframed requests rather than direct ones | `pages/risks/adversarial.en.mdx` (Illegal Behavior) | Source-derived |
| Persona-based jailbreaking exists as a documented category, where a user instructs the model to adopt a character described as having no behavioral restrictions | `pages/risks/adversarial.en.mdx` (DAN) | Source-derived |
| Jailbreak techniques have iterated over time as models improve against known attempts, with attempts becoming more sophisticated in response | `pages/risks/adversarial.en.mdx` (DAN) | Source-derived |
| The Waluigi Effect describes how training a model to satisfy a desirable property can make it easier to elicit the opposite property | `pages/risks/adversarial.en.mdx` (The Waluigi Effect, citing LessWrong) | Source-derived |
| Simulated-system or simulated-program framing is a documented jailbreaking category that indirectly elicits disallowed output by asking the model to simulate a program or game rather than answer directly | `pages/risks/adversarial.en.mdx` (GPT-4 Simulator, Game Simulator) | Source-derived |
| No universally accepted, complete defense against these attacks exists; models continue to improve against known techniques while new variants are discovered | `pages/risks/adversarial.en.mdx` (Jailbreaking, general framing) | Source-derived |
| Four-category taxonomy of reframing attempts (persona/role-play, hypothetical/fictional, simulated system, escalating reframing) | none | Architect recommendation |
| Explicit framing of "regardless of hypothetical, fictional, roleplay, or persona framing" as a system-prompt hardening pattern | none, structurally parallel to the instruction-hardening tactic in [[prompt-injection-defense]] in this library | Architect recommendation |
| Decision rule treating a persona's self-description as "no restrictions" as itself a jailbreak-intent signal | none | Architect recommendation |
| Requirement to identify the underlying mechanism behind a successful jailbreak rather than patching only its exact wording, and to test against category-equivalent variants | none | Architect recommendation |
| False-positive control requirement: legitimate fiction/hypothetical requests must remain unaffected by jailbreak defenses | none | Architect recommendation |

Note: this skill deliberately does not reproduce specific historical jailbreak prompt text (e.g. the DAN prompt variants or the simulated-program payload documented in the source), since doing so would function as a reusable circumvention script rather than a defensive resource. Categories and mechanisms are described at the level needed to design and test defenses.
