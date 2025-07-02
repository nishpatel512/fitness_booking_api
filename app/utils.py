import os
import logging
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

# Load environment variables from .env file
load_dotenv()

# Create and configure the application logger
logger = logging.getLogger("fitness_api")
logger.setLevel(logging.INFO)

# Console handler to output logs to terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define the format for log messages
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Add the handler only if it hasn't been added already
if not logger.hasHandlers():
    logger.addHandler(console_handler)

# Determine environment (e.g., dev or prod)
env = os.getenv("ENV", "dev")

# Get loggers for SQLAlchemy and Uvicorn access logs
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
uvicorn_access_logger = logging.getLogger("uvicorn.access")

# Set lower log levels in production to suppress noisy logs
if env == "prod":
    sqlalchemy_logger.setLevel(logging.WARNING)
    uvicorn_access_logger.setLevel(logging.WARNING)
else:
    sqlalchemy_logger.setLevel(logging.INFO)
    uvicorn_access_logger.setLevel(logging.INFO)

# Remove all existing handlers from sqlalchemy to suppress logs completely
for handler in sqlalchemy_logger.handlers[:]:
    sqlalchemy_logger.removeHandler(handler)

# Remove all existing handlers from uvicorn access logger to suppress logs completely
for handler in uvicorn_access_logger.handlers[:]:
    uvicorn_access_logger.removeHandler(handler)


# Converts a datetime object from its current timezone to the given target timezone
def convert_timezone(dt, tz_str: str):
    try:
        return dt.astimezone(ZoneInfo(tz_str))  # Convert using the standard ZoneInfo
    except Exception:
        return dt  # If conversion fails (e.g., bad tz), return original datetime
