import streamlit as st

st.set_page_config(page_title="Overview", page_icon="🌍", layout="wide")

st.title("🌍 Market Overview")

st.markdown("### High-Level Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Jobs Analyzed", "1,245", "+12 this week")
col2.metric("Avg Salary (Data Eng)", "$135,000", "+$2k yoy")
col3.metric("Top Skill", "Python", "85% of jobs")
col4.metric("Remote Jobs", "45%", "-2% this month")

st.divider()

st.markdown("### Recent Job Postings")
# In a real app, this would be a pd.DataFrame loaded from Snowflake or CSV
st.table({
    "Title": ["Senior Data Engineer", "Data Engineer II", "Analytics Engineer", "Data Platform Engineer"],
    "Company": ["Tech Corp", "Data Inc", "Startup Co", "Enterprise LLC"],
    "Location": ["Remote", "New York, NY", "San Francisco, CA", "Remote"],
    "Posted": ["2 hours ago", "5 hours ago", "1 day ago", "2 days ago"]
})
