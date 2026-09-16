import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv()

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
docs = []

with open(PROJECT_ROOT / "Data" / "company_info.txt", "r", encoding="utf-8") as f:
    text = f.read()
for chunk in splitter.split_text(text):
    docs.append(Document(page_content=chunk, metadata={"source": "company_info.txt"}))

with open(PROJECT_ROOT / "Data" / "faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)
for faq in faqs:
    content = f"Q: {faq['question']}\nA: {faq['answer']}"
    docs.append(Document(page_content=content, metadata={"source": "FAQ"}))

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

chroma_settings = {
    "collection_name": "nexariza_support",
    "persist_directory": str(PROJECT_ROOT / "chroma_db")
}
Chroma(embedding_function=embeddings, **chroma_settings).delete_collection()

vectordb = Chroma.from_documents(
    docs,
    embeddings,
    **chroma_settings
)

print(f"{len(docs)} chunks ingested into ChromaDB")