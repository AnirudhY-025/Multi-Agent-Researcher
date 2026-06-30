from crewai import Task
from agents import (
    research_agent,
    research_analyst,
    report_writer,
)

# --------------------------------------------------
# Research Task
# --------------------------------------------------

research_task = Task(
    description=(
        """
        Conduct detailed research on the topic: "{topic}".

        Your responsibilities:
        - Search the web for relevant and recent information.
        - Identify key concepts.
        - Gather statistics, facts, and trends.
        - Find reliable sources.
        - Produce comprehensive research notes.
        """
    ),
    expected_output=(
        "A detailed research document containing important facts, "
        "statistics, key concepts, and references."
    ),
    agent=research_agent,
)

# --------------------------------------------------
# Analysis Task
# --------------------------------------------------

analysis_task = Task(
    description=(
        """
        Analyze the research collected by the Research Agent.

        Your responsibilities:
        - Organize the information.
        - Remove duplicate information.
        - Highlight important insights.
        - Identify trends.
        - Prepare structured notes for report generation.
        """
    ),
    expected_output=(
        "A structured analysis containing the most important insights "
        "and observations."
    ),
    agent=research_analyst,
)

# --------------------------------------------------
# Report Writing Task
# --------------------------------------------------

report_task = Task(
    description=(
        """
        Create a professional research report.

        The report should contain:

        1. Executive Summary
        2. Introduction
        3. Key Findings
        4. Analysis
        5. Current Trends
        6. Challenges
        7. Future Scope
        8. Conclusion
        """
    ),
    expected_output=(
        "A complete markdown research report."
    ),
    agent=report_writer,

    output_file="output/research_report.md"
)