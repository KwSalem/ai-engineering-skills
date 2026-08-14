# Prompt Chaining Examples

## Contents
1. Worked example: document question answering
2. Debugging walkthrough
3. When two stages should have been one, and vice versa

## 1. Worked example: document question answering

A common two-stage chain for answering a question about a large document:

**Stage 1 (extraction):**
```
You are a helpful assistant. Your task is to help answer a question given
in a document. First, extract quotes relevant to the question from the
document, delimited by ####. Output the list of quotes using
<quotes></quotes>. Respond with "No relevant quotes found!" if none exist.

####
{document}
####
```

**Stage 2 (composition):**
```
Given a set of relevant quotes (delimited by <quotes></quotes>) extracted
from a document and the original document (delimited by ####), compose an
answer to the question. Ensure the answer is accurate, has a friendly tone,
and sounds helpful.

####
{document}
####

<quotes>
{stage 1 output}
</quotes>
```

Why this split works: stage 1's only job is finding relevant material, which it can do without worrying about tone or phrasing. Stage 2's only job is composing a good answer, which it can do without re-scanning the whole document for relevance. Each prompt is simpler and more reliable than a single prompt asked to both find and compose at once, and if the final answer is wrong, checking stage 1's extracted quotes immediately shows whether the problem was finding the right material or writing about it.

## 2. Debugging walkthrough

Symptom: the final answer from the two-stage chain above cites information that isn't in the document.

Debugging by isolating the stage (Step 5 of the parent skill): run stage 1 alone and inspect its quotes. Two possible findings:

- **Stage 1's quotes are accurate but stage 2 added claims not in them.** The problem is in stage 2's composition; the fix is tightening stage 2's instruction (e.g., adding "only use information present in the quotes above, do not add outside knowledge").
- **Stage 1 itself extracted something not actually in the document, or extracted nothing relevant and stage 2 filled the gap.** The problem is upstream; the fix belongs in stage 1, and no amount of tightening stage 2 will fix a fabrication rooted in bad extraction.

Without running the stages separately, both symptoms look identical from the final output alone: an answer with unsupported claims. This is the concrete value chaining provides over a single monolithic prompt, where this kind of isolation isn't possible at all.

## 3. When two stages should have been one, and vice versa

**Over-split example:** a chain with a stage for "extract the customer's name" and a separate stage for "extract the customer's order number," each a full round trip. If both pieces of information are always needed together and neither depends on the other's result, this is unnecessary latency; one extraction stage returning both fields is simpler and just as reliable.

**Under-split example:** a single stage asked to "extract the key facts, resolve any contradictions between sources, and write a two-paragraph summary." Contradiction resolution is a distinct reasoning task from extraction, and summarization has its own tone and length concerns. When this stage's quality is inconsistent, the fix is usually not a better single prompt, but splitting the contradiction-resolution step out so it can be validated (Step 3) before summarization ever sees the resolved facts.

The general test from Step 1 applies to both directions: could each proposed stage be handed to someone with no context on the others, and would that be enough for them to do their part correctly? If a stage fails that test because it needs to know about a sibling stage's internals, the split is probably wrong.
