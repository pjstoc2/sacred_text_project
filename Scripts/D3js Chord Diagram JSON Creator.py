import pandas as pd
import json
import itertools
from collections import Counter
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

# Load the CSV file containing the list of entities
df = pd.read_csv(entity_file_path, encoding='utf-8')

# Extract the "Entity" column into a list
entities = df['Entity'].tolist()

# Open the text file and read the content
with open(text_file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Normalize the text for easier matching (lowercase and remove punctuation if necessary)
normalized_text = text.lower()

# Count the frequency of each entity in the text
entity_counts = Counter()

for entity in entities:
    count = normalized_text.count(entity.lower())  # Count entity occurrences in the text
    if count > 0:
        entity_counts[entity] = count

# Limit the number of entities to the top N most frequent ones (e.g., top 50)
N = 20
top_entities = [entity for entity, _ in entity_counts.most_common(N)]

# Split the text into sentences (you can modify this for proximity-based co-occurrence)
sentences = text.split('.')

# Function to find co-occurrences of entities within each sentence
def find_cooccurrences(entities, sentences):
    cooccurrences = Counter()
    
    for sentence in sentences:
        words = sentence.split()  # Tokenize the sentence into words
        present_entities = [entity for entity in entities if entity.lower() in [word.lower() for word in words]]
        
        # Find all pairs of co-occurring entities in the sentence
        for pair in itertools.combinations(present_entities, 2):
            cooccurrences[pair] += 1

    return cooccurrences

# Find co-occurrences in the text
cooccurrences = find_cooccurrences(top_entities, sentences)

# Apply a co-occurrence strength threshold (e.g., minimum 3 co-occurrences)
min_threshold = 3
filtered_cooccurrences = {
    pair: count for pair, count in cooccurrences.items()
    if count >= min_threshold  # Only include pairs with 3 or more co-occurrences
}

# Prepare the matrix for the chord diagram
names = top_entities
matrix = [[0 for _ in top_entities] for _ in top_entities]

# Populate the matrix with filtered co-occurrence counts
entity_index = {entity: i for i, entity in enumerate(top_entities)}
for (entity1, entity2), count in filtered_cooccurrences.items():
    i = entity_index[entity1]
    j = entity_index[entity2]
    matrix[i][j] = count
    matrix[j][i] = count  # Symmetric relationship

# Prepare the Chord Diagram data
chord_data = {
    "names": names,
    "matrix": matrix
}

# Get the directory of the input text file
output_dir = os.path.dirname(text_file_path)

# Save the Chord Diagram JSON
chord_output_path = os.path.join(output_dir, 'chord_data_filtered.json')
with open(chord_output_path, 'w') as json_file:
    json.dump(chord_data, json_file, indent=4)

print(f"Filtered Chord Diagram data saved to {chord_output_path}")
