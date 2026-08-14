# Prompt Optimization Methods

## Contents
1. Automatic Prompt Engineer (APE)
2. Meta-prompting in depth
3. Exemplar order and distribution effects
4. Other optimization directions worth knowing

## 1. Automatic Prompt Engineer (APE)

APE frames instruction generation as a black-box search problem: an inference model proposes candidate instructions from a set of output demonstrations, each candidate is executed against a target model, and the highest-scoring candidate (by an evaluation metric appropriate to the task) is selected. This is systematic search, not hand-tuning: instead of a person iterating on wording by intuition, multiple candidates are generated and scored empirically.

Notable result: APE-discovered zero-shot chain-of-thought instructions outperformed the well-known hand-written "Let's think step by step," landing on "Let's work this out in a step by step way to be sure we have the right answer," which improved performance on math benchmarks (MultiArith, GSM8K) over the original phrasing. This illustrates the core value of the approach: human intuition about good phrasing is a reasonable starting point, not a ceiling, and systematic search can find phrasings a person wouldn't have tried.

Related directions in the same space, useful to know exist even without going deep on each: offline inverse reinforcement learning for query-dependent prompts (Prompt-OIRL), using an LLM to iteratively refine prompts with instructions like "take a deep breath" shown to help on math problems (OPRO), gradient-guided automatic prompt search (AutoPrompt), and lighter-weight alternatives to full fine-tuning like prefix tuning and soft prompt tuning that optimize a continuous representation rather than natural-language wording.

## 2. Meta-prompting in depth

Meta-prompting shifts emphasis from content-specific examples to the structural and syntactic pattern of a problem class. Where few-shot prompting shows fully worked examples (specific numbers, specific entities), meta-prompting shows the shape of the problem and solution: the pattern of steps, the type of answer expected, without committing to particular content.

Reported advantages over few-shot prompting for structurally repetitive problem classes:
- **Token efficiency**: abstracted structure costs fewer tokens than several fully worked examples.
- **Fairer comparison**: minimizes the influence of which specific examples happened to be chosen, useful when comparing different models or methods on the same problem class.
- **Zero-shot-like behavior**: since specific content examples are minimized, meta-prompting behaves similarly to zero-shot prompting in how much it leans on the model's own domain knowledge.

That last point is also its main limitation: meta-prompting assumes the model already has reliable knowledge of the task domain. On a genuinely novel or unusual task, the lack of concrete worked examples means performance can degrade the same way zero-shot prompting degrades on unfamiliar tasks. It fits well for complex reasoning, math problem-solving, coding challenges, and theoretical queries where the model's underlying competence is not in question and the goal is guiding its application of that competence, not teaching it new content.

## 3. Exemplar order and distribution effects

Two effects worth controlling for during evaluation, both documented empirically:

- **Distribution of exemplars**: on some tasks, an unbalanced label distribution among few-shot examples doesn't visibly bias the model; on harder, more ambiguous classification tasks, it can. The effect is task-dependent, which is precisely why it needs to be tested rather than assumed either way for a specific prompt.
- **Order of exemplars**: the sequence in which few-shot examples appear can shift model behavior independent of their content, particularly when labels are clustered rather than shuffled.

Practical implication for this skill: when comparing two prompt variants that both use few-shot examples, a difference in exemplar order or distribution between the variants is a confound. If it isn't controlled, an observed score difference can't be confidently attributed to the wording change actually being tested.

## 4. Other optimization directions worth knowing

Beyond APE and meta-prompting, the broader prompt-optimization space includes techniques that operate below the natural-language layer: continuous prompt tuning methods that learn embeddings rather than words, and reinforcement-learning-based approaches that optimize prompts against a downstream reward signal. These require more infrastructure (gradient access, a training loop) than most prompt-evaluation work needs, and are worth reaching for only once natural-language-level optimization (Steps 1-6 of the parent skill) has been exhausted and the task's value justifies the added investment.
