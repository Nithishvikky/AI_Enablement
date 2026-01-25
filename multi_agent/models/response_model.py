from pydantic import BaseModel, Field
from typing import List, Optional

class SupportAgentResponse(BaseModel):
    """Unified response format for all support agents (IT & Finance)"""
    answer: str = Field(description="Final answer to the user query")
    sources: List[str] = Field(description="Sources used: internal docs or web URLs")
    tools_used: List[str] = Field(description="List of tools invoked to generate the answer")
    confidence: float = Field(
        description="Confidence in the answer (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )
    latency_ms: float = Field(description="Time taken by the agent in milliseconds")
    notes: Optional[str] = Field(
        description="Optional notes, assumptions, or compliance remarks"
    )

class ClassificationResponse(BaseModel):
    """Structured classification response"""
    classification: str = Field(
        description="The classification of the query: either IT or FINANCE",
        enum=["IT", "FINANCE", "OTHER"]
    )
    confidence: float = Field(
        description="Confidence level of the classification (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )
    reasoning: str = Field(
        description="Brief explanation for the classification"
    )