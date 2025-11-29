from typing import List, Optional, Any
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    metric: str = Field(..., description="The metric used for evidence (e.g., 'CTR', 'ROAS')")
    value: float = Field(..., description="The value of the metric")
    support: bool = Field(..., description="Whether this evidence supports the hypothesis")
    description: str = Field(..., description="Human-readable description of the evidence")

class Insight(BaseModel):
    title: str = Field(..., description="Short title of the insight")
    hypothesis: str = Field(..., description="The proposed explanation for the observation")
    reasoning: str = Field(..., description="Why this hypothesis was generated")
    confidence: float = Field(..., description="Initial confidence score (0.0 to 1.0)")
    audience_segment: Optional[str] = Field(None, description="Specific audience segment if applicable")
    creative_type: Optional[str] = Field(None, description="Specific creative type if applicable")

class ValidatedInsight(Insight):
    is_validated: bool = Field(..., description="Whether the hypothesis was confirmed by data")
    validation_score: float = Field(..., description="Confidence score after validation")
    evidence: List[Evidence] = Field(default_factory=list, description="Quantitative evidence supporting/rejecting")
    actionable_recommendation: str = Field(..., description="What should be done based on this insight")
