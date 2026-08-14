# Sources: context-engineering

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Context engineering covers system prompt, instructions, user input, structured inputs and outputs, tools, RAG and memory, and state or history as distinct components | `pages/guides/context-engineering-guide.en.mdx` | Source-derived |
| Context engineering is iterative, and system prompts and tool descriptions are refined against observed agent failures | `pages/agents/context-engineering-deep-dive.en.mdx` | Source-derived |
| Detailed tool descriptions materially affect agent behaviour | `pages/agents/context-engineering-deep-dive.en.mdx`, `pages/agents/function-calling.en.mdx` | Source-derived |
| Sub-agent communication and context length management are core concerns in multi-agent designs | `pages/agents/context-engineering-deep-dive.en.mdx`, `pages/agents/deep-agents.en.mdx` | Source-derived |
| Memory is a first-class agent component alongside planning and tools | `pages/research/llm-agents.en.mdx`, `pages/agents/components.en.mdx` | Source-derived |
| Context caching as a cost and latency technique | `pages/applications/context-caching.en.mdx` | Source-derived |
| Percentage budget table across segments | none | Architect recommendation |
| Fixed eviction priority order (history, then retrieval, then tools) | none | Architect recommendation |
| Reserved output budget as a hard requirement | none | Architect recommendation |
| Stable-to-volatile ordering for cache reuse | none | Architect recommendation |
| Three-lifetime state model: turn, session, durable | none | Architect recommendation |
| Fixed session summary schema including a rejected-options field | none | Architect recommendation |
| Trust labelling of external segments as a structural requirement | none | Architect recommendation |
| Three-fill pressure test before shipping | none | Architect recommendation |
