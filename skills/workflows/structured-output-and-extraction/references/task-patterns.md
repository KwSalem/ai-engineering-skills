# Structured Task Patterns

## Contents
1. Extraction worked example
2. Classification: naming vs. showing the fix
3. QA with grounding and abstention
4. Summarization at different lengths
5. Combining task types

## 1. Extraction worked example

Task: extract model names from ML paper abstracts.

```
Your task is to extract model names from machine learning paper abstracts.
Your response is an array of the model names in the format ["model_name"].
If you don't find model names in the abstract or you are not sure, return ["NA"]

Abstract: Large Language Models (LLMs), such as ChatGPT and GPT-4, have
revolutionized natural language processing research...
```

Output: `["ChatGPT", "GPT-4"]`

The explicit `["NA"]` fallback matters more than it looks: without it, an abstract with no model names produces unpredictable output, sometimes an empty array, sometimes an invented placeholder, sometimes a refusal-style sentence instead of the array format at all. One line of defined behavior for the empty case removes an entire category of downstream parsing failures.

## 2. Classification: naming vs. showing the fix

Weak:
```
Classify the text into neutral, negative or positive.

Text: I think the food was okay.
Sentiment:
```
Output: `Neutral` — correct content, wrong case if the downstream system expects lowercase.

Better, format shown via one example:
```
Classify the text into neutral, negative or positive.

Text: I think the vacation is okay.
Sentiment: neutral

Text: I think the food was okay.
Sentiment:
```
Output: `neutral` — the single labelled example fixed the casing mismatch that an instruction alone didn't.

This illustrates the parent skill's Decision Rule directly: the task was already being understood correctly (both outputs correctly identify neutral sentiment), the failure was purely in output format, and the fix that worked was format demonstration, not task re-explanation.

## 3. QA with grounding and abstention

```
Answer the question based on the context below. Keep the answer short and
concise. Respond "Unsure about answer" if not sure about the answer.

Context: Teplizumab traces its roots to a New Jersey drug company called
Ortho Pharmaceutical. There, scientists generated an early version of the
antibody, dubbed OKT3. Originally sourced from mice, the molecule was able
to bind to the surface of T cells and limit their cell-killing potential.

Question: What was OKT3 originally sourced from?

Answer:
```
Output: `Mice.`

The value of the explicit "Unsure about answer" instruction shows up specifically when the context genuinely doesn't cover the question, for example asking this same prompt "What year was OKT3 approved in the EU?" when the context only discusses US approval. Test QA prompts specifically against a question the context can't answer, not only against questions it can; a prompt that performs perfectly on answerable questions can still fail silently on unanswerable ones if abstention was never explicitly tested.

## 4. Summarization at different lengths

Same source, two different length/focus instructions producing appropriately different results:

```
Explain antibiotics

A:
```
Produces a full paragraph explanation, appropriate when no length constraint is needed.

```
{paragraph explaining antibiotics}

Explain the above in one sentence:
```
Produces: "Antibiotics are medications used to treat bacterial infections by either killing the bacteria or stopping them from reproducing, but they are not effective against viruses and overuse can lead to antibiotic resistance."

Note what the one-sentence version had to do: compress cause (what antibiotics are), mechanism (how they work), and caveat (limitations) into a single sentence. A vaguer instruction like "make this shorter" gives the model no signal about which of these three elements to prioritize if all three can't fit, producing inconsistent choices across runs. Stating the focus alongside the length, when the source covers more ground than the target length allows, resolves this ambiguity directly.

## 5. Combining task types

Real tasks often combine two of these patterns in one prompt: extract-then-classify, or QA-with-a-forced-format. When combining, apply each pattern's specific guidance to its part of the prompt rather than treating the combination as a new, undocumented task type: an extract-and-classify prompt needs both defined missing-field behavior (extraction) and a fixed label set with exact format (classification), not a single blended instruction that under-specifies both. If the combination starts feeling like it's doing too much in one prompt, this is also a signal to check `prompt-chaining-and-workflows`: splitting extraction and classification into two stages, each individually well-specified per this skill's guidance, often outperforms one prompt straining to do both at once.
