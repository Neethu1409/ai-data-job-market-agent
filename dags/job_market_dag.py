"""
job_market_dag.py

Apache Airflow DAG to orchestrate the AI Data Engineering Job Market Agent pipeline.
This defines the exact sequence of events from data ingestion to AI reporting.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments dictate how tasks behave (retries, timeouts, owners)
default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2, # Retry twice if a task fails
    'retry_delay': timedelta(minutes=5),
}

# --- Placeholder Python Functions for tasks not yet fully scripted ---

def extract_job_data(**kwargs):
    """Hits job board APIs or runs scrapers to dump data into data/raw/"""
    print("Executing extraction logic from src/ingestion/...")
    print("Successfully downloaded 500 new job postings to data/raw/")

def load_to_snowflake(**kwargs):
    """Pushes the processed CSVs into the Snowflake Staging tables and runs MERGE."""
    print("Connecting to Snowflake...")
    print("Executing COPY INTO and MERGE statements...")
    print("Successfully loaded Fact and Dimension tables in Analytics schema.")

def run_ai_analysis(**kwargs):
    """Invokes the LangChain AI agent to evaluate candidate resumes against new jobs."""
    print("Initializing LangChain Agent...")
    print("Running Resume Gap Analysis and storing matching scores...")

def generate_report(**kwargs):
    """Generates a summary report (e.g., an email or Slack notification) of the pipeline run."""
    print("Generating pipeline summary report...")
    print("Report sent: 'Analyzed 500 jobs. Python demand is up 2% today.'")

# --- DAG Definition ---

with DAG(
    'ai_job_market_agent_pipeline',
    default_args=default_args,
    description='End-to-end pipeline for the AI Job Market Agent',
    schedule_interval='@daily', # Run once a day at midnight
    catchup=False, # Don't backfill historical missing runs automatically
    tags=['job_market', 'ai', 'data_engineering'],
) as dag:

    # Task 1: Extract Job Data
    # Uses a PythonOperator since ingestion usually relies heavily on Python requests/BeautifulSoup
    t1_extract_data = PythonOperator(
        task_id='extract_job_data',
        python_callable=extract_job_data,
    )

    # Task 2: Clean Data
    # Uses BashOperator to trigger the standalone Pandas script we wrote earlier.
    t2_clean_data = BashOperator(
        task_id='clean_data',
        bash_command='python src/transformation/clean_jobs.py',
    )

    # Task 3: Extract Skills
    # Trigger the Regex extraction module we built.
    t3_extract_skills = BashOperator(
        task_id='extract_skills',
        bash_command='python src/transformation/extract_skills.py',
    )

    # Task 4: Load into Snowflake
    t4_load_snowflake = PythonOperator(
        task_id='load_snowflake',
        python_callable=load_to_snowflake,
    )

    # Task 5: Run AI Analysis
    t5_run_ai = PythonOperator(
        task_id='run_ai_analysis',
        python_callable=run_ai_analysis,
    )

    # Task 6: Generate Final Report
    t6_generate_report = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report,
    )

    # --- Define the Workflow (Dependencies) ---
    # The bitshift operator (>>) explicitly defines the order of execution.
    # The DAG will fail if a downstream task attempts to run before an upstream task finishes successfully.
    
    t1_extract_data >> t2_clean_data >> t3_extract_skills >> t4_load_snowflake >> t5_run_ai >> t6_generate_report
