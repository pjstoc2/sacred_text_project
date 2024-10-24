import pandas as pd
from collections import Counter
import json
import os

# Function to clean up the file path
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')  # Remove any surrounding quotes
    return cleaned_path.replace("\\", "\\\\")

# Prompt for the CSV file location
entity_file_path = input("Enter the path to the entity CSV file (e.g., 'C:/path/to/entities.csv'): ")
entity_file_path = clean_file_path(entity_file_path)

# Prompt for the text file location
text_file_path = input("Enter the path to the sacred text file (e.g., 'C:/path/to/sacred_text.txt'): ")
text_file_path = clean_file_path(text_file_path)

# Load the CSV file, ensuring no values are treated as NaN
df = pd.read_csv(entity_file_path, encoding='utf-8')

# Identify problematic rows (non-string values in 'Entity' column)
problematic_rows = df[~df['Entity'].apply(lambda x: isinstance(x, str))]

# If there are problematic rows, print them and alert the user
if not problematic_rows.empty:
    print("Problematic rows found in the CSV file:")
    print(problematic_rows)
else:
    print("No problematic rows found.")

# Continue with the valid entities
valid_entities = df[df['Entity'].apply(lambda x: isinstance(x, str))]

# Extract the "Entity" column into a list
entities = valid_entities['Entity'].tolist()

# Open the text file with UTF-8 encoding (no lowercase normalization)
with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Count occurrences of each entity as-is (case-sensitive)
entity_counts = Counter()
for entity in entities:
    entity_counts[entity] = text.count(entity)  # No .lower() applied here

# Convert the counts to the JSON format expected by the D3.js visualization
entity_data = [{"entity": entity, "count": count} for entity, count in entity_counts.items()]

# Get the directory of the input text file
output_dir = os.path.dirname(text_file_path)

# Define the output JSON file path
output_file_path = os.path.join(output_dir, 'entity_counts.json')

# Save the entity counts as a JSON file in the text file's directory
with open(output_file_path, 'w') as json_file:
    json.dump(entity_data, json_file, indent=4)

print(f"Entity counts saved to {output_file_path}")
