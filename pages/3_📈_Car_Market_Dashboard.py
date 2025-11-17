
import datetime as dt

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Car Price Dashboard", layout="wide")


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

# extra engineered columns for the dashboard
df_clean = df_clean.copy()
df_clean["price_diff"] = df_clean["sellingprice"] - df_clean["mmr"]
df_clean["body_clean"] = df_clean["body"].astype(str).str.strip().str.title()
df_clean["sale_year"] = df_clean["sale_year"].astype("Int64")


#####################################################################
# Header + data source / refresh info
#####################################################################
st.title("Used Car Sales Dashboard 🚗")

header_left,  header_right = st.columns([2, 2])

with header_left:
    st.markdown("📦Data source: [Kaggle](www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data)")

with st.expander("How to use this page 🧭", expanded=False):
    st.markdown(
        """
* Set vehicle filters on the left. This changes:  
    * KPIs  
    * The text at the bottom  
    * What you can select from in the dropdown in the middle of the page  
* Use the dropdown above the first plot to choose vehicle brands.  
  Only brands included in the left filter panel will appear here.  
* To read the charts:  
    * **Left chart** shows average selling prices by make/model.  
    * **Right chart** shows how much body styles sell on average above or below the Manheim Market Report (MMR) value of the vehicle.  

**NOTE:** Refresh the page to reset filters.
        """
    )

with header_right:
    st.markdown(
        f"⏱️ **Last refreshed:** {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
    )


#####################################################################
# Sidebar
#####################################################################
st.sidebar.header("Filters")

# make filter (top 15 by count to keep it reasonable)
top_makes = (
    df_clean["make"]
    .value_counts()
    .head(25)
    .index.tolist()
)
selected_makes = st.sidebar.multiselect(
    "Select Make(s)",
    options=top_makes,
    default=top_makes,
)

# body filter
body_options = sorted(df_clean["body_clean"].dropna().unique().tolist())
selected_bodies = st.sidebar.multiselect(
    "Select Body style",
    options=body_options,
    default=body_options,
)

# selling price range slider
price_min = int(df_clean["sellingprice"].min())
price_max = int(df_clean["sellingprice"].max())
price_range = st.sidebar.slider(
    "Selling price range ($)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    step=500,
)


#####################################################################
# Apply filters
#####################################################################
df_filtered = df_clean.copy()

if selected_makes:
    df_filtered = df_filtered[df_filtered["make"].isin(selected_makes)]

if selected_bodies:
    df_filtered = df_filtered[df_filtered["body_clean"].isin(selected_bodies)]

df_filtered = df_filtered[
    df_filtered["sellingprice"].between(price_range[0], price_range[1])
]


#####################################################################
# KPIs
#####################################################################
st.subheader("Key Metrics")

# if filter is to scrict
if df_filtered.empty:
    st.warning("No data matches the current filters.")
else:
    total_sales = int(df_filtered.shape[0])
    avg_diff = df_filtered["price_diff"].mean()
    median_diff = df_filtered["price_diff"].median()
    median_odometer = df_filtered["odometer"].median()
    median_age = df_filtered["car_age"].median()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # formats are hard
    kpi1.metric("Total sales", f"{total_sales:,}")
    kpi2.metric("Avg vs MMR", f"{avg_diff:+,.0f} $")
    kpi3.metric("Median vs MMR", f"{median_diff:+,.0f} $")
    kpi4.metric("Typical car", f"{median_age:.1f} yrs / {median_odometer:,.0f} mi")


#####################################################################
# Visuals in two columns
#####################################################################
if not df_filtered.empty:

    left_col, right_col = st.columns((2, 1), gap="medium")

    #################################################################
    # LEFT
    #################################################################
    with left_col:
        st.subheader("Price Levels by Make & Model")

        available_makes = sorted(df_filtered["make"].unique())
        drill_options = ["All makes"] + available_makes

        # removed help=... so no '?' tooltip
        selected_make_view = st.selectbox(
            "Choose a brand to explore",
            options=drill_options,
            index=0,
        )

        if selected_make_view == "All makes":
            make_stats = (
                df_filtered.groupby("make", as_index=False)
                .agg(
                    avg_price=("sellingprice", "mean"),
                    avg_diff=("price_diff", "mean"),
                    n=("sellingprice", "size"),
                )
                .sort_values("avg_price", ascending=False)
            )

            # keep reasonably common makes
            make_stats = make_stats[make_stats["n"] >= 100].head(15)

            fig_left = px.bar(
                make_stats,
                x="avg_price",
                y="make",
                orientation="h",
                hover_data={
                    "n": True,
                    "avg_diff": ":+.0f",
                    "avg_price": ":.0f",
                },
                labels={
                    "make": "Make",
                    "avg_price": "Average selling price ($)",
                    "n": "Sales",
                    "avg_diff": "Avg vs MMR ($)",
                },
                title="Average Selling Price by Make",
                height=500,
            )
            fig_left.update_layout(yaxis=dict(autorange="reversed"))

        else:
            df_make = df_filtered[df_filtered["make"] == selected_make_view]

            model_stats = (
                df_make.groupby("model", as_index=False)
                .agg(
                    avg_price=("sellingprice", "mean"),
                    avg_diff=("price_diff", "mean"),
                    n=("sellingprice", "size"),
                )
            )

            # keep reasonably common models
            model_stats = (
                model_stats[model_stats["n"] >= 30]
                .sort_values("avg_price", ascending=False)
            )

            fig_left = px.bar(
                model_stats,
                x="avg_price",
                y="model",
                orientation="h",
                hover_data={
                    "n": True,
                    "avg_diff": ":+.0f",
                    "avg_price": ":.0f",
                },
                labels={
                    "model": "Model",
                    "avg_price": "Average selling price ($)",
                    "n": "Sales",
                    "avg_diff": "Avg vs MMR ($)",
                },
                title=f"Average Selling Price by Model – {selected_make_view}",
                height=500,
            )
            fig_left.update_layout(yaxis=dict(autorange="reversed"))

        st.plotly_chart(fig_left, use_container_width=True)

    #################################################################
    # RIGHT
    #################################################################
    with right_col:
        st.subheader("Price Compared to MMR by Body Style")

        body_stats = (
            df_filtered.groupby("body_clean", as_index=False)
            .agg(
                avg_diff=("price_diff", "mean"),
                median_diff=("price_diff", "median"),
                n=("price_diff", "size"),
            )
        )

        # keep common body styles
        body_stats = body_stats[body_stats["n"] >= 500].sort_values("avg_diff")

        if not body_stats.empty:
            fig_right = px.bar(
                body_stats,
                x="avg_diff",
                y="body_clean",
                orientation="h",
                hover_data={
                    "n": True,
                    "median_diff": ":+.0f",
                },
                labels={
                    "body_clean": "Body style",
                    "avg_diff": "Average selling price minus MMR ($)",
                    "n": "Sales",
                },
                title="Average Price Difference from MMR by Body Style",
                height=500,
            )
            fig_right.add_vline(x=0, line_dash="dash", line_color="black")
            fig_right.update_layout(yaxis=dict(autorange="reversed"))

            st.plotly_chart(fig_right, use_container_width=True)



#####################################################################
# Narrative section – buyers vs sellers (simpler language)
#####################################################################
st.subheader("What This View Means 🧭")

if df_filtered.empty:
    st.info("Adjust the filters to see insight bullets here.")
else:
    avg_diff = df_filtered["price_diff"].mean()
    median_diff = df_filtered["price_diff"].median()

    # by-make stats (used mainly for the buyer side)
    make_diff = (
        df_filtered.groupby("make", as_index=False)
        .agg(avg_diff=("price_diff", "mean"), n=("price_diff", "size"))
    )
    make_diff = make_diff[make_diff["n"] >= 100]

    if not make_diff.empty:
        cheapest_row = make_diff.sort_values("avg_diff").iloc[0]
        cheapest_make = cheapest_row["make"]
        cheapest_make_diff = cheapest_row["avg_diff"]
    else:
        cheapest_make = "some makes"
        cheapest_make_diff = median_diff

    # by-body stats (used mainly for the seller side and to tie to the body chart)
    body_diff = (
        df_filtered.groupby("body_clean", as_index=False)
        .agg(avg_diff=("price_diff", "mean"), n=("price_diff", "size"))
    )
    body_diff = body_diff[body_diff["n"] >= 500]

    if not body_diff.empty:
        strongest_body_row = body_diff.sort_values("avg_diff").iloc[-1]
        strongest_body = strongest_body_row["body_clean"]
        strongest_body_diff = strongest_body_row["avg_diff"]
    else:
        strongest_body = "some body styles"
        strongest_body_diff = median_diff

    buyers_col, sellers_col = st.columns(2)

    with buyers_col:
        st.markdown(
            f"""
### For buyers 💸

- In this view, cars sell on average **{abs(avg_diff):,.0f} $ {'below' if avg_diff < 0 else 'above'} MMR**.
- Makes like **{cheapest_make}** in this data are about **{abs(cheapest_make_diff):,.0f} $ {'below' if cheapest_make_diff < 0 else 'above'} MMR**, on average.
- In the body style chart, bars **below 0** mean prices are usually under MMR, which can be better value for you.
            """
        )

    with sellers_col:
        st.markdown(
            f"""
### For sellers 🏷️

- In the body style chart, **{strongest_body}** tends to sell about **{abs(strongest_body_diff):,.0f} $ {'above' if strongest_body_diff > 0 else 'below'} MMR** in this filtered view.
- Bars **above 0** mean prices for that body stype are usually over MMR, so buyers are already paying more than the benchmark for those body styles.
            """
        )

