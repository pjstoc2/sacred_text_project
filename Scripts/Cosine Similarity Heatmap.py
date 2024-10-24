import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to clean file paths
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')
    return cleaned_path.replace("\\", "/")  # Convert all backslashes to forward slashes


# List of all text file paths (clean them automatically)
file_paths = [
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\BG Srimad.txt"),  # Replace with actual paths
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Bible KJV.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Book of Enoch.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Dhammapada.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Kybalion.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Midrash_Collection.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Morals and Dogma.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Picatrix.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Quran Hilali.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Satanic Bible.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\Tao Te Ching.txt"),
    clean_file_path(r"C:\Users\paulo\OneDrive\Desktop\Data\Projects\Sacred Text Analysis\Text Files\The-Tibetan-Book-of-the-Dead.txt")
    # Add all 12 paths here, and they'll be cleaned
]

# Read all texts
texts = []
for path in file_paths:
    with open(path, 'r', encoding='utf-8') as file:
        texts.append(file.read())

# Calculate the TF-IDF matrix for all texts
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(texts)

# Calculate cosine similarity matrix
similarity_matrix = cosine_similarity(tfidf_matrix)

# Convert the similarity matrix to a DataFrame for visualization
similarity_df = pd.DataFrame(similarity_matrix, index=[os.path.basename(fp) for fp in file_paths], columns=[os.path.basename(fp) for fp in file_paths])

# Plot the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(similarity_df, annot=True, cmap='Reds', xticklabels=True, yticklabels=True)
plt.title("Cosine Similarity Heatmap Between Texts", pad=20, weight='bold', fontsize=20)

# Save the heatmap in the input directory
output_dir = os.path.dirname(file_paths[0])  # Assuming all files are in the same directory
output_path = os.path.join(output_dir, "cosine_similarity_heatmap.png")
plt.tight_layout()
plt.savefig(output_path)
plt.close()

print(f"Heatmap saved at: {output_path}")
