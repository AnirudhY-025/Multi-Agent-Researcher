from crewai import Crew, Process

from agents import (
    research_agent,
    research_analyst,
    report_writer
)

from tasks import (
    research_task,
    analysis_task,
    report_task
)

# Create the Crew
research_crew = Crew(
    agents=[
        research_agent,
        research_analyst,
        report_writer
    ],

    tasks=[
        research_task,
        analysis_task,
        report_task
    ],

    process=Process.sequential,

    verbose=True,

    memory=False
)