import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

# Page Config ###########################################
st.set_page_config(
    page_title="Graph Vizualization",
    page_icon="🟢",
    layout="wide",
)

st.title("Graph Vizualization Example")


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
plt.show()
