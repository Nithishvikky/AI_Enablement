import pandas as pd
from agentevals.trajectory.llm import create_trajectory_llm_as_judge, TRAJECTORY_ACCURACY_PROMPT
from langchain.messages import HumanMessage, AIMessage

from agent import create_agent_function
from eval_dataset import EVAL_DATASET

REPORT_FILE = "AGENT_EVAL_REPORT.md"

def generate_markdown_report(df: pd.DataFrame):
    accuracy = df["correct"].mean()
    avg_latency = df["latency_sec"].mean()
    hallucination_rate = 1 - accuracy
    tool_usage_success = df["tool_used_correctly"].mean()

    markdown = f"""
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
| Accuracy | {accuracy:.2%} |
| Average Latency (sec) | {avg_latency:.2f} |
| Hallucination Rate | {hallucination_rate:.2%} |
| Tool Usage Success | {tool_usage_success:.2%} |

---

## Per-Prompt Results

| Input | Final Output | Correct | Latency (sec) | Tool Used |
|------|------------|--------|---------------|-----------|
"""

    for _, row in df.iterrows():
        markdown += (
            f"| {row['input']} "
            f"| {row['final_output']} "
            f"| {row['correct']} "
            f"| {row['latency_sec']:.2f} "
            f"| {row['tool_used_correctly']} |\n"
        )

    with open(REPORT_FILE, "w") as f:
        f.write(markdown)

    print(f"\nMarkdown report generated: {REPORT_FILE}")


def run_agent_eval():

    # Initialize your Bedrock + Guardrails agent
    agent = create_agent_function()

    # Create AgentEval evaluator
    evaluator = create_trajectory_llm_as_judge(  
        model="anthropic.claude-3-5-sonnet-20240620-v1:0",  
        prompt=TRAJECTORY_ACCURACY_PROMPT,  
    )

    rows = []

    for example in EVAL_DATASET:
            print(f"\nEvaluating: {example['input']}")


            # Run your agent
            response = agent.invoke(
                {"messages": [{"role": "user", "content": example["input"]}]}
            )

            latency = response['messages'][1].response_metadata['metrics']['latencyMs'][0]
            messages = response["messages"]
            final_output = messages[-1].content

            print(f"\nOutput: {final_output}")

            eval_result = evaluator(outputs=messages)

            reference_trajectory = [
                HumanMessage(content=example["input"]),
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "id": "ref_call_1",
                            "name": example["tool_type"],
                            "args": {},
                        }
                    ],
                ),
            ]

            tool_eval = evaluator(
                outputs=messages,
                reference_outputs=reference_trajectory,
            )

            rows.append({
                "input": example["input"],
                "correct": bool(eval_result["score"]),
                "latency_sec": latency,
                "tool_used_correctly": bool(tool_eval["score"]),
                "final_output":final_output
            })

    df = pd.DataFrame(rows)
    generate_markdown_report(df)

    return df


if __name__ == "__main__":
    run_agent_eval()
