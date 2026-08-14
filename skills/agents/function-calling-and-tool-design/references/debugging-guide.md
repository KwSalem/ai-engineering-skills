# Function Calling Debugging Guide

## Contents
1. The function calling flow in full
2. The action/observation loop
3. Worked debugging trace
4. Failure signature table

## 1. The function calling flow in full

1. **User query**: the request arrives, e.g. "What is the weather in Paris?"
2. **Context assembly**: the system message, tool definitions, and user message combine into the full context sent to the model.
3. **Tool decision**: the model analyzes the context and decides whether a tool call is needed; if so, it outputs a structured call naming the tool and its arguments.
4. **Tool execution**: the developer's code receives the call and actually executes the function.
5. **Observation**: the tool's return value becomes the observation.
6. **Response generation**: the observation is passed back to the model along with the full prior context, and the model produces the final response.

The model retains full context of everything that happened in the exchange throughout this flow; that persistent context awareness is what lets it incorporate a tool's result intelligently into a coherent final answer, rather than treating the tool call as a disconnected side effect.

## 2. The action/observation loop

For agents that may need more than one tool call to answer, the loop repeats:

```
Action: agent decides to call a tool
Environment: the tool executes and returns a result
Observation: the agent receives and processes that result
Decision: call another tool, or respond to the user
```

Each observation becomes part of the context for the next iteration, so the agent's later decisions are grounded in what it has already learned, not just the original request. This is also why a single bad observation early in a multi-call task can derail the rest of the loop: everything downstream is conditioned on it.

## 3. Worked debugging trace

Query: "Latest news from OpenAI"

```
Agent thinks: I need current information about OpenAI news.
              I should use the web_search tool.

Action: web_search(query="OpenAI latest news announcements")

Observation: [Search results with recent OpenAI articles...]

Agent thinks: I now have the information needed to answer.
              Let me summarize these results for the user.

Response: "Here are the latest updates from OpenAI..."
```

To debug a failure in a flow like this, get the intermediate steps, not just the final response. A trace worth inspecting includes: which tools were called and in what order, the exact arguments passed to each, what each tool actually returned, and token usage per step if cost is also a concern. Many workflow platforms expose this under a setting like "return intermediate steps"; when the platform abstracts it away, get as close to the raw API calls as the tooling allows before concluding the model itself is at fault.

## 4. Failure signature table

| Symptom in the trace | Likely cause | Where to fix |
|---|---|---|
| Wrong tool name in the action | Descriptions too similar or too vague to disambiguate | Sharpen the tool descriptions (Step 2) |
| Malformed or incomplete arguments | Parameter description lacks constraints or examples | Add enums or concrete examples to that parameter (Step 3) |
| No tool called when one was needed | Description doesn't mention the triggering scenario | Add the missing trigger to the description, reinforce in system prompt (Step 2, Step 4) |
| Tool called correctly, final answer still wrong | Observation misinterpreted, not a tool-selection problem | Check how the observation is being incorporated into generation, separate from tool selection |
| Tool called repeatedly with the same failing arguments | Error message from the tool gives no actionable guidance | Rewrite the tool's failure return to suggest a concrete next step |
| Correct tool, but only after several wrong attempts | The tool set has scope overlap the model is resolving by trial and error | Disambiguate overlapping tools explicitly rather than letting selection stay probabilistic |
