import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def run_content_agent(custom_topic: str = ""):
    # 1. Initialize Tavily for research
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily = TavilyClient(api_key=tavily_api_key)
    
    query = custom_topic if custom_topic else "latest trending breakthroughs in AI technology 2026"
    search_results = tavily.search(query=query, max_results=5)
    
    sources = [res["url"] for res in search_results.get("results", [])]
    context = "\n".join([res["content"] for res in search_results.get("results", [])])
    
    # 2. Initialize LLM via OpenRouter
    llm = ChatOpenAI(
        model=os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash"),
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=1000,  # Token limit ko kam rakhna taake credits bachain
        temperature=0.7
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert AI Content Engineer for Nexariza AI. Your job is to create engaging social media posts incorporating Nexariza AI branding."),
        ("human", "Based on the following research context, generate 3 pieces of content:\n1. LinkedIn Post (Professional, insightful, with hashtags)\n2. Instagram Caption (Catchy, engaging, emojis, hashtags)\n3. Twitter/X Thread (3-4 connected tweets)\n\nContext:\n{context}\n\nTopic: {topic}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"context": context, "topic": query})
    
    return {
        "topic": query,
        "sources": sources,
        "content": response.content
    }