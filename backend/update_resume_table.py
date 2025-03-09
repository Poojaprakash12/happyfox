import sqlite3

# Connect to database
conn = sqlite3.connect("resumes.db")
cursor = conn.cursor()

# Add the 'resume_text' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE resumes ADD COLUMN resume_text TEXT")
    print("Column 'resume_text' added successfully!")
except sqlite3.OperationalError:
    print("Column 'resume_text' already exists.")

# Commit and close
conn.commit()
conn.close()
