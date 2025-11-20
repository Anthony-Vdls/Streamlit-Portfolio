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
    st.write(f'Person: {node}: Degree Score: {score}')
    if score > value:
        value = score
        person = node
st.markdown('The person that is the most connected with others is:')
st.write(person)
