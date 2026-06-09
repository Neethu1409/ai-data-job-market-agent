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
    # --- Example Usage & Testing ---
    extractor = SkillExtractor()
    
    sample_jd_1 = """
    We are looking for a Data Engineer with strong Python and sql skills. 
    Experience with cloud platforms like AWS or gcp is a must. 
    Bonus points if you have worked with Snowflake or DataBricks and understand airflow.
    """
    
    sample_jd_2 = """
    Requires 5+ years of experience. Must be proficient in PySpark, Kafka, and Docker. 
    Recent experience building AI agents using LangChain and OpenAI APIs is highly preferred.
    """
    
    print("Extracting from Job Description 1:")
    print(extractor.extract_skills(sample_jd_1))
    print("-" * 40)
    print("Extracting from Job Description 2:")
    print(extractor.extract_skills(sample_jd_2))
