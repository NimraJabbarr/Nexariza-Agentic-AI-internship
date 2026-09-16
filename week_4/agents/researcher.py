"""
agents/researcher.py
---------------------
Desk 1 of 4: The Research Desk.
Job: given a topic, go find real, current, sourced information on the
web using Tavily. Nothing else — no summarizing, no writing. That
separation of concerns is the whole point of a multi-agent pipeline:
each agent does ONE job well instead of one agent doing everything
average-well.
"""

from crewai import Agent
from agents import shared_llm, search_tool


def build_researcher() -> Agent:
    return Agent(
        role="Senior Research Desk Correspondent",
        goal=(
            "Investigate {topic} thoroughly using live web search. Collect "
            "concrete facts, figures, dates, and named sources — never "
            "invent anything. Cover multiple angles (what happened, who is "
            "involved, why it matters, what's next) and remove duplicate "
            "or near-duplicate sources."
        ),
        backstory=(
            "You are a veteran investigative correspondent at the Nexariza "
            "Research Desk. You've spent years learning that a report is "
            "only as good as its sourcing — you'd rather return 8 solid, "
            "verifiable sources than 20 vague ones. You always note where "
            "each fact came from."
        ),
        tools=[search_tool],
        llm=shared_llm,
        allow_delegation=False,  # linear pipeline — no agent should hand work sideways
        verbose=True,
    )
