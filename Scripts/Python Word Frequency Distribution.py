import os
import nltk
from collections import Counter
import matplotlib.pyplot as plt

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Add custom stop words if needed
custom_stop_words = {'shall', 'unto', 'verily', 'thou', 'thy', 'therefore','thou art','thou shall','1','chapter','unto','saith','thus','came','let','paragraph','thence',
                     'forth','mine','dwell','saw','ever','like','indeed','along', 'rabbi','another','incident','said','rabbis','yehuda','rabban','kehuna','bar','ben',
                     'yosef','abba','shmuel','zakai','yehoshua','spoke','qed','52','ghayat','making','42','26','sghayat','9','made','18','back','36','51','proofs',
                     'see','v','even','noco','cicale','mada','zodiredo','odo','lape','hoathahe','qaa','od','zodoreje','zodacare','seem','come','thee','set', 'yet',
                     'may','hence', 'also','ye','upon','hath','go','saying','went','things','shalt','hast','till','place','call','would','stated','say','would',
                     'rather','well','etc','satanist', 'satanic','must','wilt','thine'}  # Adjust as necessary
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
# Remove stop words and non-alphabetic tokens
filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]

# Count word frequencies
word_freq = Counter(filtered_tokens)
top_words = word_freq.most_common(20)  # Adjust the number of words displayed

# Plot the word frequency distribution
words, frequencies = zip(*top_words)
plt.figure(figsize=(10, 6))
plt.barh(words, frequencies, color='green')
plt.xlabel("Frequency")
plt.title("Top 20 Word Frequency Distribution in the Tibetan Book of the Dead")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save the plot
output_path = os.path.join(os.path.dirname(file_path), "tibetan_word_frequency_distribution.png")
plt.savefig(output_path)
plt.close()
print(f"Word Frequency Distribution saved at: {output_path}")
