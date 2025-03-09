import sqlite3

# Connect to database
conn = sqlite3.connect("resumes.db")
cursor = conn.cursor()

# Get column names
cursor.execute("PRAGMA table_info(resumes)")
columns = cursor.fetchall()

# Print column names
print("Table structure of 'resumes':")
for col in columns:
    print(col)

conn.close()
