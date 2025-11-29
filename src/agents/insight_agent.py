from typing import List
from src.utils.llm_client import LLMClient
from src.schemas.data_summary import DataSummary
from src.schemas.hypothesis import Insight
from src.utils.logging_utils import log

class InsightAgent:
    """
    Analyzes data summaries to generate hypotheses about performance.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.prompt_template = """
        You are an expert Data Analyst for Facebook Ads.
        Analyze the following data summary and generate potential reasons (hypotheses) for the performance trends.
        
        Data Summary:
        {data_summary}
        
        Focus on:
        1. Why ROAS might be dropping or increasing.
        2. Which audiences or platforms are underperforming.
        3. Signs of creative fatigue (high frequency, dropping CTR).
        
        Return a list of structured Insights.
        """

    def generate_insights(self, data_summary: DataSummary) -> List[Insight]:
        log.info("Generating insights from data summary...")
        
        # Convert Pydantic model to JSON string for the prompt
        summary_json = data_summary.model_dump_json(indent=2)
        
        prompt = self.prompt_template.format(data_summary=summary_json)
        
        try:
            # We expect a list of Insights, so we wrap it in a container model or ask for a list
            # For simplicity with the current LLMClient, let's define a wrapper or ask for one object that contains the list.
            # But LLMClient.generate_structured supports generic types if implemented correctly, 
            # or we can define a wrapper model here.
            
            from pydantic import BaseModel
            class InsightList(BaseModel):
                insights: List[Insight]
            
            result = self.llm.generate_structured(
                prompt=prompt,
                response_schema=InsightList,
                system_instruction="You are a sharp, analytical marketing data scientist."
            )
            
            log.info(f"Generated {len(result.insights)} insights.")
            return result.insights
            
        except Exception as e:
            log.error(f"Insight generation failed: {e}")
            raise
