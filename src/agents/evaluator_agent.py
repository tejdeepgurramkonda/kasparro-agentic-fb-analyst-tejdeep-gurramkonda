from typing import List
from src.schemas.hypothesis import Insight, ValidatedInsight, Evidence
from src.schemas.data_summary import DataSummary
from src.utils.logging_utils import log

class EvaluatorAgent:
    """
    Validates insights against the hard data to ensure they are grounded in reality.
    """
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.ctr_threshold = self.config.get('thresholds', {}).get('ctr_low_threshold', 0.01)
        self.roas_threshold = self.config.get('thresholds', {}).get('roas_low_threshold', 2.0)

    def validate(self, insight: Insight, data: DataSummary) -> ValidatedInsight:
        log.info(f"Validating insight: {insight.title}")
        
        evidence_list = []
        is_validated = False
        score = insight.confidence
        
        # Simple rule-based validation logic (can be expanded with LLM or more complex stats)
        
        # Check 1: If hypothesis mentions "Creative Fatigue" or "CTR", check if CTR is actually low
        if "CTR" in insight.hypothesis or "creative" in insight.hypothesis.lower():
            avg_ctr = data.avg_ctr
            if avg_ctr < self.ctr_threshold:
                evidence_list.append(Evidence(
                    metric="CTR", value=avg_ctr, support=True, 
                    description=f"CTR is {avg_ctr:.2%}, which is low (< {self.ctr_threshold:.2%})."
                ))
                is_validated = True
                score = min(score + 0.2, 1.0)
            else:
                evidence_list.append(Evidence(
                    metric="CTR", value=avg_ctr, support=False, 
                    description=f"CTR is {avg_ctr:.2%}, which is above threshold ({self.ctr_threshold:.2%})."
                ))
                score = max(score - 0.2, 0.0)

        # Check 2: If hypothesis mentions "ROAS", check ROAS
        if "ROAS" in insight.hypothesis:
            avg_roas = data.avg_roas
            if avg_roas < 2.0:
                evidence_list.append(Evidence(
                    metric="ROAS", value=avg_roas, support=True,
                    description=f"ROAS is {avg_roas:.2f}, which is below target (2.0)."
                ))
                is_validated = True
                score = min(score + 0.2, 1.0)
            else:
                evidence_list.append(Evidence(
                    metric="ROAS", value=avg_roas, support=False,
                    description=f"ROAS is {avg_roas:.2f}, which is acceptable."
                ))
                score = max(score - 0.2, 0.0)
        
        # If no specific rules matched, we rely on the initial confidence but flag it
        if not evidence_list:
            evidence_list.append(Evidence(
                metric="N/A", value=0.0, support=True,
                description="No specific quantitative check available for this hypothesis type yet."
            ))
            # Default to trusting the LLM's initial assessment if we can't disprove it
            is_validated = True 

        return ValidatedInsight(
            **insight.model_dump(),
            is_validated=is_validated,
            validation_score=score,
            evidence=evidence_list,
            actionable_recommendation=f"Based on {insight.title}, we recommend testing new variations." # Placeholder
        )
