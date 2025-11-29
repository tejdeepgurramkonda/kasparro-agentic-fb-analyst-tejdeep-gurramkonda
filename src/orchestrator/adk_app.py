import json
import os
from datetime import datetime
from typing import Dict, Any

from src.utils.llm_client import LLMClient
from src.utils.logging_utils import log
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.schemas.plan import Plan
from src.schemas.data_summary import DataSummary

class AgentOrchestrator:
    """
    Orchestrates the flow between Planner, Data, Insight, Evaluator, and Creative agents.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_client = LLMClient()
        
        # Initialize Agents
        self.planner = PlannerAgent(self.llm_client)
        self.data_agent = DataAgent(config['paths']['data_csv'])
        self.insight_agent = InsightAgent(self.llm_client)
        self.evaluator = EvaluatorAgent()
        self.creative_agent = CreativeAgent(self.llm_client)
        
        self.reports_dir = config['paths']['reports_dir']
        os.makedirs(self.reports_dir, exist_ok=True)

    def run(self, user_query: str):
        log.info(f"🚀 Starting Agentic Analysis for: '{user_query}'")
        
        # 1. Planning
        log.info("--- Step 1: Planning ---")
        plan = self.planner.create_plan(user_query)
        
        # 2. Data Loading & Summarization
        log.info("--- Step 2: Data Analysis ---")
        self.data_agent.load_data()
        data_summary = self.data_agent.get_summary() # Can be filtered based on plan if needed
        
        # 3. Insight Generation
        log.info("--- Step 3: Insight Generation ---")
        insights = self.insight_agent.generate_insights(data_summary)
        
        # 4. Evaluation
        log.info("--- Step 4: Evaluation ---")
        validated_insights = []
        for insight in insights:
            val_insight = self.evaluator.validate(insight, data_summary)
            validated_insights.append(val_insight)
            log.info(f"Insight '{val_insight.title}' validated with score: {val_insight.validation_score}")

        # 5. Creative Recommendations (if needed)
        log.info("--- Step 5: Creative Recommendations ---")
        # Check if we have low performing campaigns that need creative help
        creatives = []
        if any(i.validation_score > 0.6 and "creative" in i.hypothesis.lower() for i in validated_insights):
            log.info("Creative issues detected. Generating recommendations...")
            creatives = self.creative_agent.generate_creatives(data_summary)
        else:
            log.info("No strong creative signals detected, skipping creative generation.")

        # 6. Reporting
        self._save_outputs(plan, validated_insights, creatives)
        log.info("✅ Analysis Complete. Reports saved.")

    def _save_outputs(self, plan, insights, creatives):
        # Save Insights JSON
        insights_path = os.path.join(self.reports_dir, "insights.json")
        with open(insights_path, "w") as f:
            json.dump([i.model_dump() for i in insights], f, indent=2)
            
        # Save Creatives JSON
        creatives_path = os.path.join(self.reports_dir, "creatives.json")
        with open(creatives_path, "w") as f:
            json.dump([c.model_dump() for c in creatives], f, indent=2)
            
        # Generate Markdown Report
        report_path = os.path.join(self.reports_dir, "report.md")
        with open(report_path, "w") as f:
            f.write(f"# Kasparro Agentic Report\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            f.write("## 1. Execution Plan\n")
            f.write(f"**Goal**: {plan.goal}\n")
            for t in plan.tasks:
                f.write(f"- {t.description} ({t.agent})\n")
            
            f.write("\n## 2. Key Insights\n")
            for i in insights:
                icon = "✅" if i.is_validated else "⚠️"
                f.write(f"### {icon} {i.title} (Confidence: {i.validation_score:.2f})\n")
                f.write(f"**Hypothesis**: {i.hypothesis}\n\n")
                f.write(f"**Evidence**:\n")
                for e in i.evidence:
                    sup = "👍" if e.support else "👎"
                    f.write(f"- {sup} {e.description}\n")
                f.write(f"\n**Recommendation**: {i.actionable_recommendation}\n\n")
                
            if creatives:
                f.write("\n## 3. Creative Recommendations\n")
                for c in creatives:
                    f.write(f"### Campaign: {c.campaign_name}\n")
                    f.write(f"**Issue**: {c.current_performance}\n")
                    for v in c.variations:
                        f.write(f"- **{v.headline}**: {v.reasoning}\n")
