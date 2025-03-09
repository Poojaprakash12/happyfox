import pandas as pd

# Load the dataset
df = pd.read_csv("technical_resumes_dataset.csv")  # Adjust path if needed

# Check available columns
print("Columns in dataset:", df.columns)

# Extract Name and Skills (adjust column names based on actual dataset)
extracted_data = df[['Name', 'Technical Skills']]  # Update with correct column names

# Save extracted data to CSV
output_file = "extracted_names_skills.csv"
extracted_data.to_csv(output_file, index=False)

print(f"Extracted data saved to {output_file}")
