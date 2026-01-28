# LangChain Agent with LangFuse, Guardrails-AI, and AgentEval

## Overview

This is a simple LangChain agent instrumented for observability, safety validation, and benchmarking.  
The agent supports tool usage, input/output validation, and offline evaluation with automated report generation.

The task demonstrates:
- Tracing and monitoring of a LangChain agent using LangFuse
- Input and output validation using guardrails-ai
- Agent benchmarking using LangChain AgentEval with markdown reporting

---

## File Structure and Purpose

- `main.py` - Runs the interactive LangChain agent with LangFuse tracing and Guardrails validation.
- `agent.py` - Creates and configures the LangChain Bedrock agent and registers available tools.
- `tools.py` - Defines custom tools used by the agent (calculator, text processing utilities).
- `validators.py` - Implements input and output validation using guardrails-ai, including topic restrictions and toxicity checks.
- `evaluator_llm_as_judge.py` - Runs AgentEval benchmarks, collects metrics, and generates a markdown evaluation report.
- `eval_dataset.py` - Contains the evaluation dataset used for benchmarking agent behavior.

---

## Tools Available to the Agent

- Calculator tool (safe arithmetic expression evaluation)
- Text length counter
- Uppercase text converter

## Technology Integration Summary

### LangFuse
- LangFuse is integrated using the LangChain callback handler.  
- All agent invocations are traced, capturing prompts, responses, token usage, tool calls, and latency.  
- Traces are sent automatically to the LangFuse dashboard for observability and debugging.

### Guardrails-AI
- Guardrails-AI validates both input and output using a toxicity classifier.  
- Restricted topics, greetings, and non-work-related prompts are blocked at input time.  
- Output validation ensures unsafe responses are filtered before returning to the user.

### LangChain AgentEval
- AgentEval is used to evaluate the agent using trajectory-based LLM judging.  
- Metrics such as correctness, latency, hallucination rate, and tool usage success are computed.  
- Results are written to a markdown report for offline review and comparison.



