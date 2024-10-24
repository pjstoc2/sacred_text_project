
import nltk
from nltk import word_tokenize, pos_tag
import os
import csv

# Function to clean the file path input by removing quotes and doubling backslashes
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')
    return cleaned_path.replace("\\", "\\\\")

# Load the text file path and clean it
file_input = input("Enter the full path to your entity CSV file: ")
file_path = clean_file_path(file_input)

entities = []

# Read entities from the CSV file
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        entities.append(row[0])

# Filter out non-proper nouns using POS tagging
filtered_entities = []
for entity in entities:
    words = word_tokenize(entity)
    pos_tags = pos_tag(words)
    
    # Check if the word is tagged as a proper noun (NNP or NNPS)
    if all(tag in ['NNP', 'NNPS'] for _, tag in pos_tags):
        filtered_entities.append(entity)

# Save the filtered entities back to CSV in the same directory as the input file
output_file_path = os.path.join(os.path.dirname(file_path), "filtered_entities.csv")
with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Entity"])  # Write header
    for entity in sorted(filtered_entities):
        writer.writerow([entity])

print(f"Filtered entities have been saved to: {output_file_path}")
