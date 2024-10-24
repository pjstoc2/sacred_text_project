import os
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Function to clean file paths
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')
    return cleaned_path.replace("\\", "/")

# Prompt for the text file path and clean it
file_path = clean_file_path(input("Enter the full path to your text file: "))

# Read the text file
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read().lower()

# Remove punctuation
text = re.sub(r'[^\w\s]', '', text)

# Tokenize the text
tokens = nltk.word_tokenize(text)

# Remove stop words
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word not in stop_words]

# Save the cleaned text
output_path = os.path.join(os.path.dirname(file_path), "morals cleaned.txt")
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(" ".join(filtered_tokens))

print(f"Cleaned text saved at: {output_path}")
