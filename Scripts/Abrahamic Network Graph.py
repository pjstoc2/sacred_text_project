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
filtered_entities = [entity for entity, count in entity_counts.items() if count >= 3]  # Adjust threshold as needed
df_filtered = df[df['Entity'].isin(filtered_entities)]

# Create a network graph
G = nx.Graph()

# Add edges between Entities that co-occur in the same Text
for text in df_filtered['Text'].unique():
    entities_in_text = df_filtered[df_filtered['Text'] == text]['Entity'].tolist()
    for i, entity1 in enumerate(entities_in_text):
        for entity2 in entities_in_text[i+1:]:
            if G.has_edge(entity1, entity2):
                G[entity1][entity2]['weight'] += 1
            else:
                G.add_edge(entity1, entity2, weight=1)

# Filter edges with a minimum weight threshold to reduce clutter
G_filtered = nx.Graph(((u, v, e) for u, v, e in G.edges(data=True) if e['weight'] >= 2))  # Adjust threshold as needed

# Generate positions for network graph
pos = nx.spring_layout(G_filtered, k=0.5)

# Plot the network graph
plt.figure(figsize=(15, 10))
nx.draw(G_filtered, pos, with_labels=True, node_color='lightcoral', font_size=8, edge_color='gray', alpha=0.7, node_size=500, width=[e['weight'] * 0.3 for (u, v, e) in G_filtered.edges(data=True)])
plt.title("Filtered Network Graph of Entities")
plt.tight_layout()

# Save the graph
output_path = f"{clean_file_path(csv_path.rsplit('/', 1)[0])}/filtered_network_graph_mnd_sat.png"
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Filtered Network Graph saved at: {output_path}")
