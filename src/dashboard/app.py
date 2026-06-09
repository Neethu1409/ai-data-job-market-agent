import streamlit as st

st.set_page_config(
    page_title="AI Data Engineering Job Market Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Engineering Job Market Agent")

st.markdown("""
Welcome to the AI Data Engineering Job Market Agent Dashboard!

Use the sidebar to navigate through different sections:
- **Overview**: High-level metrics of the job market.
- **Job Trends**: Analyze job postings by location, salary, and company.
- **Skill Trends**: Discover the most in-demand Data Engineering skills.
- **Resume Gap Analysis**: Compare your resume against job requirements.
- **AI Chat Agent**: Talk to our AI to get personalized career advice.
""")

st.info("👈 Select a page from the sidebar to begin.")
