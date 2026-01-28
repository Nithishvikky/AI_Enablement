
# LangChain AgentEval Benchmark Report

## Overview
This report documents the benchmark results for the LangChain agent developed.
Evaluation was conducted using **LangChain AgentEval**.

## Metrics Evaluated
- Correctness
- Latency
- Hallucination Rate
- Tool Usage Success

---

## Summary Metrics

| Metric | Value |
|------|------|
| Accuracy | 100.00% |
| Average Latency (sec) | 1352.00 |
| Hallucination Rate | 0.00% |
| Tool Usage Success | 100.00% |

---

## Per-Prompt Results

| Input | Final Output | Correct | Latency (sec) | Tool Used |
|------|------------|--------|---------------|-----------|
| What is 25 * 4 + 10? | 110 | True | 1173.00 | True |
| Convert 'hello world' to uppercase | HELLO WORLD | True | 1137.00 | True |
| How many characters are in 'LangChain'? | 9 | True | 1604.00 | True |
| What is 100 / (5 + 5)? | 10 | True | 1494.00 | True |
