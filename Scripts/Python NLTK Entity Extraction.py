import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import os
import csv

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Load the text file
file_path = input("Enter the full path to your text file: ").strip('"')
with open(file_path, 'r', encoding='utf-8') as file:
    text_data = file.read()

# Tokenize the text and extract named entities
words = word_tokenize(text_data)
pos_tags = pos_tag(words)
entities = ne_chunk(pos_tags)

# Collect named entities into a set
entity_list = set()
for subtree in entities:
    if isinstance(subtree, nltk.Tree):
        entity_name = " ".join(word for word, tag in subtree.leaves())
        entity_list.add(entity_name)

# Define the output file path
output_file_path = os.path.join(os.path.dirname(file_path), "tibetan_extracted_entities.csv")

# Write the extracted entities to the CSV file
with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Entity"])  # Write header
    for entity in sorted(entity_list):
        writer.writerow([entity])

print(f"Extracted entities have been saved to: {output_file_path}")

