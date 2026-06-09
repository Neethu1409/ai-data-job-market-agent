import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Job Trends", page_icon="📈", layout="wide")

st.title("📈 Job Trends")

st.markdown("Explore trends in job postings across different dimensions.")

tab1, tab2 = st.tabs(["Salary Distribution", "Top Locations"])

with tab1:
    st.subheader("Salary Distribution for Data Engineers")
    # Mock data for demonstration purposes
    chart_data = pd.DataFrame(
        np.random.normal(130000, 20000, size=(100, 1)),
        columns=["Salary ($)"]
    )
    st.bar_chart(chart_data)

with tab2:
    st.subheader("Top Locations Hiring")
    loc_data = pd.DataFrame({
        "Location": ["Remote", "New York", "San Francisco", "Seattle", "Austin"],
        "Count": [450, 210, 180, 120, 95]
    })
    st.bar_chart(loc_data.set_index("Location"))
