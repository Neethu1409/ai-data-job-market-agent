"""
extract_skills.py

Module responsible for parsing job descriptions and extracting predefined 
Data Engineering and AI skills using regular expressions.
"""

import re
from typing import List

class SkillExtractor:
    """
    Extracts a predefined list of technical skills from text.
    Uses regex with word boundaries to ensure accurate matching.
    """
    
    def __init__(self):
        # The definitive list of skills we want to track in the job market
        self.target_skills = [
            "Python", "SQL", "PySpark", "Spark", "Snowflake", 
            "Databricks", "Airflow", "Kafka", "Hadoop", "Hive", 
            "AWS", "Azure", "GCP", "Docker", "OpenAI", "LangChain"
        ]
        
        # Pre-compile the regex pattern for performance (especially useful when running on thousands of rows).
        # We use \b to specify word boundaries. This prevents false positives.
        # For example, searching for "AWS" with word boundaries won't accidentally match "flAWS".
        escaped_skills = [re.escape(skill) for skill in self.target_skills]
        
        # The resulting pattern looks like: \b(Python|SQL|PySpark|...)\b
        pattern_str = r'\b(' + '|'.join(escaped_skills) + r')\b'
        
        # re.IGNORECASE ensures we match "python", "PYTHON", or "Python"
        self.pattern = re.compile(pattern_str, re.IGNORECASE)

    def extract_skills(self, text: str) -> List[str]:
        """
        Parses the input job description and returns a list of found skills.
        
        Args:
            text (str): The raw job description text.
            
        Returns:
            List[str]: A list of standard formatted skills found in the text.
        """
        if not isinstance(text, str) or not text.strip():
            return []
            
        # Find all occurrences of the skills in the text
        matches = self.pattern.findall(text)
        
        # The regex match might return variations in casing (e.g., "python", "PYTHON").
        # We want to normalize the output to perfectly match our `target_skills` casing.
        # First, convert all found matches to a set of lowercase strings to remove duplicates.
        found_lower = set(match.lower() for match in matches)
        
        # Then, iterate through our master list and select the ones that were found.
        # This guarantees the output is always consistently capitalized (e.g., "PySpark" instead of "pyspark").
        extracted = [skill for skill in self.target_skills if skill.lower() in found_lower]
        
        return extracted


if __name__ == "__main__":
    import pandas as pd
    import os
    
    print("Initializing SkillExtractor...")
    extractor = SkillExtractor()
    
    input_file = "data/raw/job_postings.csv"
    output_file = "data/processed/jobs_with_skills.csv"
    
    print(f"Reading data from {input_file}...")
    try:
        # Read the raw job postings
        df = pd.read_csv(input_file)
        
        # Ensure 'description' column exists and replace NaNs
        if 'description' not in df.columns:
            print("Error: 'description' column missing from input data.")
        else:
            df['description'] = df['description'].fillna("")
            
            print("Extracting skills from job descriptions...")
            # Apply the extraction method and join the list into a comma-separated string
            df['extracted_skills'] = df['description'].apply(
                lambda desc: ", ".join(extractor.extract_skills(desc))
            )
            
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            print(f"Saving processed data to {output_file}...")
            df.to_csv(output_file, index=False)
            print("Successfully saved processed data!")
            
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
