import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# Function to clean file paths
def clean_file_path(file_path):
    cleaned_path = file_path.strip('"')
    return file_path.replace("\\", "/")

# Prompt for the CSV file path and clean it
csv_path = clean_file_path(input('Enter the full path to your CSV file: ').strip('"'))

# Read the CSV
df = pd.read_csv(csv_path)

# Ensure columns are named 'Text' and 'Entity'
df.columns = ['Text', 'Entity']

# Filter entities that appear frequently across texts
entity_counts = Counter(df['Entity'])
filtered_entities = [entity for entity, count in entity_counts.items() if count >= 3]  # Adjust this threshold as needed
df_filtered = df[df['Entity'].isin(filtered_entities)]

# Create a bipartite graph
G = nx.Graph()

# Add nodes with the bipartite attribute
G.add_nodes_from(df_filtered['Text'], bipartite=0)  # Texts on one side
G.add_nodes_from(df_filtered['Entity'], bipartite=1)  # Entities on the other side

# Add edges between Texts and Entities
for _, row in df_filtered.iterrows():
    G.add_edge(row['Text'], row['Entity'])

# Calculate the number of connections (edges) each text has
text_entity_counts = df_filtered.groupby('Text')['Entity'].nunique().to_dict()

# Sort texts by their connection counts (descending order)
sorted_texts = sorted(text_entity_counts, key=text_entity_counts.get, reverse=True)

# Generate the layout for bipartite graph (use sorted_texts instead of the original order)
pos = nx.bipartite_layout(G, sorted_texts)

# Reverse the vertical positions (flip the Y-values)
for node, (x, y) in pos.items():
    pos[node] = (x, -y * 8)  # Flipping the y-values and increasing spacing

# Adjust specific labels (Morals and Dogma and Tibetan Book of the Dead) to move them to the right
for node in pos:
    if node == 'Morals and Dogma':
        pos[node] = (pos[node][0] + 0.02, pos[node][1])  # Move to the right by adjusting the x-value
    elif node == 'Tibetan Book of the Dead':
        pos[node] = (pos[node][0] + 0.03, pos[node][1])  # Move further to the right

# Set the figure size to a taller format
plt.figure(figsize=(15, 60))  # Increased height for more vertical space

# Create custom labels with connection counts for texts
labels_with_counts = {text: f"{text} ({text_entity_counts.get(text, 0)} connections)" for text in sorted_texts}

# Add entity labels
entity_labels = {entity: entity for entity in df_filtered['Entity'].unique()}
labels_with_counts.update(entity_labels)  # Merge text labels with entity labels

# Plot the bipartite graph with labels for both texts and entities
nx.draw(G, pos, labels=labels_with_counts, 
        node_color=['lightblue' if node in df_filtered['Text'].unique() else 'lightgreen' for node in G.nodes()],
        font_size=10, font_weight='bold', edge_color='grey', alpha=0.6, node_size=500)

# Title and layout
plt.title("Filtered Bipartite Graph of Texts and Entities (Sorted by Connection Counts, with Adjusted Labels)", pad=5)
plt.tight_layout()
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)  # Adjust margins after tight_layout()

# Save the graph
output_path = f"{clean_file_path(csv_path.rsplit('/', 1)[0])}/bipartite_graph_mnd_sorted_flipped_adjusted_labels.png"
plt.savefig(output_path, dpi=175, bbox_inches="tight")
plt.close()
print(f"Filtered Bipartite Graph saved at: {output_path}")
