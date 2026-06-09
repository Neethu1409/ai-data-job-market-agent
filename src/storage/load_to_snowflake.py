import os
import pandas as pd

# Try importing snowflake connector; handle error gracefully if not installed
try:
    import snowflake.connector
    from snowflake.connector.pandas_tools import write_pandas
except ImportError:
    print("Warning: snowflake-connector-python is not installed.")
    print("Run `pip install snowflake-connector-python[pandas]` to install it.")

def load_data_to_snowflake(file_path="data/processed/jobs_with_skills.csv", table_name="JOB_POSTINGS"):
    """
    Reads processed job data from a CSV file and loads it into a Snowflake table.
    Expects Snowflake credentials to be set as environment variables.
    """
    print(f"Reading data from {file_path}...")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} was not found.")
        return
        
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    print("Connecting to Snowflake...")
    try:
        # Connect to Snowflake using environment variables for security
        conn = snowflake.connector.connect(
            user=os.environ.get('SNOWFLAKE_USER'),
            password=os.environ.get('SNOWFLAKE_PASSWORD'),
            account=os.environ.get('SNOWFLAKE_ACCOUNT'),
            warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
            database=os.environ.get('SNOWFLAKE_DATABASE'),
            schema=os.environ.get('SNOWFLAKE_SCHEMA')
        )
        
        # Ensure table names are uppercase for Snowflake
        table_name_upper = table_name.upper()
        
        print(f"Writing {len(df)} rows to Snowflake table {table_name_upper}...")
        
        # write_pandas is an efficient way to write a DataFrame to a Snowflake table
        success, nchunks, nrows, _ = write_pandas(conn, df, table_name_upper)
        
        if success:
            print(f"Successfully loaded {nrows} rows into {table_name_upper}.")
        else:
            print("Failed to load data into Snowflake.")
            
    except snowflake.connector.errors.ProgrammingError as e:
        print(f"Snowflake Programming Error: {e}")
    except KeyError as e:
        print(f"Missing environment variable for Snowflake connection: {e}")
        print("Please set SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, etc.")
    except Exception as e:
        print(f"An unexpected error occurred during Snowflake load: {e}")
    finally:
        # Always make sure to close the connection
        if 'conn' in locals() and conn:
            conn.close()
            print("Snowflake connection closed.")

if __name__ == "__main__":
    # Test the loader function
    load_data_to_snowflake()
