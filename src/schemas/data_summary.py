from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class CampaignDailyMetrics(BaseModel):
    date: str
    spend: float
    impressions: int
    clicks: int
    ctr: float
    purchases: int
    revenue: float
    roas: float

class CreativeInfo(BaseModel):
    creative_message: str
    ctr: float
    revenue: float

class DataSummary(BaseModel):
    total_spend: float
    total_impressions: int
    total_clicks: int
    avg_ctr: float
    total_purchases: int
    total_revenue: float
    avg_roas: float

    campaign_daily: Dict[str, List[CampaignDailyMetrics]] = Field(
        default_factory=dict,
        description="Daily metrics grouped by campaign"
    )

    top_creatives: List[CreativeInfo] = Field(
        default_factory=list,
        description="Top creatives ranked by CTR or revenue"
    )

    audience_breakdown: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="CTR/ROAS by audience_type"
    )

    platform_breakdown: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="CTR/ROAS by platform"
    )
