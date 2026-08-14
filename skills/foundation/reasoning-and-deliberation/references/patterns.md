# Deliberation Patterns

## Contents
1. Zero-shot chain-of-thought
2. Demonstrated reasoning
3. Generated knowledge
4. Code delegation
5. Self-consistency
6. Branch exploration
7. Self-critique
8. Trade-off table

## 1. Zero-shot chain-of-thought

```
Solve the problem below. Work through it step by step inside <reasoning>,
then give only the final result inside <answer>.

<problem>{problem}</problem>
```
Cheapest option. Try it before anything else. It helps most on tasks with a few dependent steps and helps least on single-lookup tasks.

## 2. Demonstrated reasoning

Show the steps in the examples, not only the answers.

```
Q: A shop had 23 units, sold 7 on Monday and 9 on Tuesday. How many remain?
A: Start with 23. Sold 7, leaving 16. Sold 9 more, leaving 7. Answer: 7
```
Use when the model's reasoning pattern is wrong rather than absent. Two or three examples are usually enough; see `few-shot-prompting` for selection rules.

## 3. Generated knowledge

Two calls. First elicit relevant facts, then answer conditioned on them.

```
Call 1: List the facts relevant to deciding {question}. Facts only, no conclusion.
Call 2: Using the facts below, answer {question}.
        <facts>{output of call 1}</facts>
```
Use when the model has the knowledge but does not surface it unprompted, typically on commonsense or domain questions where it answers too fast. If the knowledge is genuinely absent, this pattern manufactures plausible-sounding facts; go to `rag-architecture-design` instead.

## 4. Code delegation

```
Write Python that computes the answer. Do not compute it yourself.
Print only the final result.
```
Execute, then use the printed result. Use for arithmetic, dates, sorting, set operations, unit conversion, and parsing. Prose reasoning over exact computation stays unreliable regardless of how carefully it is prompted, because token-level generation is not calculation.

Requires an interpreter. Without one, state the limitation rather than approximating.

## 5. Self-consistency

Sample N reasoning paths at temperature above zero, take the majority final answer.

```
N = 3 for a cheap stability check
N = 5 to 7 when accuracy matters and cost allows
```
Only for questions with one correct answer. On open-ended tasks majority voting collapses to the blandest option. At temperature 0 the samples are near-identical and the cost buys nothing.

Useful side effect: the spread across paths is a usable confidence signal. Unanimous is confident, split is worth escalating.

## 6. Branch exploration

Generate 3 candidate approaches, score each against explicit criteria, expand the best, and backtrack if it fails.

```
Step 1: Propose 3 distinct approaches to {problem}.
Step 2: Score each on {criteria}, 1 to 5, with a reason.
Step 3: Expand the highest scorer into a full solution.
Step 4: If it fails validation, return to Step 3 with the next scorer.
```
Expensive. Justified when early choices constrain everything after them, such as architecture selection or planning under constraints. Requires a scoring function; without one it is sampling with extra steps.

## 7. Self-critique

```
Draft → critique against explicit criteria → revise once
```
The criteria must be explicit and external. "Improve this" produces cosmetic edits. "Check each claim against the source, flag unsupported ones" produces useful ones. Cap at one or two revision rounds; further rounds tend to drift rather than improve.

For factual self-checking specifically, go to `factuality-and-hallucination-control`.

## 8. Trade-off table

| Pattern | Calls | Latency | Best for | Fails on |
|---|---|---|---|---|
| Zero-shot CoT | 1 | Low | Few dependent steps | Exact computation |
| Demonstrated reasoning | 1 | Low | Wrong step pattern | Novel problem shapes |
| Generated knowledge | 2 | Medium | Unsurfaced knowledge | Knowledge the model lacks |
| Code delegation | 1 plus execution | Medium | Anything computable | No interpreter available |
| Self-consistency | N | High | Unstable deterministic answers | Open-ended tasks |
| Branch exploration | Many | Highest | Early choices dominate | No scoring function |
| Self-critique | 2 to 3 | Medium | Judged quality | Vague criteria |
