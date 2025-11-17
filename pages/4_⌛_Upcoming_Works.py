import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Future Work", page_icon="⌛", layout="centered")
st.title('Under Construction🚧')
st.markdown(
        """
        ## Next Steps
        Thank you for visiting this web page, but this just the beginning. Id like to continue working on this and other data and showing casing other things I can do with the things I learned.  
        For starters:  
        * Expand this set to include more technical information about the vehicles in it, like horse power and torque.  
        * Add these features in the plots.
        * Train k-means model to cluster them by likeness and average the price of the cluster.  
        * Add a functionality to the page to that the user can input there car and it will return a realisic selling price via the k-means clusters.  
        """
        )
st.markdown('---')
st.markdown(
        """
        ## Reflection 🪞  
        * What changed from the prototype of this project is that I was not allowed to use the sane dataset. And with that the questions that I tried answering changed as well, as did the KPIs.
        * I also learned a lot more about how to format things in stream lit and I think its prettier and more accessible now.  
        """)
