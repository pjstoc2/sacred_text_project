import os
import nltk
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
import matplotlib.pyplot as plt

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Add your own stop words
custom_stop_words = {'shall', 'unto', 'verily', 'thou', 'thy', 'therefore','thou art','thou shall','1','chapter','unto','saith','thus','came','let','paragraph','thence',
                     'forth','mine','dwell','saw','ever','like','indeed','along', 'rabbi','another','incident','said','rabbis','yehuda','rabban','kehuna','bar','ben',
                     'yosef','abba','shmuel','zakai','yehoshua','spoke','qed','52','ghayat','making','42','26','sghayat','9','made','18','back','36','51','proofs',
                     'see','v','even','noco','cicale','mada','zodiredo','odo','lape','hoathahe','qaa','od','zodoreje','zodacare','seem','come','thee','set'}  # Add more as needed

# Combine default stop words with your custom ones
stop_words = set(stopwords.words('english')).union(custom_stop_words)

# Function to clean file paths
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')
    return cleaned_path.replace("\\", "/")

# Prompt for the text file path and clean it
file_path = clean_file_path(input("Enter the full path to your text file: "))

# Read and tokenize the text
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read().lower()

tokens = nltk.word_tokenize(text)
# Remove stop words
filtered_tokens = [token for token in tokens if token not in stop_words]

# Find phrase collocations
finder = BigramCollocationFinder.from_words(filtered_tokens)
finder.apply_freq_filter(3)  # Only include phrases occurring at least 3 times

bigram_measures = BigramAssocMeasures()
top_phrases = finder.nbest(bigram_measures.likelihood_ratio, 20)

# Visualize the top phrases
phrases, frequencies = zip(*[(f"{phrase[0]} {phrase[1]}", finder.ngram_fd[phrase]) for phrase in top_phrases])

plt.figure(figsize=(10, 6))
plt.barh(phrases, frequencies, color='skyblue')
plt.xlabel("Frequency")
plt.title("Top 20 Phrase Collocations in the Tao Te Ching")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save the plot
output_path = os.path.join(os.path.dirname(file_path), "tao_phrase_collocations.png")
plt.savefig(output_path)
plt.close()
print(f"Filtered Phrase Collocations saved at: {output_path}")
