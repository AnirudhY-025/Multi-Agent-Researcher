import os

from dotenv import load_dotenv
from crewai_tools import SerperDevTool
import logging

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise RuntimeError(
        "SERPER_API_KEY is not set. Please add it to your .env file."
    )

logger = logging.getLogger(__name__)
try:
    # Pass API key via env or tool constructor if supported
    search_tool = SerperDevTool()
except Exception as e:
    logger.exception("Failed to initialize SerperDevTool")
    raise