"""
agents/analyst.py
------------------
Desk 2 of 4: The Analyst Desk.
Job: take the Researcher's raw findings and extract structured signal
from them — key insights, patterns, a stakeholder-impact angle, and an
explicit "so what" (why does this matter). No web access here on
purpose: the Analyst reasons over what Research already found, it
doesn't go fetch more (that would blur the pipeline stages).
"""

from crewai import Agent
from agents import shared_llm


def build_analyst() -> Agent:
    return Agent(
        role="Lead Insights Analyst",
        goal=(
            "Read the Research Desk's findings on {topic} and extract the "
            "5-7 most important, non-obvious insights. Identify patterns "
            "across sources, flag any disagreement between sources, and "
            "state clearly why this topic matters to the reader."
        ),
        backstory=(
            "You are the Analyst Desk's lead at Nexariza — the person who "
            "turns a pile of scattered facts into a clear narrative. You "
            "never repeat raw facts verbatim; you connect them. You are "
            "allergic to filler insights like 'this is important' without "
            "explaining why."
        ),
        llm=shared_llm,
        allow_delegation=False,
        verbose=True,
    )
