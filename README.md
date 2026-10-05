<div align="center">

# Nexariza AI — Agentic AI Internship

### 6 weeks. 6 real agentic AI systems. Built, shipped, and documented in public.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-ReAct-1C3C3C)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Intern:** Areeba Zaka  
**Program:** Agentic AI Internship @ [Nexariza AI](https://nexariza.com)

</div>

---

## 📖 About

This repo documents my **6-week Agentic AI Internship at Nexariza AI** — building real, deployable **multi-agent and RAG systems** each week, from a single ReAct agent up to a full multi-tool AI assistant.

Each week lives in its own folder with its own **README, setup instructions, and demo screenshots**.

---

## 📊 Weekly Progress

| # | Project | What It Does | Status |
|:-:|:---|:---|:---:|
| 1 | **ReAct Agent** | Web-search-powered reasoning agent with sourced answers | ✅ Done |
| 2 | **NEXA Content Engine** | Trending topic research → branded LinkedIn/IG/X content, with a live research workspace UI | ✅ Done |
| 3 | **Nexariza Support Bot** | RAG chat agent grounded on real company content, with honest escalation | ✅ Done |
| 4 | **The Nexariza Research Desk** | 4-agent investigative newsroom that researches, analyzes, writes, and publishes a report | ✅ Done |
| 5 | **Lead Intelligence Agent** | Discovers real companies, scores Hot/Warm/Cold, drafts personalized outreach | 🔜 Coming |
| 6 | **Nexariza Command Center** _(Capstone)_ | Six AI tools in one workspace — research, content, email, meetings, competitors, trends | 🔜 Coming |

---

## 🛠️ Tech Stack

<p>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C" />
  <img src="https://img.shields.io/badge/Groq-Llama%203.3%2070B-orange" />
  <img src="https://img.shields.io/badge/Tavily-Search-blueviolet" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6B6B" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" />
</p>

- **LangChain** — agent & RAG orchestration
- **LangGraph** — ReAct reasoning loop
- **Groq (Llama 3.3 70B)** — fast LLM inference
- **Tavily Search** — live web search
- **ChromaDB** — vector store for RAG
- **Streamlit** — interactive UIs
- **Python** — core language

---

## 🗂️ Repository Structure

```text
Nexariza-Agentic-AI-Internship/
│
├── Week_1/                    # ReAct Agent
│   ├── app.py                 # Streamlit UI
│   ├── week1_first_agent.py   # Terminal version
│   ├── requirements.txt
│   └── README.md
│
├── Week_2/                    # NEXA Content Engine
│   ├── app.py
│   ├── daily_posting_agent.py
│   ├── requirements.txt
│   └── README.md
│
├── Week_3/                    # Nexariza Support Bot (RAG)
│   ├── app.py
│   ├── bot.py
│   ├── process.py
│   ├── view_escalations.py
│   ├── pages/
│   ├── Data/
│   ├── requirements.txt
│   └── README.md
│
├── Week_4/                    # The Nexariza Research Desk (CrewAI)
│   ├── agents/
│   ├── tasks.py
│   ├── crew.py
│   ├── utils.py
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md                  # ← you are here
