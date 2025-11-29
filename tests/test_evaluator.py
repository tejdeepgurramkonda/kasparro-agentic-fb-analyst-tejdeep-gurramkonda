import pytest
from src.agents.evaluator_agent import EvaluatorAgent
from src.schemas.hypothesis import Insight
from src.schemas.data_summary import DataSummary

@pytest.fixture
def evaluator():
    return EvaluatorAgent()

@pytest.fixture
def sample_data():
    return DataSummary(
        total_spend=1000.0,
        total_impressions=100000,
        total_clicks=500,
        avg_ctr=0.005, # 0.5% (Low)
        total_purchases=10,
        total_revenue=1500.0,
        avg_roas=1.5, # Low
        campaign_daily={},
        top_creatives=[],
        audience_breakdown={},
        platform_breakdown={}
    )

def test_validate_low_ctr_hypothesis(evaluator, sample_data):
    insight = Insight(
        title="Creative Fatigue",
        hypothesis="CTR is dropping due to creative fatigue.",
        reasoning="Frequency is high.",
        confidence=0.8
    )
    
    validated = evaluator.validate(insight, sample_data)
    
    assert validated.is_validated is True
    assert validated.validation_score > 0.8 # Score should increase because data supports it (0.5% CTR is low)
    assert any(e.metric == "CTR" and e.support is True for e in validated.evidence)

def test_validate_roas_hypothesis(evaluator, sample_data):
    insight = Insight(
        title="Audience Saturation",
        hypothesis="ROAS is low because audience is saturated.",
        reasoning="CPA is rising.",
        confidence=0.7
    )
    
    validated = evaluator.validate(insight, sample_data)
    
    assert validated.is_validated is True
    assert validated.validation_score > 0.7 # Data supports low ROAS (1.5 < 2.0)
    assert any(e.metric == "ROAS" and e.support is True for e in validated.evidence)

def test_invalidate_hypothesis(evaluator):
    # Data with GOOD metrics
    good_data = DataSummary(
        total_spend=1000.0, total_impressions=10000, total_clicks=500,
        avg_ctr=0.05, # 5% (High)
        total_purchases=50, total_revenue=5000.0, avg_roas=5.0, # High
        campaign_daily={}, top_creatives=[], audience_breakdown={}, platform_breakdown={}
    )
    
    insight = Insight(
        title="Creative Fatigue",
        hypothesis="CTR is dropping due to creative fatigue.",
        reasoning="...",
        confidence=0.8
    )
    
    validated = evaluator.validate(insight, good_data)
    
    # Validation score should drop because data contradicts hypothesis (CTR is actually high)
    assert validated.validation_score < 0.8
    assert any(e.metric == "CTR" and e.support is False for e in validated.evidence)
