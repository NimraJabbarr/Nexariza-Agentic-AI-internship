import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
vectordb = Chroma(
    collection_name="nexariza_support",
    persist_directory=str(PROJECT_ROOT / "chroma_db"),
    embedding_function=embeddings
)

# ---- OpenRouter for chat/LLM ----
llm = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct"),
    temperature=0.3,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

ESCALATION_WORDS = ["refund", "complaint", "custom solution", "urgent", "human agent", "bug"]

CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "contact@nexariza.com")
CONTACT_WHATSAPP_LINK = os.getenv("CONTACT_WHATSAPP_LINK", "https://wa.me/923707348001")

# ↓↓↓ neeche saara code same rahega jo pehle diya tha ↓↓↓


# ---------- Core RAG ----------

def get_context(question: str):
    results = vectordb.similarity_search_with_score(question, k=4)
    if not results:
        return None, [], True

    context = "\n\n".join([f"[{r[0].metadata['source']}] {r[0].page_content}" for r in results])
    sources = list({r[0].metadata['source'] for r in results})

    print(f"DEBUG — top distance: {results[0][1]}")   # temporary, terminal mein dekho

    weak_match = results[0][1] > 1.0     # ← loosened, tune karenge real numbers dekh kar
    return context, sources, weak_match


def build_prompt(question: str, context: str) -> str:
    return f"""You are Nexariza AI's support assistant. Answer ONLY using the context below.
If the answer isn't in the context, say you don't have enough information.
Do NOT mention filenames, section headers, or source names in your answer — just give a clean, natural answer.

Context:
{context}

Question: {question}"""


def get_answer(question: str) -> dict:
    """Non-streaming version — poora answer ek dafa mein deta hai"""
    context, sources, weak_match = get_context(question)

    if context is None:
        return {
            "answer": "I don't have enough info on this. Connecting you with our team.",
            "sources": [],
            "escalate": True
        }

    prompt = build_prompt(question, context)
    answer = llm.invoke(prompt).content

    needs_escalation = (
        any(w in question.lower() for w in ESCALATION_WORDS)
        or "don't have enough information" in answer.lower()
        or weak_match
    )

    return {"answer": answer, "sources": sources, "escalate": needs_escalation}


def stream_answer(question: str, context: str):
    """Answer ko word-by-word stream karta hai — ChatGPT jaisa typing effect"""
    prompt = build_prompt(question, context)
    for chunk in llm.stream(prompt):
        yield chunk.content


def get_followups(question: str, answer: str) -> list:
    """3 short follow-up questions generate karta hai"""
    prompt = f"""Based on this Q&A, suggest exactly 3 short, natural follow-up questions
a customer might ask next. Return ONLY the questions, one per line, no numbering, no extra text.

Q: {question}
A: {answer}"""
    response = llm.invoke(prompt).content
    questions = [q.strip("-•123. ") for q in response.split("\n") if q.strip()]
    return questions[:3]


# ---------- Feedback ----------

def log_feedback(question: str, answer: str, feedback: str):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "feedback": feedback
    }
    with open("feedback.json", "a", encoding="utf-8") as f:
        json.dump(entry, f)
        f.write("\n")


# ---------- Escalation ----------

def escalate(question: str, answer: str, user_name: str = "Anonymous", user_contact: str = "") -> dict:
    ref_id = f"ESC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    log_entry = {
        "id": ref_id,
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "bot_answer": answer,
        "user_name": user_name,
        "user_contact": user_contact,
        "status": "pending"
    }

    with open("escalations.json", "a", encoding="utf-8") as f:
        json.dump(log_entry, f)
        f.write("\n")

    return {
        "ref_id": ref_id,
        "email": CONTACT_EMAIL,
        "whatsapp_link": CONTACT_WHATSAPP_LINK
    }


def load_escalations() -> list:
    if not os.path.exists("escalations.json"):
        return []
    with open("escalations.json", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def update_escalation_status(ref_id: str, new_status: str):
    entries = load_escalations()
    for e in entries:
        if e["id"] == ref_id:
            e["status"] = new_status
    with open("escalations.json", "w", encoding="utf-8") as f:
        for e in entries:
            json.dump(e, f)
            f.write("\n")
SMALLTALK_KEYWORDS = ["hi", "hello", "hey", "how are you", "good morning",
                       "good evening", "good afternoon", "thanks", "thank you",
                       "bye", "goodbye", "what's up", "ok", "okay"]


def is_smalltalk(question: str) -> bool:
    q = question.lower().strip().strip("?!.")
    return len(q.split()) <= 5 and any(q == kw or q.startswith(kw) for kw in SMALLTALK_KEYWORDS)


def smalltalk_reply(question: str) -> str:
    prompt = f"""You are a friendly assistant for Nexariza AI. The user sent a casual greeting,
not a company-related question. Reply warmly in 1 short sentence, and invite them to ask
about Nexariza AI's services, pricing, or internships.

User: {question}"""
    return llm.invoke(prompt).content
import re

def clean_answer(text: str) -> str:
    """Koi stray source/metadata tags accidentally answer mein aa jayein to hata deta hai"""
    text = re.sub(r"\(Source:.*?\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"===.*?===", "", text)
    return text.strip()