# Few-Shot Examples

## Simple: format imitation

Task: normalize free-text dates into ISO form.

```
Input: March 3rd, 2024      Output: 2024-03-03
Input: 3/4/24 (UK format)   Output: 2024-04-03
Input: next Tuesday         Output: UNRESOLVED
Input: {text}               Output:
```

Three examples, and the third is the one doing the real work: it defines behaviour for input the task cannot resolve. Without it the model guesses a date and returns it with the same confidence as a parsed one.

## Realistic: classification with an ambiguous boundary

Task: label incoming maintenance requests as `urgent`, `scheduled`, or `informational`.

Selection:

| Example | Label | Why chosen |
|---|---|---|
| Power out in the whole building | urgent | Clear centre of the class |
| AC noisy, tenant is fine waiting | scheduled | Clear centre of the class |
| Smell of burning, no visible fire | urgent | Boundary case; risk wording without an outage |
| Annual inspection reminder | informational | Third label, otherwise never demonstrated |
| Lift stuck between floors, nobody inside | urgent | Boundary case; sounds severe, no person at risk, still urgent |

Ordering: labels shuffled, never two `urgent` adjacent, the most representative example last.

The two boundary examples carry most of the value. Without them the model splits on how alarming the wording is rather than on the actual rule.

## Edge case: examples that made things worse

Task: multi-step engineering cost estimation. Eight worked examples were added, each showing input and final figure. Accuracy dropped compared with zero-shot.

Reason: the examples demonstrated answers, not method. The model pattern-matched to the nearest example's magnitude instead of computing. This is the trigger in Decision Rules: adding examples degraded performance, so the task is reasoning-bound.

Resolution: remove the answer-only examples and move to `reasoning-and-deliberation`. If examples are kept, they must show the intermediate steps, which makes them demonstrations of a procedure rather than of outputs.

## Edge case: leakage from example to output

Symptom: the model returned content from example 2 when the real input was empty.

Cause: examples and real input shared the same delimiter, so the boundary between the demonstration block and the live input was ambiguous.

Fix: tag the live input distinctly and state the rule explicitly.

```
<examples> ... </examples>
<input_to_process> {text} </input_to_process>

Use <examples> only as a formatting guide. Never take content from it.
```
