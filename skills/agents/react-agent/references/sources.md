# Sources: react-agent

Repository: github.com/dair-ai/Prompt-Engineering-Guide

| Claim | Source | Type |
|---|---|---|
| ReAct interleaves reasoning traces and task-specific actions, letting the model induce, track, and update action plans while interfacing with external sources | `pages/techniques/react.en.mdx` (introduction) | Source-derived |
| ReAct outperforms baselines on language and decision-making tasks and improves interpretability and trustworthiness | `pages/techniques/react.en.mdx` (introduction) | Source-derived |
| Best approach combines ReAct with chain-of-thought, using both internal knowledge and externally retrieved information | `pages/techniques/react.en.mdx` (introduction, How it Works) | Source-derived |
| CoT alone lacks access to external information, risking fact hallucination and error propagation | `pages/techniques/react.en.mdx` (How it Works) | Source-derived |
| Trajectory exemplars combine Thought/Action/Observation steps as few-shot demonstrations; free-form thoughts serve decomposition, extraction, commonsense/arithmetic reasoning, search guidance, and synthesis | `pages/techniques/react.en.mdx` (ReAct Prompting) | Source-derived |
| Different prompt setups for different task types: dense thoughts for reasoning-primary tasks (e.g. HotpotQA), sparser thoughts for decision-making tasks with many action steps | `pages/techniques/react.en.mdx` (ReAct Prompting) | Source-derived |
| ReAct generally outperforms Act-only; ReAct's structural constraint reduces reasoning flexibility; ReAct is highly dependent on retrieval quality, with uninformative results derailing reasoning | `pages/techniques/react.en.mdx` (Results on Knowledge-Intensive Tasks) | Source-derived |
| Combining ReAct with CoT+Self-Consistency and allowing switching between them outperforms other prompting methods | `pages/techniques/react.en.mdx` (Results on Knowledge-Intensive Tasks) | Source-derived |
| ReAct outperforms Act on decision-making benchmarks (ALFWorld, WebShop); reasoning is advantageous even though performance still lags expert humans | `pages/techniques/react.en.mdx` (Results on Decision Making Tasks) | Source-derived |
| Worked LangChain ReAct example combining a search tool and a calculator tool to answer a compound question | `pages/techniques/react.en.mdx` (LangChain ReAct Usage) | Source-derived |
| Reflexion converts environment feedback into linguistic self-reflection stored as context for the next attempt, improving performance on advanced tasks | `pages/techniques/reflexion.en.mdx` (introduction) | Source-derived |
| Reflexion's three components: Actor (generates trajectory, uses CoT or ReAct), Evaluator (scores the trajectory via reward signal), Self-Reflection (generates verbal feedback stored in memory) | `pages/techniques/reflexion.en.mdx` (component description) | Source-derived |
| Reflexion process: define task, generate trajectory, evaluate, reflect, generate next trajectory; extends ReAct with self-evaluation, self-reflection, and memory | `pages/techniques/reflexion.en.mdx` (process summary) | Source-derived |
| Reflexion suits trial-and-error learning, is a lightweight alternative to fine-tuning-based RL, benefits from nuanced verbal feedback, and provides interpretable episodic memory | `pages/techniques/reflexion.en.mdx` (When to Use Reflexion) | Source-derived |
| Reflexion limitations: depends on the model's self-evaluation ability, sliding-window memory has bounded capacity, code-generation test-driven limitations | `pages/techniques/reflexion.en.mdx` (limitations) | Source-derived |
| Six-step design procedure calibrating thought density to task type and deciding when to add self-reflection | none | Architect recommendation |
| Explicit decision rule tracing loop derailment back to the originating observation rather than the most recent thought | none | Architect recommendation |
| Framing arithmetic tool delegation within a ReAct trajectory as the same principle as code delegation in reasoning-and-deliberation | none, cross-referenced from [[reasoning-and-deliberation]] in this library | Architect recommendation |
