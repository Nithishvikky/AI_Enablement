### Generic prompt
- Basic prompt is too generic and lacks role clarity
- Does not define billing scope like refunds, renewals, downgrades, or incorrect charges
- Provides no structure, constraints, or decision logic
- Results in vague answers and frequent deflection to human support

### Refined prompt
- Refined prompt clearly defines the assistant as a SaaS billing support agent
- Introduces scope limitation to billing and subscription-related issues only
- Adds constraints to avoid guessing or inventing policies
- Enforces structured responses with explanation and next steps
- Produces more accurate, consistent, and actionable billing responses

### COT prompt
- COT enhanced prompt introduces step-by-step reasoning
- Forces the model to identify the billing scenario before answering
- Explicitly applies billing policies during reasoning
- Explains why a decision was made, not just the final answer
- Reduces user confusion and follow-up questions
- Builds higher trust in billing decisions for complex cases