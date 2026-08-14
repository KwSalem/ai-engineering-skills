# Sources: agentic-system-design

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| Agentic systems split into AI workflows (predefined code paths) and AI agents (LLMs dynamically directing their own process and tool use) | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (What Are Agentic Systems?) | Source-derived |
| Workflow characteristics: predefined steps, high predictability, explicit orchestration; fits well-defined tasks needing reliability | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (AI Workflows) | Source-derived |
| Agent characteristics: dynamic decision-making, autonomous tool selection, reasoning/reflection, self-directed execution; fits open-ended tasks with unclear step count | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (AI Agents) | Source-derived |
| Three workflow patterns: prompt chaining (sequential, validation-gated), routing (classify then dispatch to specialized handlers), parallelization (independent concurrent sub-tasks) | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (Common AI Workflow Patterns) | Source-derived |
| Agent core components: tool access, memory, reasoning engine, autonomy | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (AI Agents: Autonomous Task Execution) | Source-derived |
| Workflow vs. agent comparison across control flow, decision making, tool usage, adaptability, complexity, use cases | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (How Agents Differ from Workflows) | Source-derived |
| Design guidance for choosing between workflows and agents, and hybrid approaches combining both | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (Design Considerations) | Source-derived |
| Best practices for workflows (step definition, error handling, validation gates, monitoring) and agents (tool design, memory management, guardrails, observability, iterative testing) | `pages/agents/ai-workflows-vs-ai-agents.en.mdx` (Best Practices) | Source-derived |
| Three fundamental agent capabilities: planning, tool utilization, memory management | `pages/agents/components.en.mdx` | Source-derived |
| Planning enables task decomposition via chain-of-thought, self-reflection, adaptive learning, and critical analysis; imperfect but essential | `pages/agents/components.en.mdx` (Planning) | Source-derived |
| Tool utilization: agent must know when and how to use tools, common tools include code interpreters, search, calculators, image generation | `pages/agents/components.en.mdx` (Tool Utilization) | Source-derived |
| Memory systems: short-term/working memory as an in-context buffer sufficient for most tasks, long-term memory via external vector stores for persistence across sessions | `pages/agents/components.en.mdx` (Memory Systems) | Source-derived |
| Orchestrator and sub-agent architecture, context length management, and sub-agent communication as core design concerns in deeper agent systems | `pages/agents/deep-agents.en.mdx` (Orchestrator & Sub-agent Architecture) | Source-derived |
| Function calling and reasoning are the two key capabilities LLM-based agents rely on to solve complex tasks | `pages/agents/function-calling.en.mdx` (How Function Calling Powers AI Agents) | Source-derived |
| Six-step design procedure (classify, workflow design, agent design, guardrails, orchestrator decision, observability) | none | Architect recommendation |
| Explicit anti-pattern: an LLM step inside a workflow quietly making routing decisions meant to live in code | none | Architect recommendation |
| Decision rule linking cost/latency sensitivity directly to workflow-vs-agent choice | none | Architect recommendation |
| Framing sub-agent splitting as primarily a context-isolation technique, not only a parallelism one | none | Architect recommendation, cross-referenced from [[context-engineering]] in this library |
