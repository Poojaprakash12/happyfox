import pandas as pd
import spacy
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load resumes
df = pd.read_csv("technical_resumes_dataset.csv")  # Adjust path if needed
print("Columns in CSV:", df.columns)  # Debugging to check column names

# Ensure 'Technical Skills' column exists and has no NaN values
df['Technical Skills'].fillna("", inplace=True)
df['combined_text'] = df[['Technical Skills']].astype(str).apply(lambda x: ' '.join(x), axis=1)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Vectorize resume text
vectorizer = TfidfVectorizer(stop_words='english')
resume_matrix = vectorizer.fit_transform(df['combined_text'])

def extract_skills_from_query(query):
    """Extracts key skills from user input using NLP"""
    doc = nlp(query)
    skills = [token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN", "ADJ"]]
    return skills

def recommend_candidates(query, top_n=5):
    """Finds the best candidates based on user query"""
    skills_extracted = extract_skills_from_query(query)
    print("Extracted Skills:", skills_extracted)  # Debugging

    query_text = " ".join(skills_extracted)  # Create refined query
    query_vec = vectorizer.transform([query_text])  # Convert to TF-IDF
    similarities = cosine_similarity(query_vec, resume_matrix).flatten()  # Compute similarity

    top_indices = similarities.argsort()[-top_n:][::-1]  # Get top N matches
    result = df.iloc[top_indices][['Name', 'Technical Skills']]

    # Convert to JSON
    return json.dumps(result.to_dict(orient="records"))

# Example Usage
if __name__ == "__main__":
    query = "I am looking for a Python developer with ML skills"
    recommended_json = recommend_candidates(query)
    print(recommended_json)  # JSON Output
