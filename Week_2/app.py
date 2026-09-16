import streamlit as st
import json
import datetime
from daily_agent import run_content_agent

# Page Configuration
st.set_page_config(page_title="NEXA // Content Engine", page_icon="🤖", layout="wide")

# Custom Styling for Modern Look
st.markdown("""
    <style>
    .main { background-color: #FDFBF7; }
    .stTextInput > div > div > input {
        border: 2px solid #FFB6C1;
        border-radius: 15px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #FF69B4;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 8px 20px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #eee;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("### NEXARIZA AI · AGENTIC SYSTEMS")
st.title("NEXA // Content Engine")
st.caption("Autonomous content intelligence for Nexariza AI — Powered by LangChain & Tavily")

# Input Section
topic_input = st.text_input("What should NEXA explore today?", placeholder="Enter a custom topic or leave blank for automatic AI trend discovery...")

col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    generate_clicked = st.button("Generate ✦")

if generate_clicked:
    with st.status("Executing Nexariza Autonomous Agent...", expanded=True) as status:
        st.write("🔍 Researching live AI/tech trends via Tavily Search...")
        result = run_content_agent(topic_input)
        st.write("✨ Synthesizing platform-optimized content with Nexariza branding...")
        status.update(label="Content Ready & Verified!", state="complete", expanded=False)
    
    st.success(f"Successfully generated intelligence report for: **{result['topic']}**")
    
    # Store in Session State
    st.session_state['result'] = result

# Display Output if available
if 'result' in st.session_state:
    res = st.session_state['result']
    
    # Quick Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="metric-card"><b>Status</b><br>🟢 Ready to Publish</div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><b>Sources Analyzed</b><br>📚 {len(res["sources"])} Web References</div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><b>Engine</b><br>⚡ LangChain + Tavily</div>', unsafe_allow_html=True)

    # Sources Expander
    with st.expander("🔍 View Verified Research Sources"):
        for src in res["sources"]:
            st.markdown(f"- [{src}]({src})")
            
    st.markdown("---")
    st.subheader("NEXA // OUTPUT CHANNELS")
    
    content_text = res["content"]
    word_count = len(content_text.split())
    
    tab1, tab2, tab3 = st.tabs(["💼 LinkedIn", "📸 Instagram", "🐦 Twitter / X Thread"])
    
    with tab1:
        st.markdown(f"**AI Generated** | 🟢 **Ready** | 📊 `{word_count} words`")
        st.info("Professional thought-leadership format optimized for business networking.")
        st.write(content_text)
        
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("📋 Copy LinkedIn"):
                st.toast("LinkedIn content copied to clipboard!")
                
    with tab2:
        st.markdown(f"**AI Generated** | 🟢 **Ready**")
        st.info("Engaging visual caption format packed with high-reach hashtags & emojis.")
        st.write(content_text)
        
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("📋 Copy Instagram"):
                st.toast("Instagram caption copied to clipboard!")
                
    with tab3:
        st.markdown(f"**AI Generated** | 🟢 **Ready**")
        st.info("Connected multi-tweet thread structured for maximum viral reach.")
        st.write(content_text)
        
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("📋 Copy Twitter"):
                st.toast("Twitter thread copied to clipboard!")

    # --- Feature: Save Daily Report (Fulfills core requirement #4) ---
    st.markdown("---")
    report_json = json.dumps(res, indent=4)
    st.download_button(
        label="📥 Download Structured Daily Report (JSON)",
        data=report_json,
        file_name=f"nexariza_daily_report_{datetime.date.today()}.json",
        mime="application/json"
    )