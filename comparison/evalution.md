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
| Code Quality | Claude Sonnet (Bedrock) | excellent | - Clean, readable code - Very low latency |
| Code Quality | DeepSeek R1 7b | good | - Correct logic - Violated code-only rule - Very high latency |
| Code Quality | GPT-4o (Azure) | excellent | - Clean, correct code - Followed constraints well |

| Use Case | Model | Rating | Comments |
|--------|------|--------|---------|
| SQL Generation | Gemini Flash | excellent | - Simple, valid query - Correct ordering and limit |
| SQL Generation | Claude Sonnet (Bedrock) | excellent | - Optimal SQL - Selected correct columns |
| SQL Generation | DeepSeek R1 7b | good | - Correct query - Added explanations despite constraints |
| SQL Generation | GPT-4o (Azure) | excellent | - Clean query - Strictly followed instructions |

| Use Case | Model | Rating | Comments |
|--------|------|--------|---------|
| Infrastructure Automation (Scripts) | Gemini Flash | excellent | - Simple and correct - Handles empty dirs implicitly |
| Infrastructure Automation (Scripts) | Claude Sonnet (Bedrock) | excellent | - Robust script - Explicit empty handling |
| Infrastructure Automation (Scripts) | DeepSeek R1 7b | basic or limited support | - Invalid flags - Script is syntactically broken |
| Infrastructure Automation (Scripts) | GPT-4o (Azure) | excellent | - Clean script - Correct file counting |

| Use Case | Model | Rating | Comments |
|--------|------|--------|---------|
| Ease of Use | Gemini Flash | excellent | - Minimal prompting needed - Follows constraints |
| Ease of Use | Claude Sonnet (Bedrock) | excellent | - Strong instruction adherence - Consistent behavior |
| Ease of Use | DeepSeek R1 7b | good | - Needs strict prompting - Verbose by default |
| Ease of Use | GPT-4o (Azure) | excellent | - Follows rules naturally - Low verbosity |

| Use Case | Model | Rating | Comments |
|--------|------|--------|---------|
| Speed / Latency | Gemini Flash | good | - ~3–6s latency - Acceptable consistency |
| Speed / Latency | Claude Sonnet (Bedrock) | excellent | - ~2–3s latency - Very consistent |
| Speed / Latency | DeepSeek R1 7b | basic or limited support | - 13–25s latency - Very slow and variable |
| Speed / Latency | GPT-4o (Azure) | excellent | - ~2–3s latency - Fast and stable |

---

## Overall Notes
- Claude Sonnet → Best for strict evaluation and production use  
- GPT-4o → Best balance of speed + instruction following  
- Gemini Flash → Strong baseline model, good consistency  
- DeepSeek R1 → Useful for exploration, weak for automation and constraints  
