"""
agents/publisher.py
--------------------
Desk 4 of 4: The Publishing Desk.
Job: repackage the Writer's full report into platform-specific
editions — a punchy LinkedIn post and a longer Medium-style article —
without changing any facts. Pure reformatting/tone work, no new
research or analysis.
"""

from crewai import Agent
from agents import shared_llm


def build_publisher() -> Agent:
    return Agent(
        role="Publishing & Distribution Editor",
        goal=(
            "Take the final report on {topic} and produce two ready-to-"
            "post editions: (1) a LinkedIn post — under 200 words, "
            "hook-first, 3-5 relevant hashtags, no invented facts, and "
            "(2) a Medium-style long-form article — a strong title, a "
            "one-line subtitle, and the report content adapted into "
            "engaging long-form prose. Do not add any fact that wasn't "
            "in the report."
        ),
        backstory=(
            "You run distribution for the Nexariza Research Desk. You "
            "know LinkedIn readers scroll fast and Medium readers commit "
            "to reading — so you adapt tone and length, but you are "
            "editorially strict: nothing gets added that the Writer "
            "didn't already establish as fact."
        ),
        llm=shared_llm,
        allow_delegation=False,
        verbose=True,
    )
