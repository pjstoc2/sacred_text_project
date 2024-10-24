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

# Generate the layout for bipartite graph
pos = nx.bipartite_layout(G, df_filtered['Text'].unique())

# Plot the bipartite graph
plt.figure(figsize=(15, 10))
nx.draw(G, pos, with_labels=True, node_color=['lightblue' if node in df_filtered['Text'].unique() else 'lightgreen' for node in G.nodes()], font_size=8, edge_color='grey', alpha=0.6, node_size=500)
plt.title("Filtered Bipartite Graph of Texts and Entities")
plt.tight_layout()

# Save the graph
output_path = f"{clean_file_path(csv_path.rsplit('/', 1)[0])}/bipartite_graph_mnd_all.png"
plt.savefig(output_path, dpi=300)
plt.close()
print(f"Filtered Bipartite Graph saved at: {output_path}")
