import streamlit as st
from datetime import datetime
from bot import get_context, stream_answer, escalate, get_followups, log_feedback, is_smalltalk, smalltalk_reply

st.set_page_config(page_title="Nexariza AI Support", page_icon="🎧", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] { background-color: #1e1b2e; }
[data-testid="stSidebar"] * { color: white !important; }
.stButton > button {
    border-radius: 8px;
    background-color: #6C63FF;
    color: white;
    border: none;
}
.stButton > button:hover { background-color: #5548e6; }
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat" not in st.session_state:
    cid = datetime.now().strftime("chat_%H%M%S")
    st.session_state.chats[cid] = [{"role": "assistant", "content": "Hi! Ask me anything about Nexariza AI."}]
    st.session_state.current_chat = cid
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "suggestions" not in st.session_state:          # ← NAYA
    st.session_state.suggestions = []

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🤖 Nexariza AI Support")

    st.session_state.user_name = st.text_input(
        "Your name", value=st.session_state.user_name, placeholder="Optional"
    )

    if st.button("➕ New Chat", use_container_width=True):
        cid = datetime.now().strftime("chat_%H%M%S")
        st.session_state.chats[cid] = [{"role": "assistant", "content": "Hi! Ask me anything about Nexariza AI."}]
        st.session_state.current_chat = cid
        st.session_state.suggestions = []
        st.rerun()

    st.markdown("**Recent Conversations**")
    for cid, msgs in reversed(list(st.session_state.chats.items())):
        user_msgs = [m for m in msgs if m["role"] == "user"]
        label = user_msgs[0]["content"][:28] + "..." if user_msgs else "New chat"
        if st.button(label, key=f"select_{cid}", use_container_width=True):
            st.session_state.current_chat = cid
            st.session_state.suggestions = []
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chats = {}
        cid = datetime.now().strftime("chat_%H%M%S")
        st.session_state.chats[cid] = [{"role": "assistant", "content": "Hi! Ask me anything about Nexariza AI."}]
        st.session_state.current_chat = cid
        st.session_state.suggestions = []
        st.rerun()

# ---------- Main chat ----------
st.title("🎧 Nexariza AI Support")
messages = st.session_state.chats[st.session_state.current_chat]

for i, msg in enumerate(messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant" and i > 0:
            col1, col2, _ = st.columns([1, 1, 10])
            with col1:
                if st.button("👍", key=f"up_{st.session_state.current_chat}_{i}"):
                    log_feedback(messages[i-1]["content"], msg["content"], "up")
                    st.toast("Thanks for the feedback!")
            with col2:
                if st.button("👎", key=f"down_{st.session_state.current_chat}_{i}"):
                    log_feedback(messages[i-1]["content"], msg["content"], "down")
                    st.toast("Thanks — we'll improve!")

# ---------- Chat input ----------
if question := st.chat_input("Type here..."):
    messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    if is_smalltalk(question):                                    # ← NAYA: greeting handling
        with st.chat_message("assistant"):
            answer = smalltalk_reply(question)
            st.write(answer)
        messages.append({"role": "assistant", "content": answer})
        st.session_state.suggestions = []
    else:
        context, sources, weak_match = get_context(question)

        with st.chat_message("assistant"):
            if context is None:
                answer = "I don't have enough info on this. Connecting you with our team."
                st.write(answer)
            else:
                answer = st.write_stream(stream_answer(question, context))

        messages.append({"role": "assistant", "content": answer})

        if sources:
            with st.expander("📚 Sources"):
                st.write(", ".join(sources))

        needs_escalation = (
            context is None
            or weak_match
            or any(w in question.lower() for w in ["refund", "complaint", "custom solution", "urgent", "human agent", "bug"])
            or "don't have enough information" in answer.lower()
        )

        if needs_escalation:
            esc = escalate(question, answer, user_name=st.session_state.user_name or "Anonymous")
            st.warning("This needs human attention.")
            st.markdown(f"""
            **Reference:** `{esc['ref_id']}`

            📧 [Email us]({"mailto:" + esc['email']})  
            💬 [Chat on WhatsApp]({esc['whatsapp_link']})
            """)

        # ← CHANGE: sirf session_state mein store karo, yahan render mat karo
        st.session_state.suggestions = get_followups(question, answer) if context is not None else []

# ---------- Suggested follow-ups (ab block ke BAHAR, har run mein render hota hai) ----------
if st.session_state.suggestions:
    st.caption("You might also ask:")
    cols = st.columns(len(st.session_state.suggestions))
    for idx, s in enumerate(st.session_state.suggestions):
        if cols[idx].button(s, key=f"sugg_{st.session_state.current_chat}_{idx}"):
            st.session_state.suggestions = []
            st.session_state["pending_question"] = s
            st.rerun()

# ---------- Handle suggestion click ----------
if "pending_question" in st.session_state:
    q = st.session_state.pop("pending_question")
    messages.append({"role": "user", "content": q})

    if is_smalltalk(q):
        ans = smalltalk_reply(q)
    else:
        ctx, srcs, weak = get_context(q)
        with st.spinner("Thinking..."):
            ans = "".join(list(stream_answer(q, ctx))) if ctx else "I don't have enough info on this."

    messages.append({"role": "assistant", "content": ans})
    st.rerun()