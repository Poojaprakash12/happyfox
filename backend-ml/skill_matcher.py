import os
import PyPDF2
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Directory where resumes are stored
RESUME_DIR = "../backend/uploads/"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_skills(text):
    """Extract relevant skills from text using NLP."""
    doc = nlp(text.lower())
    skills = [token.text for token in doc if token.is_alpha]
    return " ".join(skills)

def get_resume_data():
    """Extract text from all stored resumes."""
    resume_texts = []
    resume_names = []
    
    for file in os.listdir(RESUME_DIR):
        if file.endswith(".pdf"):
            file_path = os.path.join(RESUME_DIR, file)
            text = extract_text_from_pdf(file_path)
            processed_text = extract_skills(text)
            resume_texts.append(processed_text)
            resume_names.append(file)
    
    return resume_texts, resume_names

def match_skills(job_description):
    """Match resumes to the given job description using TF-IDF and cosine similarity."""
    resume_texts, resume_names = get_resume_data()
    
    if not resume_texts:
        return "No resumes found."

    # Include job description in the comparison
    all_texts = [job_description] + resume_texts
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Compute similarity
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Sort resumes by similarity
    sorted_indices = np.argsort(similarities)[::-1]
    
    matched_resumes = [(resume_names[i], similarities[i]) for i in sorted_indices]
    return matched_resumes

if __name__ == "__main__":
    job_desc = input("Enter job description: ")
    results = match_skills(job_desc)

    for name, score in results:
        print(f"{name}: {score:.2f}")
