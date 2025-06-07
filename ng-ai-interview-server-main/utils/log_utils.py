import sys
from loguru import logger

def setup_logger():
    """Configure and setup loguru logger"""
    # Remove default handler
    logger.remove()
    
    # Add custom formatted handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # Optional: Add file handler for logging to file
    logger.add(
        "logs/ai_interview_{time}.log",
        rotation="500 MB",
        retention="10 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    return logger

# Initialize logger
logger = setup_logger() 