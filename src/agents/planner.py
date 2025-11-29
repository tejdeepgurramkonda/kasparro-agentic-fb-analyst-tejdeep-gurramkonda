from src.utils.llm_client import LLMClient
from src.schemas.plan import Plan
from src.utils.logging_utils import log

class PlannerAgent:
    """
    Decomposes high-level user queries into executable plans.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        # In a real scenario, load from prompts/planner_prompt.md
        # For now, we'll define a robust default here or read it if it exists.
        return """
        You are an expert Marketing Analyst Planner.
        Your goal is to break down a user's request about Facebook Ads performance into a structured plan.
        
        Available Agents:
        1. Data Agent: Can load data, calculate metrics (ROAS, CTR, Spend), and aggregate by time/platform/audience.
        2. Insight Agent: Analyzes the data summary to find patterns, anomalies, and generate hypotheses.
        3. Evaluator Agent: Validates hypotheses using statistical checks or logic.
        4. Creative Agent: Generates new ad copy/headlines if performance is low.

        User Query: "{user_query}"

        Create a plan that logically flows from Data -> Insight -> Evaluator -> Creative (if needed).
        """

    def create_plan(self, user_query: str) -> Plan:
        log.info(f"Creating plan for query: {user_query}")
        
        prompt = self.prompt_template.format(user_query=user_query)
        
        try:
            plan = self.llm.generate_structured(
                prompt=prompt,
                response_schema=Plan,
                system_instruction="You are a precise planner for an AI agent system."
            )
            log.info(f"Plan generated with {len(plan.tasks)} tasks.")
            return plan
        except Exception as e:
            log.error(f"Planning failed: {e}")
            raise
