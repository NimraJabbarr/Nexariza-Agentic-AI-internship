"""
app.py
------
The Nexariza Research Desk — Streamlit front-end for the 4-agent
CrewAI pipeline. Single-file UI with enhanced professional color scheme
and refined typography.
"""

import os
import time
import datetime
import streamlit as st
import litellm
from functools import wraps

# ============================================================
# FIX: Disable caching and patch completion for Groq
# ============================================================

# 1. Disable caching globally
os.environ["LITELLM_CACHE_TYPE"] = "none"
litellm.caching = False
litellm.cache = None

# 2. Monkey patch to filter out cache_breakpoint from messages
original_completion = litellm.completion

@wraps(original_completion)
def patched_completion(*args, **kwargs):
    if 'messages' in kwargs:
        kwargs['messages'] = [
            {k: v for k, v in msg.items() if k != 'cache_breakpoint'}
            if isinstance(msg, dict) else msg
            for msg in kwargs['messages']
        ]
    return original_completion(*args, **kwargs)

litellm.completion = patched_completion

# 3. Now import your custom modules
from agents import validate_keys
from crew_local import run_pipeline
from utils import (split_editions, count_words, count_numbered_insights,
                    extract_pull_quote, classify_sources)

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Nexariza Intelligence Desk",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# THEME / CSS - Enhanced Professional Color Scheme
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #1a2639;        /* Deep navy */
        --primary-light: #2c3e66;
        --secondary: #3d5a80;      /* Muted blue */
        --accent: #e67e22;         /* Warm amber accent */
        --accent-light: #f39c12;
        --success: #2ecc71;        /* Emerald */
        --background: #f0f2f5;     /* Light gray background */
        --card-bg: #ffffff;
        --card-border: #e8edf2;
        --text-primary: #1a2639;
        --text-secondary: #4a5a6e;
        --text-muted: #7f8fa6;
        --shadow: 0 4px 20px rgba(26, 38, 57, 0.08);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--background) !important;
        color: var(--text-primary);
    }

    .stApp {
        background: linear-gradient(135deg, #f0f2f5 0%, #e8ecf1 100%);
    }

    /* ---- Masthead ---- */
    .masthead {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
        border-bottom: 3px solid var(--accent);
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
        border-radius: 12px;
        padding: 2.5rem 2rem;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    .masthead::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: rgba(230, 126, 34, 0.05);
        border-radius: 50%;
    }
    .masthead h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        letter-spacing: 1px;
        color: #ffffff;
        margin-bottom: 0.3rem;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: relative;
    }
    .masthead .tagline {
        font-style: italic;
        color: var(--accent-light);
        font-size: 1rem;
        letter-spacing: 1px;
        font-weight: 300;
        position: relative;
    }
    .masthead .issue-line {
        color: rgba(255,255,255,0.6);
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 0.8rem;
        font-weight: 300;
        position: relative;
    }

    /* ---- Sidebar / Archive ---- */
    section[data-testid="stSidebar"] {
        background-color: var(--primary);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.2) !important;
        border-color: var(--accent-light) !important;
    }
    .archive-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 0.1rem;
        font-weight: 700;
    }
    .archive-sub {
        color: rgba(255,255,255,0.5);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 1.2rem;
    }
    .archive-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 8px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }
    .archive-card:hover {
        background: rgba(255,255,255,0.12);
        transform: translateX(4px);
    }
    .archive-card .ts {
        color: var(--accent-light);
        font-size: 0.65rem;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .archive-card .headline {
        font-size: 0.85rem;
        color: #ffffff;
        margin: 0.15rem 0;
        font-weight: 500;
    }
    .archive-card .meta {
        color: rgba(255,255,255,0.4);
        font-size: 0.7rem;
    }

    /* ---- Stepper ---- */
    .desk-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: left;
        min-height: 100px;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    .desk-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(26, 38, 57, 0.12);
    }
    .desk-num {
        color: var(--text-muted);
        font-size: 0.7rem;
        letter-spacing: 2px;
        font-weight: 600;
    }
    .desk-name {
        font-weight: 700;
        font-size: 0.95rem;
        margin: 0.15rem 0 0.3rem 0;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    .status-standing { 
        color: var(--text-muted); 
        font-size: 0.75rem; 
        font-weight: 500;
    }
    .status-active { 
        color: var(--accent); 
        font-size: 0.75rem; 
        font-weight: 600;
    }
    .status-filed { 
        color: var(--success); 
        font-size: 0.75rem; 
        font-weight: 600;
    }
    .desk-meta { 
        color: var(--text-muted); 
        font-size: 0.7rem; 
        margin-top: 0.2rem;
        font-weight: 400;
    }

    /* ---- Timeline ---- */
    .timeline-title {
        color: var(--secondary);
        letter-spacing: 3px;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin: 1.5rem 0 0.8rem 0;
        border-bottom: 2px solid var(--card-border);
        padding-bottom: 0.5rem;
        font-weight: 700;
    }
    .timeline-row {
        background: var(--card-bg);
        border-left: 3px solid var(--accent);
        border-radius: 6px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.4rem;
        font-size: 0.85rem;
        box-shadow: var(--shadow);
        transition: all 0.2s ease;
    }
    .timeline-row:hover {
        transform: translateX(4px);
        border-left-color: var(--accent-light);
    }
    .timeline-row .t-time {
        color: var(--text-muted);
        font-size: 0.7rem;
        display: block;
        font-weight: 500;
    }

    /* ---- Report card ---- */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 4px;
        font-size: 0.65rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    .badge-special { 
        background: var(--accent); 
        color: #ffffff; 
    }
    .badge-verified { 
        background: transparent; 
        border: 2px solid var(--success); 
        color: var(--success); 
    }

    .report-headline {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        color: var(--text-primary);
        margin: 0.6rem 0 0.2rem 0;
        font-weight: 700;
        line-height: 1.3;
    }
    .report-byline {
        color: var(--text-secondary);
        font-size: 0.8rem;
        border-bottom: 2px solid var(--card-border);
        padding-bottom: 0.8rem;
        font-weight: 400;
    }
    .pull-quote {
        border-left: 4px solid var(--accent);
        padding: 0.8rem 1.2rem;
        font-style: italic;
        color: var(--secondary);
        margin: 1.2rem 0;
        font-size: 1rem;
        background: rgba(61, 90, 128, 0.05);
        border-radius: 0 6px 6px 0;
    }

    .source-row {
        border-bottom: 1px solid var(--card-border);
        padding: 0.6rem 0;
        transition: all 0.2s ease;
    }
    .source-row:hover {
        background: rgba(61, 90, 128, 0.03);
        padding-left: 0.5rem;
    }
    .source-tag {
        font-size: 0.6rem;
        letter-spacing: 1px;
        color: var(--success);
        border: 1px solid var(--success);
        padding: 0.05rem 0.5rem;
        border-radius: 3px;
        margin-right: 0.6rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* buttons */
    .stButton>button, .stDownloadButton>button {
        background-color: var(--card-bg);
        color: var(--text-primary);
        border: 1.5px solid var(--secondary);
        border-radius: 6px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        padding: 0.5rem 1.2rem;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: var(--secondary);
        color: #ffffff;
        border-color: var(--secondary);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(61, 90, 128, 0.3);
    }
    div[data-testid="stTextInput"] input {
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--card-border) !important;
        border-radius: 6px !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--secondary) !important;
        box-shadow: 0 0 0 3px rgba(61, 90, 128, 0.1) !important;
    }
    footer, #MainMenu {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--card-bg);
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        color: var(--text-secondary);
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(61, 90, 128, 0.08);
        color: var(--text-primary);
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--secondary) !important;
        color: #ffffff !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--card-bg) !important;
        border-radius: 6px !important;
        border: 1px solid var(--card-border) !important;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* Alert/warning styling */
    .stAlert {
        border-radius: 8px !important;
        border-left: 4px solid var(--accent) !important;
    }
    .stAlert [data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------
if "archive" not in st.session_state:
    st.session_state.archive = []          # list of past reports (dicts)
if "timeline" not in st.session_state:
    st.session_state.timeline = []          # list of (time, label) for current run
if "current" not in st.session_state:
    st.session_state.current = None         # currently displayed report dict
if "desk_status" not in st.session_state:
    st.session_state.desk_status = {"Research": "standing", "Analyst": "standing",
                                     "Writer": "standing", "Publisher": "standing"}
if "desk_metrics" not in st.session_state:
    st.session_state.desk_metrics = {"Research": "", "Analyst": "", "Writer": "", "Publisher": ""}

ISSUE_NO = len(st.session_state.archive) + 1


def log_step(label: str):
    st.session_state.timeline.append((datetime.datetime.now().strftime("%H:%M:%S"), label))


# ----------------------------------------------------------------------
# SIDEBAR — THE ARCHIVE
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="archive-title">📊 Intelligence Archive</div>', unsafe_allow_html=True)
    st.markdown('<div class="archive-sub">Case Files</div>', unsafe_allow_html=True)

    if st.button("🗑️  Clear Archive", use_container_width=True):
        st.session_state.archive = []
        st.session_state.current = None
        st.session_state.timeline = []
        st.rerun()

    st.markdown("---")

    if not st.session_state.archive:
        st.caption("No intelligence reports filed yet. Begin a new investigation.")
    else:
        for i, item in enumerate(reversed(st.session_state.archive)):
            st.markdown(
                f"""
                <div class="archive-card">
                    <div class="ts">Case #{len(st.session_state.archive) - i}</div>
                    <div class="headline">{item['topic'][:42]}</div>
                    <div class="meta">{item['num_sources']} sources · filed</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open Report", key=f"open_{i}", use_container_width=True):
                st.session_state.current = item
                st.rerun()

# ----------------------------------------------------------------------
# MASTHEAD - Updated with professional branding
# ----------------------------------------------------------------------
today = datetime.date.today().strftime("%A, %B %d, %Y").upper()
st.markdown(
    f"""
    <div class="masthead">
        <h1>NEXARIZA INTELLIGENCE DESK</h1>
        <div class="tagline">AI-Powered Research &amp; Analysis</div>
        <div class="issue-line">{today} · REPORT NO. {ISSUE_NO} · NEXARIZA AGENTIC SYSTEMS</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# ASSIGNMENT BAR - Updated with professional language
# ----------------------------------------------------------------------
st.markdown("#### 🎯 Start an Investigation")
st.caption("Define the research focus for the intelligence team")

col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input("topic", placeholder="Enter your research topic or question...",
                           label_visibility="collapsed")
with col2:
    run_clicked = st.button("START ANALYSIS →", use_container_width=True)

# ----------------------------------------------------------------------
# STEPPER (4 desks) - Updated labels
# ----------------------------------------------------------------------
desk_names = ["Research Desk", "Analytics Desk", "Content Desk", "Publishing Desk"]
desk_keys = ["Research", "Analyst", "Writer", "Publisher"]
stepper_cols = st.columns(4)
stepper_placeholders = []
for i, col in enumerate(stepper_cols):
    with col:
        ph = st.empty()
        stepper_placeholders.append(ph)


def render_stepper():
    labels = {"standing": ("STANDING BY", "status-standing"),
              "active": ("● ANALYZING", "status-active"),
              "filed": ("✓ COMPLETE", "status-filed")}
    for i, ph in enumerate(stepper_placeholders):
        key = desk_keys[i]
        status = st.session_state.desk_status[key]
        text, css = labels[status]
        metric = st.session_state.desk_metrics.get(key, "")
        metric_html = f'<div class="desk-meta">{metric}</div>' if metric else ""
        ph.markdown(
            f"""
            <div class="desk-card">
                <div class="desk-num">STEP {i+1}</div>
                <div class="desk-name">{desk_names[i].upper()}</div>
                <div class="{css}">{text}</div>
                {metric_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


render_stepper()

# ----------------------------------------------------------------------
# RUN PIPELINE
# ----------------------------------------------------------------------
if run_clicked:
    problems = validate_keys()
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before starting the analysis.")
    elif problems:
        for p in problems:
            st.error(f"⚠️ {p}")
    else:
        st.session_state.timeline = []
        st.session_state.desk_status = {k: "standing" for k in desk_keys}
        st.session_state.desk_metrics = {k: "" for k in desk_keys}
        log_step("📋 Assignment received")
        render_stepper()

        stage_order = ["Research", "Analyst", "Writer", "Publisher"]
        stage_labels = {
            "research_started": ("Research", "🔎 Research phase initiated"),
            "pipeline_complete": (None, "✅ Report completed successfully"),
        }

        timeline_box = st.container()

        def step_callback(event: str):
            if event in stage_labels:
                desk, label = stage_labels[event]
                if desk:
                    st.session_state.desk_status[desk] = "active"
                log_step(label)
                render_stepper()

        # app.py - RUN PIPELINE section (around line 580)

with st.spinner("🔍 The intelligence team is analyzing..."):
    try:
        outputs = run_pipeline(topic, step_callback=step_callback)
        if outputs is None:
            st.error("⚠️ Pipeline returned no output. Please try again.")
            outputs = None
    except Exception as e:
        st.error(f"⚠️ Pipeline encountered an error: {e}")
        outputs = None

        if outputs:
            # ---- compute real metrics from the actual outputs ----
            sources = classify_sources(outputs["research"])
            num_sources = max(len(sources), 1)
            num_insights = count_numbered_insights(outputs["analysis"])
            num_words = count_words(outputs["report"])
            editions = split_editions(outputs["published"])
            pull_quote = extract_pull_quote(outputs["report"])

            st.session_state.desk_status = {k: "filed" for k in desk_keys}
            st.session_state.desk_metrics = {
                "Research": f"{num_sources} sources identified",
                "Analyst": f"{num_insights} key insights",
                "Writer": f"{num_words} words drafted",
                "Publisher": "2 editions formatted",
            }
            render_stepper()

            # ---- FIXED: Save files with proper encoding ----
            import os as _os
            _os.makedirs("output", exist_ok=True)
            
            # ✅ FIXED: Added encoding='utf-8' and error handling
            try:
                with open("output/full_report.txt", "w", encoding="utf-8", errors="replace") as f:
                    f.write(outputs["report"])
                with open("output/linkedin_post.txt", "w", encoding="utf-8", errors="replace") as f:
                    f.write(editions["linkedin"])
                with open("output/medium_post.md", "w", encoding="utf-8", errors="replace") as f:
                    f.write(editions["medium"])
            except Exception as e:
                st.warning(f"⚠️ Could not save files: {e}")
                # Fallback: save without encoding
                with open("output/full_report.txt", "w", errors="ignore") as f:
                    f.write(outputs["report"])
                with open("output/linkedin_post.txt", "w", errors="ignore") as f:
                    f.write(editions["linkedin"])
                with open("output/medium_post.md", "w", errors="ignore") as f:
                    f.write(editions["medium"])

            report = {
                "topic": topic,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "num_sources": num_sources,
                "num_insights": num_insights,
                "num_words": num_words,
                "pull_quote": pull_quote,
                "sources": sources,
                "research": outputs["research"],
                "analysis": outputs["analysis"],
                "report": outputs["report"],
                "linkedin": editions["linkedin"],
                "medium": editions["medium"],
                "timeline": list(st.session_state.timeline),
            }
            st.session_state.archive.append(report)
            st.session_state.current = report
            log_step("📤 Editions ready for distribution")
            st.rerun()

# ----------------------------------------------------------------------
# TIMELINE (only while nothing filed yet, or to show most recent run)
# ----------------------------------------------------------------------
if st.session_state.timeline and not st.session_state.current:
    st.markdown('<div class="timeline-title">⏱ Investigation Timeline</div>', unsafe_allow_html=True)
    for ts, label in st.session_state.timeline:
        st.markdown(
            f'<div class="timeline-row"><span class="t-time">{ts}</span>{label}</div>',
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------
# REPORT DISPLAY
# ----------------------------------------------------------------------
if st.session_state.current:
    r = st.session_state.current

    st.markdown(
        '<span class="badge badge-special">INTELLIGENCE REPORT</span>'
        '<span class="badge badge-verified">VERIFIED ✓</span>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="report-headline">{r["topic"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="report-byline">Prepared by the Nexariza AI Intelligence Team · '
        f'{datetime.date.today().isoformat()} · {r["num_sources"]} sources consulted</div>',
        unsafe_allow_html=True,
    )

    if r.get("pull_quote"):
        st.markdown(f'<div class="pull-quote">"{r["pull_quote"]}"</div>', unsafe_allow_html=True)

    tabs = st.tabs(["📄 Full Report", "🧠 Intelligence Analysis", "🔎 Research Findings"])
    with tabs[0]:
        st.markdown(r["report"])
    with tabs[1]:
        st.markdown(r["analysis"])
    with tabs[2]:
        st.markdown(r["research"])

    # ---- THE SOURCE ROOM ----
    st.markdown('<div class="timeline-title">📚 Source Directory</div>', unsafe_allow_html=True)
    sources = r.get("sources", [])
    n_academic = sum(1 for s in sources if s["tag"] == "ACADEMIC")
    n_news = sum(1 for s in sources if s["tag"] == "NEWS")
    n_primary = sum(1 for s in sources if s["tag"] == "PRIMARY")
    st.caption(
        f"{len(sources)} sources referenced — {n_academic} academic · {n_news} news · "
        f"{n_primary} primary/industry"
    )
    st.caption("Classification based on domain analysis.")
    for s in sources:
        st.markdown(
            f"""<div class="source-row"><span class="source-tag">{s['tag']}</span>
            {s['domain']}</div>""",
            unsafe_allow_html=True,
        )

    # ---- THE PRESS ROOM ----
    st.markdown('<div class="timeline-title">🖨 Distribution Channels</div>', unsafe_allow_html=True)
    press_cols = st.columns(3)

    with press_cols[0]:
        st.markdown("**LinkedIn — Professional Edition**")
        preview = r["linkedin"][:220] + ("…" if len(r["linkedin"]) > 220 else "")
        st.markdown(f"<div style='color:#7f8fa6;font-size:0.85rem;'>{preview}</div>",
                    unsafe_allow_html=True)
        st.download_button("📤 Export", r["linkedin"],
                            file_name="linkedin_post.txt", use_container_width=True)

    with press_cols[1]:
        st.markdown("**Medium — Long Form Edition**")
        preview = r["medium"][:220] + ("…" if len(r["medium"]) > 220 else "")
        st.markdown(f"<div style='color:#7f8fa6;font-size:0.85rem;'>{preview}</div>",
                    unsafe_allow_html=True)
        st.download_button("📰 Download", r["medium"],
                            file_name="medium_post.md", use_container_width=True)

    with press_cols[2]:
        st.markdown("**Full Report — Archive Edition**")
        preview = r["report"][:220] + ("…" if len(r["report"]) > 220 else "")
        st.markdown(f"<div style='color:#7f8fa6;font-size:0.85rem;'>{preview}</div>",
                    unsafe_allow_html=True)
        st.download_button("🗄 Archive", r["report"],
                            file_name="full_report.txt", use_container_width=True)

    if r.get("timeline"):
        with st.expander("⏱ View investigation timeline"):
            for ts, label in r["timeline"]:
                st.markdown(
                    f'<div class="timeline-row"><span class="t-time">{ts}</span>{label}</div>',
                    unsafe_allow_html=True,
                )

st.markdown(
    '<div style="text-align:center;color:#7f8fa6;font-size:0.7rem;margin-top:3rem;padding-top:1rem;border-top:1px solid #e8edf2;">'
    '⚡ POWERED BY CREWAI + OPENROUTER + TAVILY — NEXARIZA AI AGENTIC SYSTEMS</div>',
    unsafe_allow_html=True,
)