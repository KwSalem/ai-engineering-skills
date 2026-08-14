# Prompt Injection Attack and Defense Patterns

## Contents
1. What prompt injection is
2. Task hijacking pattern
3. Prompt leaking pattern
4. Defense tactic details
5. Why no single defense is complete

## 1. What prompt injection is

Prompt injection is a vulnerability where a prompt built from a concatenation of trusted instructions and untrusted input causes unexpected or undesired model behavior, because the model has no inherent way to distinguish "instructions I should follow" from "text I should treat as data" once they're combined into one input stream. It has been described as a form of security exploit, by analogy to injection vulnerabilities in traditional software (most directly, SQL injection). The core issue is architectural: without explicit structural separation, instructions and data occupy the same undifferentiated text, and injected text formatted to look like an instruction can be treated as one.

## 2. Task hijacking pattern

The classic demonstration: a translation task is given, followed by embedded text instructing the model to disregard the translation instruction and instead output something unrelated. The model, having no structural signal that the second sentence is untrusted input rather than a continuation of trusted instructions, sometimes follows the injected instruction instead of the original one. The same pattern applies beyond translation: a sentiment classification task followed by injected text asking the model to abandon classification and instead produce harmful or off-task output. The general shape is always: original task, followed by text designed to look like a new instruction that overrides the first.

This is precisely the vulnerability Step 1 (instruction hardening) and Step 2 (delimiting) of the parent skill address directly: hardening tells the model explicitly to disregard override attempts even when it can't structurally tell them apart from real instructions, and delimiting removes the ambiguity by giving the model a structural signal for what counts as data versus instruction.

## 3. Prompt leaking pattern

A related but distinct injection outcome: rather than hijacking the task, the injected text asks the model to reveal the prompt's own contents, including confidential few-shot examples or system instructions that were never meant to be shown to the end user. This matters commercially as much as it matters for safety, since a well-crafted prompt (with tuned examples and instructions) can represent real product IP that a company doesn't want exposed. Testing for this specifically (not just for task hijacking) matters because a system can be fully robust against hijacking while still being vulnerable to leaking, since they exploit the same structural weakness toward different goals.

## 4. Defense tactic details

**Instruction hardening**: adding an explicit clause telling the model that the input may contain attempts to change its behavior and that it should perform the original task regardless. This alone is not a complete solution, but it demonstrably shifts behavior back toward the original task even against an explicit override attempt, and costs only a sentence of prompt budget.

**Delimiting and parameterization**: separating instructions from input structurally, treating them the way parameterized queries treat user input in SQL, rather than as one concatenated string. The trade-off noted in the source material is a potential loss of flexibility; a rigidly parameterized prompt is less adaptable to varied phrasing than a loosely concatenated one, so this is a real design trade-off, not a free structural upgrade.

**Formatting and quoting tricks**: escaping or quoting untrusted input, and requiring a specific structured output format (for example, requiring the response as a named JSON field rather than free text) as an additional layer. These raise the bar against injected text trying to escape a simple delimiter, but are not reported as fully robust either; injected text that mimics the expected structure or escaping convention can still sometimes defeat them, and results have been inconsistent across different formatting choices even for the same underlying idea.

**Avoiding instruction-tuned models for narrow tasks**: using a k-shot prompt on a non-instruction-tuned model, or a model fine-tuned for a specific narrow task, removes some of the general "follow embedded instructions" behavior that injected text exploits. This is not immune either: an attacker can still disrupt the expected example pattern or mimic the demonstration syntax to redirect behavior, and this approach trades away the flexibility that makes instruction-tuned models broadly useful, so it fits narrow, well-defined, high-risk tasks rather than general-purpose systems.

**Adversarial-prompt detector**: a separate model call, given a security-focused persona and told to evaluate whether an incoming prompt is safe to pass to the main system, deciding yes or no with reasoning. This adds a genuinely separate layer of defense that doesn't depend on the main prompt's own robustness, at the cost of an extra call per request. The detector prompt is itself a prompt, and is not inherently immune to injection either.

## 5. Why no single defense is complete

Across all reported defense tactics, a consistent theme holds: prompt injection remains easy to attempt and there is no widely accepted, complete technique to prevent it. Each tactic raises the bar rather than closing the vulnerability outright, and successful defenses against one specific injection phrasing have repeatedly been defeated by minor rephrasing or reformatting of the same underlying attempt. This is why the parent skill treats these as layered defenses to combine, evaluated against realistic testing including paraphrased attack variants, rather than as a checklist where completing all items guarantees safety.
