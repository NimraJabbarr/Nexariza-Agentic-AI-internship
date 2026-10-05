# Week 4 — The Nexariza Research Desk

> A **4-agent CrewAI pipeline** (Researcher → Analyst → Writer → Publisher) wrapped in a **newsroom-themed Streamlit UI**. Give it a topic, and a virtual newsroom researches it, analyzes it, writes it up, and publishes a finished edition.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Newsroom%20UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-000000)](https://www.crewai.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange)](https://groq.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-blueviolet)](https://tavily.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📸 Screenshot

![The Nexariza Research Desk](screenshot.png)

---

## 🎯 What It Is

The **Nexariza Research Desk** is a **multi-agent AI system** built on CrewAI. It simulates a real newsroom:

| Role | Responsibility |
|---|---|
| 🔍 **Researcher** | Searches the web (Tavily) for the latest, most relevant info on the topic |
| 🧠 **Analyst** | Reads the research, extracts the signal, and identifies key themes/insights |
| ✍️ **Writer** | Turns the analysis into a structured, readable article/edition |
| 📤 **Publisher** | Polishes, formats, and packages the final output for delivery |

Each agent has a **role + goal + backstory**, and the output of each stage is passed cleanly to the next via CrewAI's built-in context chaining.

---

## ✨ Features

- 🤖 **4 specialized agents** working as a pipeline: Researcher → Analyst → Writer → Publisher
- 🌐 **Live web search** via Tavily — no stale data, no hallucinated facts
- ⚡ **Groq-powered inference** — fast and free-tier friendly
- 📰 **Newsroom-themed Streamlit UI** — feels like a real editorial workspace
- 🔗 **Context-chained tasks** — each agent gets the previous stage's output
- 💾 **Per-stage output files** — every stage saves its own artifact for review
- 🔁 **Retry handling** — `retry_on_failure` decorator keeps a run from dying on a transient error
- 📚 **Multi-edition support** — `split_editions` helper separates different topics/editions cleanly
- 🖥️ **CLI + UI** — run it from the terminal or the full dashboard

---

## 🧠 How It Works

The pipeline is a **strict linear chain** — no branching, no loops:
