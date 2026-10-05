# Week 1 — ReAct Agent

> A web-search-powered reasoning agent built with LangGraph's ReAct pattern.  
> Given a question, it searches the web, reasons over the results, and returns a sourced answer.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct-1C3C3C)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)](https://groq.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-blueviolet)](https://tavily.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📸 Screenshot

![ReAct Agent Demo](screenshot.png)

---

## ✨ Features

- **ReAct agent** — reason + act loop using LangGraph
- **Groq Llama 3.3 70B** — fast LLM inference
- **Live web search** — powered by Tavily
- **Streamlit UI** with:
  - Persistent chat history grouped by date
  - Local JSON storage for conversations
  - Expandable source citations for every answer
  - Custom warm-toned theme
  - Animated mascot that reacts while the agent is thinking
- **Terminal version** — plain Python script for quick testing

---

## 🧠 How It Works

1. You ask a question.
2. The agent reasons about what it needs to know.
3. If needed, it calls the Tavily web search tool.
4. It reads the search results and reasons again.
5. The loop continues until the agent has enough information.
6. It returns a final answer with source citations.

This is the classic **ReAct** pattern: **Reason → Act → Observe → Repeat**.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | ReAct agent orchestration |
| [Groq](https://groq.com/) | Llama 3.3 70B inference |
| [Tavily](https://tavily.com/) | Live web search |
| [Streamlit](https://streamlit.io/) | Web UI |
| Python | Core language |

---

## 📁 Project Structure

```text
.
├── app.py                  # Streamlit demo UI (main deliverable)
├── week1_first_agent.py    # Plain terminal version of the same agent
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not committed)
├── screenshot.png          # Demo screenshot
└── README.md
