# Sources: function-calling-and-tool-design

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Function calling enables LLMs to interact with external tools, APIs, and knowledge bases when a query needs information or action beyond training data | `pages/agents/function-calling.en.mdx` (What is Function Calling?) | Source-derived |
| Function calling flow: user query, context assembly, tool decision, tool execution, observation, response generation | `pages/agents/function-calling.en.mdx` (How Function Calling Powers AI Agents) | Source-derived |
| Tool definitions consist of name, description, and parameters; the description is the primary signal for what the tool does and when to use it | `pages/agents/function-calling.en.mdx` (The Role of Tool Definitions) | Source-derived |
| Tool definitions consume tokens on every call and affect cost and latency; be concise but descriptive | `pages/agents/function-calling.en.mdx` (The Role of Tool Definitions) | Source-derived |
| The agent loop: action, environment response, observation, decision, repeating until the agent responds | `pages/agents/function-calling.en.mdx` (The Agent Loop: Actions and Observations) | Source-derived |
| Debugging via intermediate steps: which tools were called, arguments passed, observations received, token usage; common issues include incorrect tool selection, bad arguments, missing context, observation misinterpretation | `pages/agents/function-calling.en.mdx` (Debugging Function Calls) | Source-derived |
| Some platforms abstract away full prompt context; get as close to raw API calls as possible when debugging | `pages/agents/function-calling.en.mdx` (Debugging Function Calls) | Source-derived |
| Best practice: specific descriptions over vague ones (e.g. stating when to use web search, not just that it searches) | `pages/agents/function-calling.en.mdx` (Best Practices for Tool Definitions) | Source-derived |
| Best practice: reinforce tool usage guidance in the system prompt alongside tool definitions, especially to set priority among overlapping tools | `pages/agents/function-calling.en.mdx` (Best Practices for Tool Definitions) | Source-derived |
| Best practice: use enums and examples to constrain parameters | `pages/agents/function-calling.en.mdx` (Best Practices for Tool Definitions) | Source-derived |
| Best practice: tools should return informative error messages enabling recovery, not bare failures | `pages/agents/function-calling.en.mdx` (Best Practices for Tool Definitions) | Source-derived |
| Tool utilization requires understanding not just tool access but when and how to use each tool appropriately | `pages/agents/components.en.mdx` (Tool Utilization) | Source-derived |
| Parallel structure between a tool description's "what + when" requirement and a Skill description's own two-part requirement | none, cross-referenced from this library's own [[CONVENTIONS]] | Architect recommendation |
| Explicit decision rule prioritizing description fixes over parameter fixes based on which failure signature appears in the trace | none | Architect recommendation |
| Failure signature table mapping trace symptoms to fixes | none | Architect recommendation |
| Guidance to treat context-budget pressure from tool definitions as a context-engineering concern rather than solving it by degrading description specificity | none | Architect recommendation |
