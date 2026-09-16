import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_community.utilities import SerpAPIWrapper

# Load environment variables
load_dotenv()

openrouter_key = os.getenv("OPENROUTER_API_KEY")
serpapi_key = os.getenv("SERPAPI_API_KEY")

if not openrouter_key:
    st.error("Missing OPENROUTER_API_KEY. Add it to your .env file or environment before running the app.")
    st.stop()

# Initialize OpenRouter-compatible LLM via the OpenAI client
# Use a model name that is actually available on OpenRouter.
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    openai_api_key=openrouter_key,
    base_url="https://openrouter.ai/api/v1",
)

# Initialize SerpAPI search tool
search = SerpAPIWrapper(serpapi_api_key=serpapi_key) if serpapi_key else None

def safe_search(query: str):
    if search is None:
        return "Set the SERPAPI_API_KEY value in your .env file to enable web search."
    return search.run(query)

tools = [
    Tool(
        name="Web Search",
        func=safe_search,
        description="Useful for searching the web.",
    )
]

# Correct custom ReAct prompt
react_prompt = PromptTemplate.from_template(
    """
You are a helpful assistant.
You have access to the following tools:
{tools}

Use this format exactly:

Question: the input question
Thought: reason about what to do next
Action: the action to take, should be one of: {tool_names}
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Important:
- If no tool is needed, do not invent an action. Instead, respond with:
  Thought: I can answer directly.
  Final Answer: <your final response>
- Never output `Action: None`.

Question: {input}
{agent_scratchpad}
"""
)

# Create agent with prompt
agent = create_react_agent(llm, tools, react_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

# Streamlit UI setup
st.set_page_config(page_title="ReAct Agent", page_icon="🤖", layout="wide")

st.sidebar.title("📜 History")
if "history" not in st.session_state:
    st.session_state["history"] = []

for i, item in enumerate(st.session_state["history"]):
    st.sidebar.write(f"{i + 1}. {item['query']}")

st.title("🌐 ReAct Agent")
query = st.text_input("Ask anything…")
if st.button("Ask Agent →") and query:
    with st.spinner("Thinking..."):
        response = agent_executor.invoke({"input": query})
    st.success("ANSWER")
    st.write(response["output"])
    st.session_state["history"].append({"query": query, "response": response["output"]})
