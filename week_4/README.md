# The Nexariza Research Desk

A 4-agent CrewAI pipeline (Researcher → Analyst → Writer → Publisher) with a
newsroom-themed Streamlit UI.

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then paste your free Groq + Tavily keys into .env
```

## Run
```bash
# terminal test (no UI)
python crew.py "Latest AI Agent Frameworks 2025"

# full UI
streamlit run app.py
```

## Why this stack (vs. the Gemini/DeepSeek versions you compared)
- **CrewAI over LangGraph**: this is a strict linear chain, no branching/loops —
  CrewAI's role+goal+backstory model fits with less boilerplate than LangGraph's
  state-graph, which earns its complexity when you *do* need conditional paths.
- **Groq + built-in `TavilySearchTool`** over GPT-4o + hand-rolled Tavily calls:
  free-tier friendly, and the built-in tool handles retries/formatting so there's
  less custom code to maintain.
- **`crewai==1.15.x` (current)**, not the `0.28.8` pin — the old pin would likely
  fail to install cleanly or run with a very different (older) API surface.
- **`Crew.kickoff()`** drives the whole run instead of manually calling
  `agent.execute_task()` per agent — kickoff() is what actually manages
  CrewAI's built-in context-passing between tasks.

## Known dependency gotcha (already fixed here)
`crewai_tools.TavilySearchTool` needs the separate `tavily-python` package
installed, or it will interactively prompt to install it (which hangs in
non-interactive environments). It's pinned in `requirements.txt`.

## File structure
```
nexariza_research_engine/
├── agents/
│   ├── __init__.py      # shared Groq LLM + Tavily tool + key validation
│   ├── researcher.py    # build_researcher()
│   ├── analyst.py       # build_analyst()
│   ├── writer.py        # build_writer()
│   └── publisher.py     # build_publisher()
├── tasks.py              # 4 tasks, context-chained, output_file per stage
├── crew.py                # Crew assembly + run_pipeline() with retry + callback
├── utils.py                # retry_on_failure decorator, split_editions helper
├── app.py                   # Streamlit "Research Desk" UI
├── requirements.txt
├── .env.example
└── .gitignore
```
