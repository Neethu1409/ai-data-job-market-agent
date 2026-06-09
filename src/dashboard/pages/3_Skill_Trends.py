import streamlit as st
import pandas as pd

st.set_page_config(page_title="Skill Trends", page_icon="🛠️", layout="wide")

st.title("🛠️ Skill Trends")

st.markdown("What are the most requested skills in the data engineering market today?")

# Mock data
skills_data = pd.DataFrame({
    "Skill": ["Python", "SQL", "Spark", "AWS", "Snowflake", "Airflow", "Kafka"],
    "Demand (%)": [85, 80, 65, 60, 55, 45, 30]
}).sort_values("Demand (%)", ascending=False)

st.bar_chart(skills_data.set_index("Skill"))

st.info("💡 **Insight:** Python and SQL remain the absolute foundational skills, while Cloud (AWS) and Modern Data Stack tools (Snowflake) are highly desired.")
