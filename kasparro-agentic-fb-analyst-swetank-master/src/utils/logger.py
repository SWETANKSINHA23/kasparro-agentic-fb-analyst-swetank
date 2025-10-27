"""Utility module for logging configuration."""

import logging
import sys
from typing import Optional


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Configure and return a standard logger instance.
    
    Input: Logger name (default: module name).
    Output: Configured Logger object.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
    return logger

# note: important
