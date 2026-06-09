import pandas as pd
import os

def ingest_job_postings(file_path="data/raw/job_postings.csv"):
    """
    Reads job postings from a CSV file, validates required columns,
    and returns a pandas DataFrame.
    """
    print(f"Loading data from {file_path}...")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} was not found.")
        
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Define the required columns that our downstream code expects
    required_columns = ["job_title", "company", "location", "description"]
    
    # Validate that all required columns are present in the DataFrame
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in the dataset: {missing_columns}")
        
    print(f"Successfully loaded {len(df)} job postings.")
    return df

if __name__ == "__main__":
    # Test the ingestion function
    try:
        df = ingest_job_postings()
        print(df.head())
    except Exception as e:
        print(f"Error during ingestion: {e}")
