import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
from networkx.algorithms.community import greedy_modularity_communities

# Page Config ###########################################
st.set_page_config(
    page_title="Graph Vizualization",
    page_icon="🟢",
    layout="wide",
)

st.title("Graph Vizualization Example")
st.markdown(
        """
        **This is a Graph Vizualization Example**
        """
        )
st.markdown("---")



# Data ##################################################

data = [
        ('Alice', 'Bob'),
        ('Alice','Charlie'),
        ('Bob','Charlie'),
        ('Charlie','Diana'),
        ('Diana','Eve'),
        ('Bob','Diana'),
        ('Frank','Eve'),
        ('Eve','Ian'),
        ('Diana','Ian'),
        ('Ian','Grace'),
        ('Grace','Hannah'),
        ('Hannah','Jack'),
        ('Grace','Jack'),
        ('Charlie','Frank'),
        ('Alice','Eve'),
        ('Bob','Jack'),
        ]

g = nx.Graph()
g.add_edges_from(data)
pos = nx.spring_layout(g)  # Force-directed layout
nx.draw(g, pos, with_labels=True, node_color='lightgreen', edge_color='gray')

st.pyplot(plt.show())

person = ''
value = 0
# ID who is the most connected ##############################
st.markdown('---')
conn = nx.degree_centrality(g)
for node, score in conn.items():
    st.write(f'Person: {node}: Degree Score: {score}')
st.markdown('The people with the highest degree centrality are:')
st.write('Bob, Charlie, Diana, Eve')

# Betweenness Centrality #####################################
st.markdown('---')
between= nx.betweenness_centrality(g, weight='weight')
for node, score in between.items():
    st.write(f'Person: {node}: Betweenness Score: {score}')
    if score > value:
        value = score
        person = node
st.markdown('The person that is the most connected with others is:')
st.write(person)

# Closeness Centrality ######################################
st.markdown('---')
person = ''
value = 0
close = nx.closeness_centrality(g)
for node, score in close.items():
    st.write(f'Person: {node}: Clooseness to others: {score}')
    if score > value:
        value = score
        person = node
st.markdown('The person that is the most close to others is:')
st.write(person)

# Community Detection ########################################
st.markdown('---')
communites = greedy_modularity_communities(g)
for i, community in enumerate(communites, 1):
    st.write(f'Community {i}: {list(community)}')
st.markdown('These are the communities of this friend gorup graph:')

# Assign a unique color to each community
palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
node_to_comm = {}

for c_index, comm in enumerate(communites):
    for node in comm:
        node_to_comm[node] = c_index

# Build list of colors for drawing
community_colors = [palette[node_to_comm[n]] for n in g.nodes()]

# Draw graph again with community colors
plt.figure(figsize=(8,6))
nx.draw(
    g, pos, with_labels=True, node_size=3000,
    node_color=community_colors, edge_color="gray",
    font_size=10, font_weight="bold", arrows=True
)
weights = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=weights)
plt.title("Phishing Network Colored by Community")
st.pyplot(plt.show())

colors = ['red' if 'malicious' in node else 'green' for node in g.nodes()]
nx.draw(
    g, pos, with_labels=True, node_size=3000, node_color=colors,
    edge_color='gray', font_size=10, font_weight='bold'
)
plt.title("Phishing Network with Malicious Node Highlighting")
st.pyplot(plt.show())
