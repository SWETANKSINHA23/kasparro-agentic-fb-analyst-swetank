# src/utils/schema.py
from typing import Set
import logging

logger = logging.getLogger("kasparro")

# Required columns for the system to operate
REQUIRED_COLUMNS: Set[str] = {
    "date",
    "spend",
    "impressions",
    "clicks",
    "purchases",
    "revenue"
}

def validate_schema(df_columns) -> None:
    missing = REQUIRED_COLUMNS - set(df_columns)

    if missing:
        logger.error("Schema validation failed. Missing columns: %s", missing)
        raise ValueError(f"Dataset missing required columns: {missing}")

    logger.info("Schema validation passed. All required columns present.")

# optimized

# note: important

# note: important

# temporary fix
