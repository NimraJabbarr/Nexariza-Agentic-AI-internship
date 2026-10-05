Week 1 — ReAct Agent
A web-search-powered reasoning agent built with LangGraph's ReAct pattern. Given a question, it searches the web, reasons over the results, and returns a sourced answer.

Features
ReAct agent (reason + act loop) using Groq's Llama 3.3 70B
Live web search via Tavily
Streamlit UI with:
Persistent chat history, grouped by date (saved to local JSON)
Expandable source citations for every answer
Custom warm-toned theme with an animated mascot that reacts while the agent is thinking
Files
app.py — Streamlit demo UI (main deliverable to run)
week1_first_agent.py — plain terminal version of the same agent
requirements.txt — Python dependencies
Setup
Create a virtual environment and activate it: python -m venv venv venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file in this folder with your API keys:
GROQ_API_KEY=your_key_here TAVILY_API_KEY=your_key_here

Free keys available at console.groq.com and tavily.com.

Run the Streamlit app:
streamlit run app.py

Or run the plain terminal version:

python week1_first_agent.py

Screenshot
ReAct Agent Demo
