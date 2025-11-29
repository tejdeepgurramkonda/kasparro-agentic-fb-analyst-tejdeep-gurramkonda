# Self-Review: Kasparro Agentic System

## Design Choices

### 1. Architecture: Orchestrator Pattern
I chose a central `AgentOrchestrator` to manage the flow between agents. This ensures a predictable execution path (Plan -> Data -> Insight -> Evaluator -> Creative) which is suitable for this specific analytical task.
- **Tradeoff**: Less flexible than a fully autonomous "swarm" but significantly more reliable and easier to debug.

### 2. Pydantic for Structured Output
All inter-agent communication and LLM outputs use Pydantic models (`src/schemas/`).
- **Benefit**: Guarantees type safety and valid JSON structure, reducing "hallucination" errors where the LLM produces malformed data.

### 3. Google GenAI V2 SDK
Used the latest `google-genai` SDK with `gemini-2.0-flash-001`.
- **Reason**: Fast inference speed and large context window, essential for processing data summaries.

### 4. Evaluation Logic
The `EvaluatorAgent` uses a hybrid approach:
- **Rule-based**: Checks hard metrics (e.g., if hypothesis mentions "Low CTR", it verifies if CTR < 1%).
- **LLM-based fallback**: For qualitative insights, it relies on the LLM's reasoning score but flags it as "No quantitative check available".
- **Tradeoff**: Simple rules cover 80% of cases; complex statistical validation would require more time.

### 5. Observability
Implemented structured JSON logging (`logs/app.json`) using `loguru` and `orjson`. This allows for easy ingestion into observability tools (like Datadog or Langfuse) in the future.

## Future Improvements
- **Memory**: Implement a vector store (ChromaDB) to recall past insights.
- **Dynamic Planning**: Allow the Planner to modify the plan mid-execution based on intermediate findings.
