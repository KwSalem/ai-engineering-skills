# Prompt Elements

## Contents
1. The six slots
2. Ordering
3. Delimiter choice
4. System prompt vs user prompt
5. Settings reference

## 1. The six slots

| Slot | Question it answers | Include when | Common fault |
|---|---|---|---|
| Role | Who is speaking | Perspective or register changes the answer | Decorative roles that change nothing |
| Instruction | What action to perform | Always | Two actions in one instruction |
| Context | What background is needed | The model cannot be assumed to know it | Dumping background that is never used |
| Input data | What to operate on | There is content to process | Not delimited from the instruction |
| Constraints | What bounds apply | Length, tone, scope, or exclusions matter | Only negative constraints |
| Output format | What shape to return | Always, unless prose is genuinely fine | Named rather than shown |

Not every prompt needs all six. It needs a conscious decision about all six.

## 2. Ordering

Default order that survives most models:

```
[Role]
[Instruction]
[Constraints]
[Context]
###
[Input data]
###
[Output format + filled example]
```

Reasons for this order:
- Instruction first, because attention to the opening is strongest and it is the part most often dropped when buried.
- Input late and fenced, so nothing after it can be mistaken for an instruction.
- Output format last, closest to generation, so it is the freshest constraint.

When input is very long, repeat the instruction after the input. Long inputs push the opening instruction far from the generation point and adherence degrades.

## 3. Delimiter choice

| Delimiter | Use for |
|---|---|
| XML-like tags `<document>` | Multiple distinct inputs that must be told apart |
| `###` blocks | A single input block |
| Triple quotes | Short quoted strings |

Choose one convention per prompt and never nest the same marker inside itself. If the input can contain your delimiter, pick a delimiter it cannot contain and say so in the instruction.

## 4. System prompt vs user prompt

- System prompt: durable identity, standing rules, tool policy, refusal policy, output conventions. Content that is true for every turn.
- User prompt: this task, this input, this format.

Rule of thumb: if it changes per request, it does not belong in the system prompt. Putting per task detail in the system prompt is a common cause of stale instructions surviving into later turns.

For allocating the whole window across system prompt, tools, retrieved context, memory, and history, go to `context-engineering`.

## 5. Settings reference

| Setting | Effect | Guidance |
|---|---|---|
| temperature | Flattens or sharpens the token distribution | Near 0 for deterministic tasks, higher for variety |
| top_p | Truncates the distribution by cumulative probability | Alternative to temperature, not a companion |
| max tokens | Hard output ceiling | Set it; an unbounded ceiling hides runaway output |
| stop sequences | Ends generation on a marker | Useful when the format has a natural terminator |

Adjusting temperature and top_p together makes results unattributable. Move one at a time.
