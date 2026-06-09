# AI Data Engineering Job Market Agent

## Project Goal
Analyze Data Engineer job postings, extract skills, identify job market trends, compare candidate resumes against job requirements, and provide AI-generated recommendations.

## Directory and File Structure Explained

* **`data/`**: The central repository for all local data assets.
  * **`raw/`**: Stores unprocessed, immutable data exactly as it was collected (e.g., raw JSON responses from job board APIs, HTML dumps). **Never modify data here directly.**
  * **`processed/`**: Stores cleaned, transformed, and structured data ready for analysis, dashboarding, or model consumption.

* **`src/`**: The core Python package containing the application logic. 
  * **`ingestion/`**: Modules dedicated to acquiring data. Includes API clients, web scrapers, and scripts to fetch job postings from various platforms.
  * **`transformation/`**: Modules for data cleaning, normalization, and feature extraction. This is where raw job descriptions are parsed to extract specific skills, experience levels, and salaries.
  * **`storage/`**: Handles data persistence. Includes database models (e.g., SQLAlchemy ORM), schema definitions, and functions to load transformed data into a database or data warehouse.
  * **`agent/`**: The "brain" of the project. Contains the AI and LLM integration logic (e.g., LangChain agents) responsible for semantic matching between resumes and job requirements, generating recommendations, and identifying nuanced market trends.
  * **`dashboard/`**: The user interface layer (likely using Streamlit or a similar framework) to visualize the extracted market trends, skills distribution, and present the agent's insights to the user.

* **`tests/`**: Contains unit tests, integration tests, and data quality tests to ensure the pipeline is robust and the AI agent's outputs are consistent. Follows `pytest` conventions.

* **`docs/`**: Detailed project documentation, including architecture diagrams, API documentation, and data dictionaries.

* **`requirements.txt`**: Lists all external Python dependencies required to run the project, ensuring reproducible environments.

* **`README.md`**: This file. The entry point for the repository providing a high-level overview, project goals, and setup instructions.

## Python Best Practices Followed
- **Modularity:** Separation of concerns (Ingestion -> Transformation -> Storage -> UI/Agent).
- **Immutability of Raw Data:** Raw data is never overwritten.
- **Reproducibility:** Dependencies are pinned in `requirements.txt`.
- **Testability:** A dedicated `tests/` directory is prepared for test-driven development.

## How to Run

1. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Pipeline Scripts**:
   - Ingest data: `python src/ingestion/job_ingestion.py`
   - Extract skills: `python src/transformation/extract_skills.py`
   - Load to Snowflake (requires env vars): `python src/storage/load_to_snowflake.py`

3. **Run Dashboard & AI Agent**:
   ```bash
   streamlit run src/dashboard/app.py
   ```
   *Navigate to the AI Chat Agent page to ask questions about the market!*
