import sys
import json
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define a comprehensive list of technical skills
TECH_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust", "php", "swift", "kotlin",
    # Web Development
    "html", "css", "react", "angular", "vue", "node", "express", "django", "flask", "spring", "bootstrap",
    "next.js", "graphql", "rest api", "tailwind", "jquery", "sass",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "nosql", "oracle", "firebase", "dynamodb", "redis", "cassandra",
    "sqlite", "sql server",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform", "ansible", "devops", "ci/cd",
    "gitlab", "prometheus", "grafana", "elk", "linux", "bash", "nginx", "apache",
    # Data Science & AI
    "machine learning", "deep learning", "ai", "data science", "tensorflow", "pytorch", "nlp", "computer vision",
    "data analysis", "statistics", "pandas", "numpy", "scikit-learn", "big data", "hadoop", "spark",
    "keras", "matplotlib", "seaborn", "nltk", "opencv",
    # Mobile Development
    "android", "ios", "react native", "flutter", "xamarin", "mobile development", "jetpack compose",
    # Other Technical Areas
    "blockchain", "cybersecurity", "ethical hacking", "penetration testing", "networking", "iot",
    "embedded systems", "game development", "unity", "unreal engine", "ar/vr", "qa", "testing",
    "selenium", "git", "agile", "scrum", "microservices", "restful api", "graphql", "jira", "confluence",
    "ui/ux", "figma", "adobe xd", "jest", "cypress"
]

def is_valid_tech_query(query):
    """Check if the query contains at least one technical skill"""
    query_lower = query.lower()
    
    # Check if any tech skill is in the query
    for skill in TECH_SKILLS:
        if skill in query_lower:
            return True
            
    # Check for common tech skill patterns
    tech_patterns = [
        r'\b(front|back)[\s-]?end\b',  # front-end, backend
        r'\b(full[\s-]?stack)\b',       # full-stack
        r'\b(dev(eloper)?|engineer|architect)\b',  # developer, engineer
        r'\b(data[\s-]?(engineer|scientist|analyst))\b',  # data engineer/scientist
        r'\bsde\b',                     # SDE
        r'\bml\b',                      # ML
        r'\bai\b',                      # AI
        r'\bui/ux\b'                    # UI/UX
    ]
    
    for pattern in tech_patterns:
        if re.search(pattern, query_lower):
            return True
    
    return False

def match_resumes(query):
    """Match resumes based on the query"""
    # First check if the query is valid
    if not is_valid_tech_query(query):
        return json.dumps({
            "error": "Invalid input. Please enter technical skills (e.g., Python, Java, Machine Learning)."
        })
    
    try:
        # Load the dataset
        df = pd.read_csv("technical_resumes_dataset.csv")
        
        # Extract skills from query
        query_skills = [skill for skill in TECH_SKILLS if skill in query.lower()]
        
        # If no specific skills were found but query was valid (e.g., "developer")
        if not query_skills:
            query_skills = [query.lower()]
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # Ensure Technical Skills column exists and is string type
        if "Technical Skills" not in df.columns:
            return json.dumps({
                "error": "Dataset missing 'Technical Skills' column."
            })
        
        # Fill NaN values and convert to string
        df["Technical Skills"] = df["Technical Skills"].fillna("").astype(str)
        
        # Create document-term matrix
        skills_matrix = vectorizer.fit_transform(df["Technical Skills"])
        
        # Transform query
        query_vector = vectorizer.transform([query])
        
        # Calculate similarity
        similarity_scores = cosine_similarity(query_vector, skills_matrix).flatten()
        
        # Get top 5 matches
        top_indices = similarity_scores.argsort()[-5:][::-1]
        
        # Get results
        results = []
        for idx in top_indices:
            if similarity_scores[idx] > 0.01:  # Only include if there's some similarity
                results.append({
                    "Name": df.iloc[idx]["Name"],
                    "Technical Skills": df.iloc[idx]["Technical Skills"]
                })
        
        # Return results as a clean JSON array
        return json.dumps(results)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return json.dumps({
            "error": f"An error occurred: {str(e)}",
            "details": error_details
        })

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        result = match_resumes(query)
        print(result)
    else:
        print(json.dumps({
            "error": "No query provided."
        }))
