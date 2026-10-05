# Week 3 — RAG Customer Support Agent

> A production-style RAG customer support agent for **Nexariza AI** — grounded in the company's real website content, with source citations, follow-up suggestions, feedback logging, and a calibrated human-escalation system.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6B6B)](https://www.trychroma.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Embeddings-412991?logo=openai&logoColor=white)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📸 Screenshot

![RAG Customer Support Agent](screenshot.png)

---

## 🎯 The Challenge

This week's challenge: build a **production-style RAG customer support agent** — one that actually *knows the company*, not just a generic chatbot wrapper.

Most tutorials stop at "retrieve + generate." The hard part isn't getting answers — it's teaching the bot **when not to answer**. That's the difference between a demo and something you'd actually trust in front of real customers.

---

## ✨ Features

- 🔍 **RAG pipeline grounded in Nexariza's real website content** — founder, services, industries, everything sourced, not hallucinated
- 📌 **Expandable source citations** under every answer, so users can verify where the info came from
- 💬 **AI-generated follow-up question suggestions** after each response, to keep the conversation flowing naturally
- 👍👎 **Feedback logging** on every answer — a real signal loop for what's working and what isn't
- 🆘 **Calibrated escalation system** — when the bot doesn't know something, it says so honestly, generates a reference ID, and hands off to a human via **Email** or **WhatsApp** instead of guessing
- 🗂️ **Escalation viewer** — a dedicated page to review all escalated queries
- 📄 **Structured escalation log** (`escalations.json`) for auditing and follow-up

---

## 🧠 How It Works

1. **Ingest** — Nexariza's website content is scraped and split into chunks.
2. **Embed** — each chunk is embedded via OpenAI embeddings and stored in ChromaDB.
3. **Retrieve** — on a user query, the most relevant chunks are retrieved.
4. **Generate** — the LLM answers *only* using the retrieved context, with source citations attached.
5. **Suggest** — the LLM generates 2–3 natural follow-up questions.
6. **Escalate (when needed)** — if the bot can't confidently answer, it:
   - Says so honestly (no guessing)
   - Generates a unique **reference ID**
   - Offers **Email** and **WhatsApp** handoff options
   - Logs the escalation to `escalations.json`
7. **Feedback** — every answer can be rated 👍 / 👎 for review.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [LangChain](https://www.langchain.com/) | RAG orchestration |
| [ChromaDB](https://www.trychroma.com/) | Vector store for retrieved content |
| [OpenAI](https://openai.com/) | Embeddings + LLM |
| [Streamlit](https://streamlit.io/) | Web UI |
| Python | Core language |

---

## 📁 Project Structure

```text
Week_3/
├── app.py                    # Streamlit main app (chat UI)
├── bot.py                    # RAG bot logic — retrieval, generation, escalation
├── process.py                # Data ingestion & embedding pipeline
├── view_escalations.py       # Page to view logged escalations
├── escalations.json          # Escalation log (auto-generated)
├── requirements.txt          # Python dependencies
├── Data/                     # Source content / knowledge base
├── pages/                    # Streamlit multi-page app pages
├── .vscode/                  # Editor settings
└── README.md
