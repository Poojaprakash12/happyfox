import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("resumes.db")
cursor = conn.cursor()

# Fetch all resumes from the database
cursor.execute("SELECT * FROM resumes")
resumes = cursor.fetchall()

# Get column names
columns = [desc[0] for desc in cursor.description]

# Convert to DataFrame
df = pd.DataFrame(resumes, columns=columns)

# Save to CSV file
df.to_csv("resumes_data.csv", index=False)

# Close the connection
conn.close()

print("✅ Resume data successfully extracted and saved to resumes_data.csv!")
