# Kasparro — Agentic Facebook Performance Analyst

## Quick Start
```bash
python -V  # should be >= 3.10
python -m venv .venv 
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt

# Set your Google API Key
# Create a .env file with: GOOGLE_API_KEY=your_key_here

# Run the analysis
python -m src.orchestrator.run "Analyze ROAS drop in last 7 days"
```

## Data
- The project uses a synthetic dataset located at `data/synthetic_fb_ads_undergarments.csv`.
- To use your own data, place the CSV in `data/` and update `config/config.yaml`.
- See `data/README.md` for details.

## Config
Edit `config/config.yaml`:
```yaml
python: "3.10"
random_seed: 42
llm:
  model_name: "gemini-2.5-pro" 
thresholds:
  confidence_min: 0.6
```

## Repo Map
- `src/agents/` — `planner.py`, `data_agent.py`, `insight_agent.py`, `evaluator_agent.py`, `creative_agent.py`
- `src/orchestrator/` — `adk_app.py` (Main Logic), `run.py` (CLI)
- `prompts/` — Markdown prompt templates
- `reports/` — `report.md`, `insights.json`, `creatives.json` (Generated outputs)
- `logs/` — Structured JSON logs
- `tests/` — `test_evaluator.py`

## Run
```bash
# Run Analysis
python -m src.orchestrator.run "Analyze ROAS drop"

# Run Tests
pytest tests/
```

## Outputs
- `reports/report.md`: Human-readable analysis report.
- `reports/insights.json`: Structured insights with validation scores.
- `reports/creatives.json`: Generated creative recommendations (if applicable).

## Observability
- Logs are stored in `logs/app.json` in structured JSON format.
