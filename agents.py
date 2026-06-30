import os
from crewai import Agent, LLM
from tools import search_tool

# Create a shared LLM instance using Ollama
# Model and base URL are read from environment variables set by `run.py`.
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

# Allow model value to include or exclude the 'ollama/' prefix
model_name = OLLAMA_MODEL if OLLAMA_MODEL.startswith("ollama/") else f"ollama/{OLLAMA_MODEL}"

llm = LLM(model=model_name, base_url=OLLAMA_BASE)

# -----------------------------
# Research Agent
# -----------------------------
research_agent = Agent(
    role="Senior AI Researcher",
    goal=(
        "Conduct thorough and accurate web research on the given topic "
        "and collect the most relevant and up-to-date information."
    ),
    backstory=(
        "You are an experienced AI researcher with expertise in finding, "
        "evaluating, and summarizing information from trusted online sources."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=True,
)

# -----------------------------
# Research Analyst
# -----------------------------
research_analyst = Agent(
    role="Research Analyst",
    goal=(
        "Analyze the collected research, identify important insights, "
        "remove duplicate information, and organize findings."
    ),
    backstory=(
        "You specialize in analyzing technical research and transforming "
        "raw information into structured insights."
    ),
    verbose=True,
    memory=False,
    llm=llm,
    allow_delegation=False,
)

# -----------------------------
# Report Writer
# -----------------------------
report_writer = Agent(
    role="Technical Report Writer",
    goal=(
        "Write a professional research report based on the analyzed findings."
    ),
    backstory=(
        "You are an expert technical writer capable of converting "
        "complex research into clear, well-structured reports."
    ),
    verbose=True,
    memory=False,
    llm=llm,
    allow_delegation=False,
)