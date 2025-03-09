from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
  # Allow all origins

# Load and clean resumes dataset
df = None  # Initialize df
vectorizer = None  # Initialize vectorizer
resume_matrix = None  # Initialize resume matrix

try:
    df = pd.read_csv("technical_resumes_dataset.csv")  # Update with actual file name

    # Check if required columns exist
    if "Name" not in df.columns or "Technical Skills" not in df.columns:
        raise ValueError("CSV format incorrect: Missing 'Name' or 'Technical Skills' column")

    df["Technical Skills"] = df["Technical Skills"].fillna("")  # Fill NaN with empty string
    df["combined_text"] = df["Technical Skills"].astype(str)  # Ensure text format

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    resume_matrix = vectorizer.fit_transform(df["combined_text"])

except Exception as e:
    print(f"❌ Error loading dataset: {e}")  # Log error for debugging
    df = None

def recommend_candidates(query, top_n=5):
    """Finds the best candidates based on input query"""
    if df is None or vectorizer is None or resume_matrix is None:
        return []  # Return empty if dataset is not loaded

    try:
        query_vec = vectorizer.transform([query])  # Convert query to TF-IDF
        similarities = cosine_similarity(query_vec, resume_matrix).flatten()  # Compute similarity
        top_indices = similarities.argsort()[-top_n:][::-1]  # Get top N matching indices
        
        # Return recommended candidates
        return df.iloc[top_indices][['Name', 'Technical Skills']].to_dict(orient='records')
    except Exception as e:
        print(f"❌ Error in recommendation function: {e}")  # Log error
        return []

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Query is missing"}), 400
        
        query = data["query"]
        results = recommend_candidates(query)

        if not results:
            return jsonify({"message": "No matching candidates found"}), 200
        
        return jsonify({"candidates": results})
    except Exception as e:
        print(f"❌ API Error: {e}")  # Log API error
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
