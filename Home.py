import streamlit as st

st.set_page_config(
    page_title="Anthony Vidales",
    page_icon="🪪",
    layout="wide"
)

st.title(" Welcome to My Streamlit Site🕺")

st.markdown(
        """

This site is a small portfolio of the things I learned in Data Visualization class.
In the sidebar to the left of this text:

- 🪪 **Who I Am** – Background and skills, and a quote I made up.
- 🚗 **Used Car Market Explorer** – Sweet interactive visualizations about used car sales.
- 📈 **Car Market Dashboard** – A highly interactive dashboard with KPIs and takeaways for buyers and sellers.
- ⌛ **Upcoming Works** – Notes on ideas and projects I’m planning next.
        """
    )

st.markdown("---")

st.markdown(
    """
### How to get around

- Use the **left sidebar** to switch between pages.  
- If you’re just checking out my work:
  1. Start with **Who I Am** for a quick intro.
  2. Jump to **Car Market Dashboard** to see a polished analysis.
  3. Visit **Used Car Market Explorer** if you want to explore some of the data yourself.

Thanks for taking a look 👋
    """
)
