
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

##################################################################### 
# Page config
##################################################################### 
st.set_page_config(
    page_title="Used Car EDA Gallery",
    page_icon="🚗",
    layout="wide",
)

pio.templates.default = "plotly_white"

st.title("Used Car EDA Gallery")

st.markdown(
    """
This page showcases four exploratory data visualizations built from a used car
sales dataset. Each chart answers a question and includes a short
guide on how to read it. Below them are observations from the plots.
"""
)

##################################################################### 
# Data Cleaning
##################################################################### 
@st.cache_data
def load_clean_data(path: str = "./data/car_prices.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    # need UTC so that pandas datetime funcs work
    df["saledate"] = pd.to_datetime(df["saledate"], errors="coerce", utc=True)

    # engineered features
    df["sale_year"] = df["saledate"].dt.year
    df["car_age"] = df["sale_year"] - df["year"]

    # get rid of ages that don't make sense
    df = df[(df["car_age"] >= 0) & (df["car_age"] <= 60)]

    # take out outliers using 5th–95th percentiles
    outliers = ["odometer", "mmr", "sellingprice", "car_age"]
    for col in outliers:
        low, high = df[col].quantile([0.05, 0.95])
        df = df[(df[col] >= low) & (df[col] <= high)]

    df_clean = df.copy()
    return df_clean


df_clean = load_clean_data()
st.markdown(f"**Rows after cleaning & outlier removal:** {len(df_clean):,}")
st.markdown('---')
##################################################################### 
# 1) Bar chart – Avg selling price vs MMR by make
##################################################################### 
st.header("1. Are some makes consistently sold above or below MMR?")

st.markdown("**Chart type:** Horizontal bar chart")

st.markdown("**Question:**")
st.markdown(
    "Do certain vehicle makes tend to sell for more or less than the Manheim "
    "Market Report (MMR) benchmark retail price?"
)

st.markdown("**How to read this chart:**")
st.markdown(
    """
- Each bar represents a **vehicle make/brand** with at least 300 sales in the dataset.
- The x-axis shows the **average difference** between selling price and MMR within a make. 
- Bars to the **right of zero** indicate makes that tend to sell **above** their MMR price while bars to the left sell **below** it.
- Hover over a bar with the mouse for more detials.   
"""
)

# keep rows with valid MMR
df_m = df_clean[df_clean["mmr"] > 0].copy()

# price difference vs MMR
df_m["price_diff"] = df_m["sellingprice"] - df_m["mmr"]

# aggregate by make
make_stats = (
    df_m.groupby("make")
    .agg(
        avg_diff=("price_diff", "mean"),
        med_diff=("price_diff", "median"),
        n=("price_diff", "size"),
    )
    .reset_index()
)

# leave out the super unpopular ones
make_stats = make_stats[make_stats["n"] >= 300]

# sort from most underpriced to most overpriced
make_stats = make_stats.sort_values("avg_diff")

# size the gaps of the bars better (like notebook)
n_makes_bar = len(make_stats)
height_bar = min(900, 30 * n_makes_bar)  # ~30px per bar, cap at 900

bar_fig = px.bar(
    make_stats,
    x="avg_diff",
    y="make",
    orientation="h",
    height=height_bar,
    title="Average Selling Price vs MMR by Make",
    labels={
        "make": "Make",
        "avg_diff": "Average Sell Price (Above or Below MMR) $",
    }
)

bar_fig.update_traces(
    customdata=make_stats[["med_diff", "n"]].to_numpy(),
    hovertemplate=(
        "Make: %{y}<br>"
        "Avg diff: $%{x:.0f}<br>"
        "Median diff: $%{customdata[0]:.0f}<br>"
        "Sales: %{customdata[1]:,}<extra></extra>"
    ),
    marker_line_color="black",
    marker_line_width=1,
)

bar_fig.add_vline(x=0, line_dash="solid", line_color="black")
bar_fig.update_layout(
    yaxis_title="Make",
    xaxis_title="Average Sell Price (Above or Below MMR) $USD",
    yaxis=dict(autorange="reversed"),
)

st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("**Observations & insights:**")
st.markdown(
    """
- Concitering these are **used car sales**, its not suprizing that most of the makes are being sold bellow MMR.
- Suzuki sells the highest alove MMR while the it tapers off fast showing that used vehicle sales do not maintain MMR value for long.  
- **Luxury brands**, like Jaguar, Mercedes and Lexus populate the higher portion of the plot.  
"""
)

st.markdown("---")


##################################################################### 
# 2) Choropleth – Average selling price by state
##################################################################### 
st.header("2. How do average selling prices vary across U.S. states?")

st.markdown("**Chart type:** Choropleth map")

st.markdown("**Question:**")
st.markdown(
    "Which states have higher or lower average selling prices for used vehicles?"
)

st.markdown("**How to read this chart:**")
st.markdown(
    """
- Each state is colored by its **average selling price** in the dataset.
- Brighter colors represent **higher average prices** while darker blues represent lower prices.
- Hover over a state to see more stats on eatch state.   
- Grey/white states have **no sales** in the data used to make this map.
"""
)

state_data = df_clean.copy()
state_data["state_upper"] = state_data["state"].astype(str).str.upper().str.strip()

state_summary = (
    state_data.groupby("state_upper")
    .agg(
        avg_price=("sellingprice", "mean"),
        n_sales=("sellingprice", "size"),
        avg_age=("car_age", "mean"),
    )
    .reset_index()
)

map_fig = px.choropleth(
    state_summary,
    locations="state_upper",
    locationmode="USA-states",
    color="avg_price",
    scope="usa",
    title="Average Selling Price by State",
    labels={"avg_price": "Avg price ($)"},
    # color blind friendly scale
    color_continuous_scale="Viridis",
)

map_fig.update_traces(
    customdata=np.stack(
        [state_summary["avg_age"], state_summary["n_sales"]], axis=-1
    ),
    hovertemplate=(
        "State: %{location}<br>"
        "Avg price: $%{z:,.0f}<br>"
        "Avg car age: %{customdata[0]:.1f} yrs<br>"
        "Sales: %{customdata[1]:,}<extra></extra>"
    ),
)

map_fig.update_layout(coloraxis_colorbar_title="Avg price")

st.plotly_chart(map_fig, use_container_width=True)

st.markdown("**Observations & insights:**")
st.markdown(
    """
- *Massachusetts has the **lowest** average selling price for all used vehicles.*
- *If you're willing to go the next state over when buying a used car you can save a couple thousand dollars*
"""
)

st.markdown("---")

##################################################################### 
# 3) Line chart – Median price vs odometer by make (with dropdown)
##################################################################### 
st.header("3. How does median selling price change with mileage for different makes?")

st.markdown("**Chart type:** Line chart with dropdown")

st.markdown("**Question:**")
st.markdown(
    "How does the typical selling price vary across mileage bands, and "
    "do some makes hold their value better at higher mileage?"
)

st.markdown("**How to read this chart:**")
st.markdown(
    """
- The x-axis shows **odometer (mileage)**, medians when sold at the y-axis price.
- The y-axis shows the **median selling price** within each mileage group.
- Each line represents a **vehicle make**. Use the dropdown menu to focus on a single make or show all of them.
- A steeper drop means that brand loses value faster.  
- Find your favorite car make! 
"""
)

pio.templates.default = "plotly_white"

top_makes_for_lines = (
    df_clean["make"]
    .value_counts()
    .head(20)
    .index
)

# define odometer bins
min_odo = df_clean["odometer"].min()
max_odo = df_clean["odometer"].max()
odo_bins = np.linspace(min_odo, max_odo, 11)
odo_midpoints = (odo_bins[:-1] + odo_bins[1:]) / 2

line_fig = go.Figure()
trace_names = []

for make in top_makes_for_lines:
    tmp = df_clean[df_clean["make"] == make].copy()

    tmp["odo_bin"] = pd.cut(
        tmp["odometer"],
        bins=odo_bins,
        labels=odo_midpoints,
        include_lowest=True,
    )

    grouped = (
        tmp.groupby("odo_bin")["sellingprice"]
        .median()
        .reset_index()
        .dropna()
    )

    grouped["odo_bin"] = grouped["odo_bin"].astype(float)

    line_fig.add_trace(
        go.Scatter(
            x=grouped["odo_bin"],
            y=grouped["sellingprice"],
            mode="lines+markers",
            name=make,
            hovertemplate=(
                "Make: " + make +
                "<br>Odometer ~ %{x:,.0f} mi"
                "<br>Median price: $%{y:,.0f}<extra></extra>"
            ),
        )
    )
    trace_names.append(make)

# dropdown for makes
buttons = []
for i, make in enumerate(trace_names):
    visible = [False] * len(trace_names)
    visible[i] = True
    buttons.append(
        dict(
            label=make,
            method="update",
            args=[
                {"visible": visible},
                {"title": f"Median Selling Price vs Odometer – {make}"},
            ],
        )
    )

# "All" button
buttons.insert(
    0,
    dict(
        label="All",
        method="update",
        args=[
            {"visible": [True] * len(trace_names)},
            {"title": "Median Selling Price vs Odometer by Make"},
        ],
    )
)

line_fig.update_layout(
    title="Median Selling Price vs Odometer by Make",
    xaxis_title="Odometer Medians Durring Sale (Miles)",
    yaxis_title="Median Selling Price ($USD)",
    legend_title_text="Make",
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=1.02,
            xanchor="left",
            y=1.15,
            yanchor="top",
        )
    ],
    # colorblind friendly 
    colorway=px.colors.qualitative.Safe,
)

st.plotly_chart(line_fig, use_container_width=True)

st.markdown("**Observations & insights:**")
st.markdown(
    """
- *Looks like **Ford** losses value the fastest*
- *There is a spike in **Jeep**.*
- *A lot of the makes experance a slight increase in selling price at the milage reaches 150k Miles *
"""
)

st.markdown("---")

# ===================================================================
# 4) Heatmap – Age distribution of vehicle sales by make
# ===================================================================
st.header("4. Which makes show up more often as older vehicles in the resale market?")

st.markdown("**Chart type:** Heatmap")

st.markdown("**Question:**")
st.markdown(
    "For the **most common** makes, how is the age of vehicles at sale distributed? "
    "Do some brands appear more often as older cars in this dataset?"
)

st.markdown("**How to read this chart:**")
st.markdown(
    """
- Each **row** is a vehicle make (top makes by sales volume).
- Each **column** is a **range of years** at the time of sale:  
`<3`, `3–5`, `5–7`, `7+` years.
- Color shows the **proportion of that make's sales** falling into each age band (lighter/brighter = higher share).
- Makes with brighter colors in the older age bands (`5–7`, `7+`) show up more often as older cars.
"""
)

df_hm = df_clean.copy()

# Define age bands
age_bins = [0, 3, 5, 7, 100]
age_labels = ["<3 yrs", "3–5 yrs", "5–7 yrs", "7+ yrs"]

df_hm["age_band"] = pd.cut(
    df_hm["car_age"],
    bins=age_bins,
    labels=age_labels,
    right=False,
    include_lowest=True,
)

# Focus on top N makes by volume
TOP_MAKES = 15
top_makes_for_heat = (
    df_hm["make"]
    .value_counts()
    .head(TOP_MAKES)
    .index
)

df_hm = df_hm[df_hm["make"].isin(top_makes_for_heat)]

# Count cars by (make, age_band)
agg = (
    df_hm.groupby(["make", "age_band"])
    .size()
    .reset_index(name="count")
)

# Compute within-make share
totals = agg.groupby("make")["count"].sum().reset_index(name="total")
agg = agg.merge(totals, on="make")
agg["share"] = agg["count"] / agg["total"]

# Pivot to matrix form: rows = makes, cols = age bands, values = share
heat_data = agg.pivot(index="make", columns="age_band", values="share")

heatmap_fig = px.imshow(
    heat_data,
    labels=dict(
        x="Vehicle Ages",
        y="Make",
        color="Proportion of sales",
    ),
    title="Heatmap of Vehicle's Ages when Sold by Make\n",
    aspect="auto",
    # colorblind friendly
    color_continuous_scale="Viridis",
)

n_makes_heat = len(heat_data.index)
heatmap_fig.update_layout(
    height=min(50 * n_makes_heat, 900),
)

heatmap_fig.update_yaxes(
    tickmode="array",
    tickvals=list(range(n_makes_heat)),
    ticktext=list(heat_data.index),
)

# Human-readable hover
hover_text = []
for make in heat_data.index:
    row = []
    for band in heat_data.columns:
        share = heat_data.loc[make, band]
        if pd.isna(share):
            row.append("")
        else:
            count = int(
                agg[(agg["make"] == make) & (agg["age_band"] == band)]["count"].iloc[0]
            )
            row.append(
                f"Make: {make}<br>"
                f"Age: {band}<br>"
                f"Proportion of sales: {share:.0%}<br>"
                f"Cars: {count:,}"
            )
    hover_text.append(row)

heatmap_fig.update_traces(
    customdata=np.array(hover_text),
    hovertemplate="%{customdata}",
)

heatmap_fig.update_xaxes(side="top")

st.plotly_chart(heatmap_fig, use_container_width=True)

st.markdown("**Observations & insights:**")
st.markdown(
    """
- **BMW** has the some of the oldest vehicles on the market.*
- *Other then that, the general trend is that most cars bening sold are mostly within the **1-3 year** range.* 
- **Infiniti, Nissan and Honda** have most of there inventory sold around the middle of the range, that is around *3-5 years*
"""
)

