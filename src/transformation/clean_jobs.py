"""
clean_jobs.py

This module contains a data cleaning pipeline for job postings.
It utilizes Pandas to read raw job data, clean and standardize it,
and save the processed output for downstream analysis or agent consumption.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional

# Configure basic logging for visibility into the pipeline's progress
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobDataCleaner:
    """
    A data pipeline class designed to clean and process raw job postings data.
    Follows Data Engineering best practices by encapsulating transformation logic.
    """
    
    def __init__(self, input_path: str | Path, output_path: str | Path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.df: Optional[pd.DataFrame] = None

    def read_data(self) -> None:
        """1. Reads raw job postings from a CSV file into a Pandas DataFrame."""
        logger.info(f"Reading data from {self.input_path}")
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info(f"Loaded {len(self.df)} rows from raw data.")
        except FileNotFoundError:
            logger.error(f"File not found: {self.input_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading {self.input_path}: {e}")
            raise

    def remove_duplicates(self) -> None:
        """3. Removes duplicate job postings based on common identifiers."""
        if self.df is None:
            raise ValueError("Data not loaded. Call read_data() first.")
        
        initial_count = len(self.df)
        
        # Define columns that usually identify a unique job posting. 
        # If these columns exist in the raw data, use them to find duplicates.
        subset_cols = ['title', 'company', 'location', 'description'] 
        cols_to_check = [c for c in subset_cols if c in self.df.columns] or None
        
        # keep='first' retains the first occurrence and drops subsequent ones
        self.df.drop_duplicates(subset=cols_to_check, keep='first', inplace=True)
        logger.info(f"Removed {initial_count - len(self.df)} duplicate rows.")

    def handle_null_values(self) -> None:
        """4. Handles missing (null) values by filling or dropping them."""
        if self.df is None:
            raise ValueError("Data not loaded.")
        
        initial_count = len(self.df)
        
        # Step A: Drop rows where absolutely critical fields are missing
        critical_cols = ['title', 'description']
        cols_to_check = [c for c in critical_cols if c in self.df.columns]
        if cols_to_check:
            self.df.dropna(subset=cols_to_check, inplace=True)
            
        # Step B: Fill non-critical missing values with a default string
        fill_cols = ['location', 'company', 'salary']
        for col in fill_cols:
            if col in self.df.columns:
                # Using fillna to replace NaN/None with "Not Specified"
                self.df[col] = self.df[col].fillna("Not Specified")
                
        logger.info(f"Dropped {initial_count - len(self.df)} rows due to nulls in critical fields.")

    def standardize_text(self) -> None:
        """5. Standardizes text fields (lowercase, removing extra whitespace, etc.)."""
        if self.df is None:
            raise ValueError("Data not loaded.")
        
        # Dynamically find all text-based columns
        text_cols = self.df.select_dtypes(include=['object', 'string']).columns
        
        for col in text_cols:
            # Convert to string (to be safe), lowercase, and strip leading/trailing spaces
            self.df[col] = self.df[col].astype(str).str.lower().str.strip()
            # Replace multiple consecutive spaces with a single space using regex
            self.df[col] = self.df[col].str.replace(r'\s+', ' ', regex=True)
            
        logger.info("Standardized text fields (converted to lowercase, stripped extra whitespace).")

    def save_processed_data(self) -> None:
        """6. Saves the cleaned DataFrame to the processed data directory."""
        if self.df is None:
            raise ValueError("Data not loaded.")
        
        # Ensure the output directory exists before attempting to save
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving {len(self.df)} processed rows to {self.output_path}")
        # Save to CSV without the Pandas index column
        self.df.to_csv(self.output_path, index=False)
        logger.info("Data saved successfully.")

    def run_pipeline(self) -> None:
        """Executes the full data cleaning pipeline in the correct sequence."""
        logger.info("Starting data cleaning pipeline...")
        self.read_data()
        self.remove_duplicates()
        self.handle_null_values()
        self.standardize_text()
        self.save_processed_data()
        logger.info("Data cleaning pipeline completed.")


if __name__ == "__main__":
    # --- Example execution & demonstration ---
    
    # Defining paths relative to the script location
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    RAW_DATA_FILE = PROJECT_ROOT / "data" / "raw" / "job_postings.csv"
    PROCESSED_DATA_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_job_postings.csv"
    
    # 1. Create a dummy raw CSV for testing if it doesn't already exist
    if not RAW_DATA_FILE.exists():
        logger.info("Raw data file not found. Creating a dummy file for demonstration...")
        RAW_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Creating dummy data with duplicates, nulls, and messy text
        dummy_data = pd.DataFrame({
            "title": [" Data Engineer ", "Data engineer", "Senior Data Engineer", None, "Data Scientist"],
            "company": ["Tech Corp", "Tech Corp", "Data Inc", "Unknown", None],
            "location": ["Remote", "remote", "New York", "Remote", "SF"],
            "description": ["Must know Python.", "Must know Python.", "Looking for PySpark expert.", "No description", "Data stuff"],
            "salary": ["$100k", "$100k", None, "$120k", "$150k"]
        })
        dummy_data.to_csv(RAW_DATA_FILE, index=False)

    # 2. Instantiate the cleaner and run the pipeline
    cleaner = JobDataCleaner(input_path=RAW_DATA_FILE, output_path=PROCESSED_DATA_FILE)
    cleaner.run_pipeline()
