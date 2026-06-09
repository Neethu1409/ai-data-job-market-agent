import pandas as pd
import os

class JobMarketAgent:
    """
    A rule-based agent that analyzes processed job market data.
    Provides answers about skills, locations, and recommendations 
    without requiring external LLM APIs.
    """
    
    def __init__(self, data_path="data/processed/jobs_with_skills.csv"):
        self.data_path = data_path
        self.df = None
        self.load_data()
        
    def load_data(self):
        """Loads the processed data into a DataFrame."""
        if os.path.exists(self.data_path):
            try:
                self.df = pd.read_csv(self.data_path)
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            print(f"Warning: Data file {self.data_path} not found.")
            
    def get_top_skills(self, top_n=5):
        """Returns the top N most frequently mentioned skills."""
        if self.df is None or 'extracted_skills' not in self.df.columns:
            return "Data not available to analyze top skills."
            
        all_skills = []
        for skills_str in self.df['extracted_skills'].dropna():
            # Split by comma and strip whitespace
            skills = [s.strip() for s in str(skills_str).split(',') if s.strip()]
            all_skills.extend(skills)
            
        if not all_skills:
            return "No skills found in the dataset."
            
        # Count frequencies
        skill_counts = pd.Series(all_skills).value_counts()
        
        top_skills = skill_counts.head(top_n)
        result = "Top Skills:\n"
        for skill, count in top_skills.items():
            result += f"- {skill}: {count} postings\n"
            
        return result
        
    def get_jobs_by_location(self, location):
        """Returns jobs matching the specified location."""
        if self.df is None or 'location' not in self.df.columns:
            return "Data not available to analyze locations."
            
        # Case-insensitive search for location
        matches = self.df[self.df['location'].str.contains(location, case=False, na=False)]
        
        if matches.empty:
            return f"No jobs found in {location}."
            
        result = f"Found {len(matches)} jobs in {location}:\n"
        # Return top 3 as examples to not overwhelm
        for _, row in matches.head(3).iterrows():
            result += f"- {row.get('job_title', 'Unknown Title')} at {row.get('company', 'Unknown Company')}\n"
            
        if len(matches) > 3:
            result += f"... and {len(matches) - 3} more."
            
        return result
        
    def get_resume_missing_skills(self, my_skills):
        """Compares user's skills against top market skills."""
        if isinstance(my_skills, str):
            my_skills = [s.strip().lower() for s in my_skills.split(',')]
        else:
            my_skills = [s.lower() for s in my_skills]
            
        # Get top 10 market skills
        if self.df is None or 'extracted_skills' not in self.df.columns:
            return "Data not available to compare skills."
            
        all_skills = []
        for skills_str in self.df['extracted_skills'].dropna():
            skills = [s.strip().lower() for s in str(skills_str).split(',') if s.strip()]
            all_skills.extend(skills)
            
        if not all_skills:
            return "Market skill data is currently unavailable."
            
        top_market_skills = pd.Series(all_skills).value_counts().head(10).index.tolist()
        
        missing = [skill.title() for skill in top_market_skills if skill not in my_skills]
        
        if not missing:
            return "Great job! You have all the top 10 in-demand skills."
            
        result = "Based on current market trends, you should consider learning:\n"
        for skill in missing:
            result += f"- {skill}\n"
            
        return result
        
    def get_learning_recommendations(self):
        """Provides general learning recommendations."""
        return (
            "Learning Recommendations for Data Engineers:\n"
            "1. SQL & Python are foundational. Ensure you master them.\n"
            "2. Cloud Platforms (AWS, Azure, GCP) are heavily requested.\n"
            "3. Distributed Computing tools like Spark/PySpark add significant value.\n"
            "4. Understand orchestration tools like Airflow.\n"
            "5. Build personal projects to demonstrate practical experience."
        )
        
    def ask(self, query):
        """
        Simple rule-based router that calls the right method based on keywords in the query.
        """
        query_lower = query.lower()
        
        if "top skills" in query_lower or "most demanded skills" in query_lower:
            return self.get_top_skills()
            
        elif "jobs in" in query_lower or "location" in query_lower:
            # Simple extraction heuristic for location
            parts = query_lower.split("jobs in")
            if len(parts) > 1:
                location = parts[1].strip(" ?.")
                return self.get_jobs_by_location(location)
            return "Please specify a location (e.g., 'What are jobs in New York?')."
            
        elif "resume" in query_lower or "my skills" in query_lower or "missing" in query_lower:
            # Simple heuristic: assume they mentioned their skills after a colon
            if ":" in query_lower:
                my_skills = query_lower.split(":")[1].strip()
                return self.get_resume_missing_skills(my_skills)
            return "Please provide your skills like this: 'Check my resume: python, sql, aws'."
            
        elif "learn" in query_lower or "recommendations" in query_lower or "path" in query_lower:
            return self.get_learning_recommendations()
            
        else:
            return (
                "I am a rule-based AI Career Agent. You can ask me:\n"
                "- 'What are the top skills?'\n"
                "- 'Are there jobs in [Location]?'\n"
                "- 'Check my resume: [Skill 1, Skill 2]'\n"
                "- 'What are some learning recommendations?'"
            )

if __name__ == "__main__":
    # Test the agent
    agent = JobMarketAgent()
    print(agent.ask("What are the top skills?"))
    print("-" * 20)
    print(agent.ask("What are some learning recommendations?"))
