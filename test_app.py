import streamlit as st

st.set_page_config(
    page_title="Smart City Test",
    page_icon="🏙️"
)

st.title("🏙️ Smart City Test")

st.header("👨‍💼 Admin Dashboard")

st.metric("📊 Total", 7)
st.metric("⏳ Pending", 7)

st.subheader("🔎 Search & Filter")

search = st.text_input("🔍 Search Complaint")

filter_status = st.selectbox(
    "📌 Filter by Status",
    ["All", "Pending", "In Progress", "Resolved"]
)

st.write("Test completed successfully.")