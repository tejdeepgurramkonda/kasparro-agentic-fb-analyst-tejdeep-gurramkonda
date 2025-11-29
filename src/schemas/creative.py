from typing import List
from pydantic import BaseModel, Field

class CreativeVariation(BaseModel):
    headline: str = Field(..., description="New ad headline")
    primary_text: str = Field(..., description="New primary text/caption")
    call_to_action: str = Field(..., description="Recommended CTA button (e.g., 'Shop Now')")
    reasoning: str = Field(..., description="Why this variation is expected to perform better")

class CreativeRecommendation(BaseModel):
    campaign_name: str = Field(..., description="The campaign this recommendation is for")
    current_performance: str = Field(..., description="Summary of why the current creative is failing")
    variations: List[CreativeVariation] = Field(..., description="List of proposed creative variations")
