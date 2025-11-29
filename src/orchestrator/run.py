import typer
import yaml
import sys
import os
from dotenv import load_dotenv

# Load environment variables explicitly
load_dotenv(dotenv_path=".env")

from src.utils.logging_utils import setup_logging, log
from src.orchestrator.adk_app import AgentOrchestrator

app = typer.Typer()

@app.command()
def analyze(
    query: str = typer.Argument(..., help="The analysis query (e.g., 'Analyze ROAS drop')"),
    config_path: str = typer.Option("config/config.yaml", help="Path to configuration file")
):
    """
    Run the Kasparro Agentic Analyst on a specific query.
    """
    try:
        # Load Config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        # Setup Logging
        setup_logging(
            log_dir=config['paths']['logs_dir'],
            level="INFO"
        )
        
        log.info(f"🔧 Loaded config from {config_path}")
        
        # Initialize and Run Orchestrator
        orchestrator = AgentOrchestrator(config)
        orchestrator.run(query)
        
    except Exception as e:
        log.error(f"❌ Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    app()
