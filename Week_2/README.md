# Week 2 — Daily Content Posting Agent

> **NEXA // Content Engine** — An autonomous agent that researches trending AI/tech topics and generates branded, platform-specific content for LinkedIn, Instagram, and X/Twitter, with a live visual workspace showing the agent's research and generation process.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Agent-1C3C3C)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange)](https://groq.com/)
[![Tavily](https://img.shields.io/badge/Tavily-Web%20Search-blueviolet)](https://tavily.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📸 Screenshots

| Research View | Content Output |
|---|---|
| ![Research View](screenshot-research.png) | ![Content Output](screenshot-output.png) |

---

## ✨ Features

- **Auto-discovers trending AI/tech topics** via Tavily search — or accepts a manual topic
- **Platform-specific content generation**:
  - LinkedIn post
  - Instagram caption + hashtags
  - X/Twitter thread
  - All branded to **Nexariza AI**
- **Structured JSON daily reports** saved for every run
- **Intelligence Canvas** — shows the selected topic connected to the *real* sources the agent found (title, domain, category, live link). No fabricated data.
- **5-stage live workflow rail**: `Research → Analyze → Select → Generate → Ready`
- **Editable & regeneratable content cards** per platform
- **Daily report archive** in the sidebar, grouped by date, with clear-history support
- **Custom pastel dashboard UI**, built from scratch

---

## 🎯 What Was Required (per the internship roadmap)

- ✅ Accept a topic, or auto-discover a trending AI/tech topic
- ✅ Generate platform-specific content for LinkedIn, Instagram, and Twitter/X
- ✅ Include Nexariza AI branding in every post
- ✅ Output structured JSON with all posts
- ✅ Simple CLI or Streamlit UI

All of the above is implemented in:
- `daily_posting_agent.py` — core logic
- `app.py` — UI

---

## 🚀 What I Added Beyond the Requirement

- 🎨 **A full custom dashboard UI** ("NEXA // Content Engine") — not just a basic form. Built with a distinct visual identity, pastel branded theme, and micro-interactions (hover states, glow effects, animated transitions).
- ⚡ **A live 5-stage workflow rail** (Research → Analyze → Select → Generate → Ready) that animates as the agent actually works — instead of a plain loading spinner.
- 🧠 **An "Intelligence Canvas"** — the selected topic is shown connected to the real sources the agent found, with each source's title, domain, category, and a live link. The research is transparent and verifiable, not a black box.
- ✏️ **Editable content cards** — each platform's output can be edited in place and saved.
- 🔁 **Regenerate per platform** — re-run just LinkedIn, just Instagram, or just the Twitter thread without regenerating everything.
- 🗂️ **Persistent daily report archive** in the sidebar, grouped by date (Today / Yesterday / etc.), with a confirm-before-delete "Clear History" option.
- 🚫 **Topic repeat avoidance** — the agent remembers recently used topics and avoids picking the same one twice in a row.
- 🎯 **Deliberately avoided fabricated metrics** (e.g. fake "trend scores" or "brand alignment %") — every number and label shown is backed by real data the agent actually produced.

---

## 🧠 How It Works

The agent runs a 5-stage pipeline:

1. **Research** — uses Tavily to find trending AI/tech topics and gathers real source articles.
2. **Analyze** — reads and understands what actually matters in those articles.
3. **Select** — picks the strongest topic (avoiding recently used ones).
4. **Generate** — writes a LinkedIn post, Instagram caption + hashtags, and an X/Twitter thread — each in the right tone for that platform, all branded to Nexariza AI.
5. **Ready** — packages everything into a structured JSON daily report and displays it in the dashboard.

The interesting part isn't the LLM call — it's the **pipeline**: research → understand → write → format, each step handing off cleanly to the next. That's the actual skill agentic AI teaches: breaking a fuzzy task into steps a model can reliably do one at a time.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [LangChain](https://www.langchain.com/) | Agent pipeline orchestration |
| [Tavily](https://tavily.com/) | Live web search for trending topics |
| [Groq](https://groq.com/) | Fast LLM inference |
| [Streamlit](https://streamlit.io/) | Dashboard UI |
| Python | Core language |

---

## 📁 Project Structure

```text
.
├── app.py                    # Streamlit dashboard (main deliverable)
├── daily_posting_agent.py    # Core agent pipeline — also runnable standalone
├── requirements.txt          # Python dependencies
├── .env                      # API keys (not committed)
├── screenshot-research.png   # Research view screenshot
├── screenshot-output.png     # Content output screenshot
└── README.md
