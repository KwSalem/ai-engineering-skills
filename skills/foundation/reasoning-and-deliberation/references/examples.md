# Reasoning Examples

## Simple: escalating one level

Task: word problems with two dependent steps. Baseline accuracy 6 of 10.

Level 1 applied, asking for steps before the answer inside a fenced block: 9 of 10. Stop here. Levels 2 and above would add cost for a gap that no longer exists.

Recorded: baseline 60 percent, level 1 90 percent, latency plus 0.4 seconds. That record is what makes the choice defensible later.

## Realistic: reasoning that was rationalizing

Task: pick the compliant option among four vendor quotes under several constraints. Answers were fluent, well-argued, and wrong about a third of the time.

Trace inspection showed the pattern: the model picked a favourite early, then wrote reasoning supporting it, silently dropping one constraint. Final-answer grading never caught this, because the wrong answers were argued as well as the right ones.

Fix in two parts:
1. Force the intermediate structure before any conclusion. A constraint-by-option table, filled first.
2. Delegate the elimination to code, since constraint filtering is exactly computable.

```
Step 1: For each option, output a row: option, constraint_1_met, ..., total_cost.
Step 2: Write Python that filters rows where all constraints are met and sorts by cost.
Step 3: Report the top row and name any option eliminated, with the failing constraint.
```
Accuracy went to 10 of 10 and, more usefully, failures became visible in the table rather than hidden in prose.

## Edge case: reasoning correctly removed

Task: classify support tickets into five categories. The prompt carried "think step by step" inherited from an earlier template.

Measured: with reasoning 92 percent accuracy, 2.1 seconds per call. Without reasoning 93 percent, 0.6 seconds. Deliberation was pure overhead, and it had been there for months because nobody measured it.

This is why Step 2 requires a baseline. Reasoning is presumed useful until measured; the presumption is often wrong on classification, extraction, and lookup.

## Edge case: self-consistency misapplied

Task: draft a project risk summary. Self-consistency with N of 5 was applied hoping for better quality.

Result: the majority vote selected the most generic phrasing every time, because generic content is what several independent drafts converge on. Cost was 5 times higher and the output was worse than a single draft.

Rule confirmed: self-consistency needs one correct answer to vote on. For open-ended output, use self-critique instead.
