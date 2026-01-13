# AI Model Comparison Sheet

## Rating Legend
- excellent
- good
- basic or limited support
- not supported

---

## Model Comparison Table

| Use Case | Model | Rating | Comments |
|--------|------|--------|---------|
| Code Quality | Gemini Flash | excellent | - Correct, concise JS - Followed code-only rule - Good latency |
| Code Quality | Claude Sonnet (Bedrock) | excellent | - Clean, readable code - Strict instruction following - Very low latency |
| Code Quality | DeepSeek-R1:7B (Ollama) | good | - Correct logic - Added explanations despite constraints - High latency |
| SQL Generation | Gemini Flash | excellent | - Simple, valid query - Correct ordering and limit |
| SQL Generation | Claude Sonnet (Bedrock) | excellent | - Optimal SQL - Clear column selection |
| SQL Generation | DeepSeek-R1:7B (Ollama) | good | - Correct query - Minimal output this time |
| Infrastructure Automation (Scripts) | Gemini Flash | excellent | - Uses `nullglob` safely - Handles empty dirs cleanly |
| Infrastructure Automation (Scripts) | Claude Sonnet (Bedrock) | excellent | - Robust script - Explicit empty-case handling |
| Infrastructure Automation (Scripts) | DeepSeek-R1:7B (Ollama) | basic or limited support | - Script is syntactically broken - Incorrect file counting |
| Ease of Use | Gemini Flash | excellent | - Minimal prompting needed - Follows constraints |
| Ease of Use | Claude Sonnet (Bedrock) | excellent | - Strong instruction adherence - Consistent behavior |
| Ease of Use | DeepSeek-R1:7B (Ollama) | good | - Needs strict prompting - Verbose by default |
| Speed / Latency | Gemini Flash | good | - ~4–8s latency - Acceptable consistency |
| Speed / Latency | Claude Sonnet (Bedrock) | excellent | - ~2–3s latency - Very consistent |
| Speed / Latency | DeepSeek-R1:7B (Ollama) | basic or limited support | - 7–18s latency - Slow and variable |

---

## Overall Notes
- Claude Sonnet → Best for production and strict evaluations
- Gemini Flash → Strong balance of speed and correctness
- DeepSeek-R1 → Usable for exploration, weak for automation
