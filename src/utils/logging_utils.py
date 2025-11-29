import sys
from pathlib import Path
from loguru import logger
from rich.logging import RichHandler
import orjson

def setup_logging(log_dir: str = "logs", level: str = "INFO"):
    """
    Configure logging with Rich for console and JSON for files.
    
    Args:
        log_dir: Directory to store log files.
        level: Logging level for console output.
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Remove default handler to avoid duplicate logs
    logger.remove()

    # Add Rich handler for beautiful console output
    logger.add(
        RichHandler(rich_tracebacks=True, markup=True),
        format="{message}",
        level=level,
        backtrace=True,
        diagnose=True
    )

    # Add JSON handler for structured file logging (great for observability)
    log_file = Path(log_dir) / "app.json"
    
    def serialize(record):
        subset = {
            "timestamp": record["time"].timestamp(),
            "level": record["level"].name,
            "message": record["message"],
            "extra": record["extra"],
            "file": record["file"].name,
            "line": record["line"],
        }
        return orjson.dumps(subset).decode("utf-8") + "\n"

    logger.add(
        log_file,
        format="{message}",
        level="DEBUG",
        serialize=True,
        rotation="10 MB",
        retention="1 week",
    )

    return logger

# Create a default logger instance to be imported elsewhere
log = logger
