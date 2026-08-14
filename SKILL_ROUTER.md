# Skill Router

How to pick the right skill for a problem. Three layers, in order of how
people actually arrive with a problem: an architectural fork for building
something new, a symptom table for someone describing a failure, and
pre-composed chains for building a full system.

Read this when unsure which skill applies. Individual skills' own
`When to Use` / `When NOT to Use` sections are the authoritative detail;
this file exists to get to the right one fast.

---

## Layer 1: Architectural Gate

Start here when building something new, before any specific symptom exists.

```
Does the model already know how to answer, given a well-written prompt?
├── Yes → prompt-design
└── No, it needs something external
     │
     ├── Private, large, or changing knowledge (documents, a knowledge base)
     │        → rag-architecture-design
     │
     ├── Live external information or an action on another system
     │        → function-calling-and-tool-design (define the tool)
     │           then agentic-system-design (decide the control structure)
     │
     └── Dynamic planning where the steps can't be listed in advance
              → agentic-system-design

Is the task structured (extract/classify/QA/summarize) rather than open-ended?
└── Yes → structured-output-and-extraction

Does the task decompose into stages, or need to stay fully autonomous?
├── Fixed, enumerable stages → prompt-chaining-and-workflows
└── Steps depend on runtime discoveries → agentic-system-design (agent, not workflow)

Will this system read content the developer doesn't fully control
(user input beyond a simple query, documents, tool results, web pages)?
└── Yes, always pair whatever you built above with → prompt-injection-defense
```

---

## Layer 2: Symptom Table

The more common entry point: someone describes a problem, not a solution.
Match the symptom, not the guessed cause.

| Symptom | Skill |
|---|---|
| "Output isn't consistent between runs" (single prompt, no multi-step reasoning) | `prompt-design` |
| "Output isn't consistent" and the task is genuinely multi-step or arithmetic | `reasoning-and-deliberation` |
| "The model ignores part of my instruction" | `prompt-design` |
| "I've reworded this three times and it's still not working" | `few-shot-prompting` |
| "It gets confused halfway through" / "skips steps" | `reasoning-and-deliberation` |
| "Wrong despite a confident-sounding explanation" | `reasoning-and-deliberation` |
| "It makes things up" / hallucinates facts | `factuality-and-hallucination-control` |
| "It won't say 'I don't know'" | `factuality-and-hallucination-control` |
| "It answers from memory instead of my documents" (RAG exists) | `rag-retrieval-and-grounding` |
| "It doesn't know our internal stuff" (no RAG yet) | `rag-architecture-design` |
| "Retrieved chunks aren't relevant to the query" | `rag-retrieval-and-grounding` (if index exists) or `rag-architecture-design` (if not) |
| "How do I know if our RAG is actually good?" | `rag-evaluation` |
| "Answer quality decays as the conversation grows" | `context-engineering` |
| "Constraints from early in the conversation get forgotten" | `context-engineering` |
| "It calls the wrong tool" / "bad arguments" | `function-calling-and-tool-design` |
| "The tool call is right but results are still bad" | `rag-retrieval-and-grounding` |
| "Should this be an agent or a fixed pipeline?" | `agentic-system-design` |
| "The agent loops" / "doesn't adapt after a bad result" | `react-agent` |
| "One prompt is doing extract-then-verify-then-summarize and failing" | `prompt-chaining-and-workflows` |
| "The JSON/label/format breaks or varies" | `structured-output-and-extraction` |
| "I don't have enough training data, or it's sensitive" | `synthetic-data-generation` |
| "Did this prompt change actually help?" | `prompt-evaluation-and-optimization` |
| "A document uploaded by a user changed the agent's behavior" | `prompt-injection-defense` |
| "It printed its own system prompt / leaked its instructions" | `prompt-injection-defense` |
| "Users get it to break its own rules by claiming a persona" | `jailbreak-resistance` |
| "Someone reframed a disallowed request as fiction/hypothetical and it worked" | `jailbreak-resistance` |

If a symptom seems to fit two rows, check whether the source of the
problem is external content (→ `prompt-injection-defense`) or the user
themselves reframing a request (→ `jailbreak-resistance`); these are the
most commonly conflated pair, and both may legitimately apply together.

---

## Layer 3: Composed Chains

Pre-built sequences for full systems, in the order each skill is actually
invoked during design.

**Building a RAG system:**
```
prompt-design → context-engineering → rag-architecture-design
→ rag-retrieval-and-grounding → prompt-injection-defense → rag-evaluation
```

**Building a tool-using agent:**
```
prompt-design → context-engineering → agentic-system-design
→ function-calling-and-tool-design → react-agent
→ prompt-injection-defense → jailbreak-resistance → prompt-evaluation-and-optimization
```

**Building a multi-stage structured pipeline (no autonomy needed):**
```
prompt-design → structured-output-and-extraction
→ prompt-chaining-and-workflows → prompt-evaluation-and-optimization
```

**Preparing training data with no autonomous system involved:**
```
prompt-design → prompt-chaining-and-workflows (if generation is iterative)
→ synthetic-data-generation → prompt-evaluation-and-optimization (to validate the data's downstream effect)
```

**Hardening any deployed system before shipping:**
```
prompt-injection-defense (any external content) + jailbreak-resistance (any
direct user access) + factuality-and-hallucination-control (any factual
claims) — apply all three that are relevant, not just one.
```

`prompt-injection-defense` is not optional in any chain that reads external
content. This is enforced identically in every skill's own `When NOT to Use`
section that touches external content, not only here.

## Common misroutes worth naming

- **Landing on `synthetic-data-generation` when you meant `rag-architecture-design`, or vice versa.** The first prepares training data for a retriever; the second builds the production index. A request that mentions both retriever fine-tuning and indexing needs both, not one instead of the other.
- **Landing on `function-calling-and-tool-design` when the tool is being called correctly but its results are just low-quality.** That's `rag-retrieval-and-grounding`, not a tool-definition problem.
- **Landing on `prompt-design` for a task that's actually reasoning-bound.** If three rewording attempts haven't fixed it and the task involves computation or multi-step logic, that's `reasoning-and-deliberation`, not a fourth reword.
- **Landing on `jailbreak-resistance` for content injected from outside the conversation.** Source matters more than framing: if the adversarial text arrived via a document, tool result, or web page, it's `prompt-injection-defense` even if it uses a fictional or hypothetical frame.
