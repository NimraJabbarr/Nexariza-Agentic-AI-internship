import streamlit as st
import pandas as pd
from bot import load_escalations, update_escalation_status

st.set_page_config(page_title="Escalations", page_icon="📋", layout="wide")
st.title("📋 Escalation Dashboard")

escalations = load_escalations()

if not escalations:
    st.info("No escalations yet.")
else:
    df = pd.DataFrame(escalations)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Escalations", len(df))
    col2.metric("Pending", len(df[df["status"] == "pending"]))
    col3.metric("Resolved", len(df[df["status"] == "resolved"]))

    st.divider()

    filter_status = st.selectbox("Filter", ["All", "pending", "resolved"])
    filtered = df if filter_status == "All" else df[df["status"] == filter_status]

    for _, row in filtered[::-1].iterrows():
        with st.expander(f"{row['id']} — {row['user_name']} — {row['status'].upper()}"):
            st.write(f"**Question:** {row['question']}")
            st.write(f"**Bot Answer:** {row['bot_answer']}")
            st.write(f"**Contact:** {row.get('user_contact', 'N/A')}")
            st.write(f"**Time:** {row['timestamp']}")

            if row["status"] == "pending":
                if st.button("✅ Mark Resolved", key=f"resolve_{row['id']}"):
                    update_escalation_status(row["id"], "resolved")
                    st.rerun()