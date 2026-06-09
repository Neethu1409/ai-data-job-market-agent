import streamlit as st

st.set_page_config(page_title="Resume Gap Analysis", page_icon="📄", layout="wide")

st.title("📄 Resume Gap Analysis")

st.markdown("Upload your resume to see how you stack up against current job requirements.")

uploaded_file = st.file_uploader("Upload your resume (PDF/TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")
    
    with st.spinner("Analyzing your resume against market trends..."):
        # Mock analysis delay
        import time
        time.sleep(1.5)
        
    st.subheader("Analysis Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Skills Matched")
        st.write("- Python\n- SQL\n- Airflow")
        
    with col2:
        st.markdown("### ❌ Skills Missing (High Demand)")
        st.write("- Snowflake\n- PySpark\n- Kafka")
        
    st.divider()
    st.subheader("Personalized Learning Recommendations")
    st.write("1. **Snowflake**: Take the 'Snowflake SnowPro Core Certification' path.")
    st.write("2. **PySpark**: Focus on distributed data processing concepts using Databricks Community Edition.")
