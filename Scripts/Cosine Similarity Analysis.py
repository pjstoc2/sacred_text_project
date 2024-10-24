import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the two text files
file1_path = input("Enter the full path to your first text file: ").strip('"')
file2_path = input("Enter the full path to your second text file: ").strip('"')

with open(file1_path, 'r', encoding='utf-8') as file1:
    text1 = file1.read()

with open(file2_path, 'r', encoding='utf-8') as file2:
    text2 = file2.read()

# Create a DataFrame with the two texts
texts = [text1, text2]
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(texts)

# Calculate cosine similarity
similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
similarity_score = similarity_matrix[0][0]  # Extract the similarity score

print(f"The cosine similarity between the two texts is: {similarity_score:.4f}")
