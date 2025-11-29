from typing import List
from src.utils.llm_client import LLMClient
from src.schemas.data_summary import DataSummary
from src.schemas.creative import CreativeRecommendation
from src.utils.logging_utils import log

class CreativeAgent:
    """
    Generates new creative angles and copy for underperforming campaigns.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.prompt_template = """
        You are a world-class Copywriter for Facebook Ads.
        The following campaign is underperforming (Low CTR/ROAS).
        
        Campaign Data:
        {campaign_data}
        
        Top Performing Creatives (for inspiration):
        {top_creatives}
        
        Task:
        Generate 3 distinct creative variations to improve performance.
        1. One focused on "Social Proof".
        2. One focused on "Urgency/Scarcity".
        3. One focused on "Benefit/Problem-Solution".
        
        Return a structured CreativeRecommendation.
        """

    def generate_creatives(self, data_summary: DataSummary) -> List[CreativeRecommendation]:
        log.info("Generating creative recommendations...")
        
        recommendations = []
        
        # Identify low performing campaigns (e.g., CTR < 1% or ROAS < 2.0)
        # For this MVP, we'll generate for the campaign with the lowest ROAS
        
        if not data_summary.campaign_daily:
            return []

        # Find campaign with lowest average ROAS
        campaign_stats = {}
        for camp, metrics in data_summary.campaign_daily.items():
            total_spend = sum(m.spend for m in metrics)
            total_rev = sum(m.revenue for m in metrics)
            roas = total_rev / total_spend if total_spend > 0 else 0
            campaign_stats[camp] = roas
            
        worst_campaign = min(campaign_stats, key=campaign_stats.get)
        worst_roas = campaign_stats[worst_campaign]
        
        log.info(f"Targeting worst campaign: {worst_campaign} (ROAS: {worst_roas:.2f})")
        
        # Prepare context
        top_creatives_str = "\n".join([f"- {c.creative_message} (Rev: ${c.revenue})" for c in data_summary.top_creatives[:3]])
        
        prompt = self.prompt_template.format(
            campaign_data=f"Campaign: {worst_campaign}, ROAS: {worst_roas:.2f}",
            top_creatives=top_creatives_str
        )
        
        try:
            rec = self.llm.generate_structured(
                prompt=prompt,
                response_schema=CreativeRecommendation,
                system_instruction="You are a creative strategist."
            )
            recommendations.append(rec)
            return recommendations
            
        except Exception as e:
            log.error(f"Creative generation failed: {e}")
            raise
