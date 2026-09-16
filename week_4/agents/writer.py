"""
agents/writer.py
-----------------
Desk 3 of 4: The Writer's Desk.
Job: turn the Analyst's structured insights into one full, readable
report with a clear structure (headline, executive summary,
background, findings, implications, outlook). Explicitly instructed
not to invent statistics that weren't in the research — this is the
single most important guardrail in the whole pipeline, since LLMs
left unchecked will happily hallucinate a plausible-sounding number.
"""

from crewai import Agent
from agents import shared_llm


def build_writer() -> Agent:
    return Agent(
        role="Senior Staff Writer",
        goal=(
            "Write a complete, well-structured report on {topic} using "
            "ONLY the facts and insights handed to you by Research and "
            "Analysis. Never invent a statistic, quote, date, or name "
            "that wasn't in the provided material. Structure: Headline, "
            "Executive Summary, Background, Key Findings, Implications, "
            "Outlook."
        ),
        backstory=(
            "You are the Nexariza Research Desk's senior staff writer. "
            "Editors trust you because your reports never need a fact-"
            "check correction — if something isn't in the source "
            "material, it doesn't go in the report, no matter how good "
            "it would sound."
        ),
        llm=shared_llm,
        allow_delegation=False,
        verbose=True,
    )
