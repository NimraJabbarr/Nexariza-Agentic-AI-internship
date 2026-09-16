"""
tasks.py
--------
Defines the 4 tasks and wires them into a strict linear chain using
`context=[...]`. Passing context explicitly (instead of relying on
CrewAI to guess) means:
  1. Anyone reading this file instantly understands the data flow.
  2. Each task's output is also saved to its own output_file — useful
     for debugging a specific stage without re-running the whole crew.
"""

from crewai import Task
from agents.researcher import build_researcher
from agents.analyst import build_analyst
from agents.writer import build_writer
from agents.publisher import build_publisher


def build_tasks():
    researcher = build_researcher()
    analyst = build_analyst()
    writer = build_writer()
    publisher = build_publisher()

    research_task = Task(
    description="Research '{topic}' and find key facts, players, and dates. List sources.",
    expected_output="Brief findings with Overview, 5 Key Facts with sources, Sources list.",
)

    analysis_task = Task(
        description=(
            "Analyze the Research Desk's findings on '{topic}'. Extract "
            "5-7 key insights, note any contradictions between sources, "
            "and explain the significance of this topic for stakeholders."
        ),
        expected_output=(
            "A numbered list of 5-7 insights, each 2-3 sentences, plus a "
            "short 'Why It Matters' paragraph."
        ),
        agent=analyst,
        context=[research_task],
        output_file="output/2_analysis_insights.md",
    )

    writing_task = Task(
        description=(
            "Using the Analyst's insights and the Research Desk's facts "
            "on '{topic}', write a complete report. Use ONLY facts from "
            "the provided material — do not invent statistics, quotes, "
            "or names. Structure: Headline, Executive Summary, "
            "Background, Key Findings, Implications, Outlook."
        ),
        expected_output=(
            "A full markdown report with the six required sections, "
            "roughly 700-1200 words."
        ),
        agent=writer,
        context=[research_task, analysis_task],
        output_file="output/3_full_report.md",
    )

    publishing_task = Task(
        description=(
            "Repackage the Writer's report on '{topic}' into two editions: "
            "a LinkedIn post (under 200 words, hook-first, 3-5 hashtags) "
            "and a Medium-style article (title + subtitle + long-form "
            "body). Do not add facts beyond what's in the report. Clearly "
            "label each edition with a markdown heading "
            "'## LinkedIn Edition' and '## Medium Edition'."
        ),
        expected_output=(
            "A markdown document with two clearly labeled sections: "
            "LinkedIn Edition and Medium Edition."
        ),
        agent=publisher,
        context=[writing_task],
        output_file="output/4_published_editions.md",
    )

    return [research_task, analysis_task, writing_task, publishing_task]