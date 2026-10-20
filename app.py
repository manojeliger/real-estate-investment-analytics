
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Dubai Real Estate Analytics",
    page_icon="🏙️",
    layout="wide",
)

st.title("🏙️ Dubai Real Estate Investment Analytics")
st.caption(
    "Explore locality prices, property values, and sales activity."
)

# --------------------------------------------------
# PostgreSQL connection
# --------------------------------------------------
@st.cache_resource
def get_engine():
    db = st.secrets["postgres"]

    url = URL.create(
        drivername="postgresql+psycopg",
        username=db["username"],
        password=db["password"],
        host=db["host"],
        port=db["port"],
        database=db["database"],
    )

    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=300)
def load_locality_data():
    query = text("""
        SELECT
            locality,
            sales_records,
            avg_transaction_value,
            avg_price_per_sqm,
            avg_property_area
        FROM locality_price_analysis
        WHERE locality IS NOT NULL
        ORDER BY avg_price_per_sqm DESC
    """)

    with get_engine().connect() as connection:
        return pd.read_sql(query, connection)


try:
    df = load_locality_data()

except Exception as error:
    st.error("Unable to load data from PostgreSQL.")
    st.caption(
        f"Error type: {type(error).__name__}. "
        "Check your database settings and SQL view."
    )
    st.stop()

if df.empty:
    st.warning("No locality data was returned.")
    st.stop()

# --------------------------------------------------
# Sidebar filters
# --------------------------------------------------
st.sidebar.header("Dashboard Filters")

minimum_sales = st.sidebar.slider(
    "Minimum sales records per locality",
    min_value=100,
    max_value=max(100, int(df["sales_records"].max())),
    value=200,
    step=50,
)

filtered_df = df[df["sales_records"] >= minimum_sales].copy()

if filtered_df.empty:
    st.warning("No localities match this filter.")
    st.stop()

# --------------------------------------------------
# KPI cards
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Eligible Localities", f"{len(filtered_df):,}")
col2.metric(
    "Sales Records in View",
    f"{filtered_df['sales_records'].sum():,}",
)
col3.metric(
    "Highest Average Price / m²",
    f"{filtered_df['avg_price_per_sqm'].max():,.2f}",
)
col4.metric(
    "Average Transaction Value",
    f"{filtered_df['avg_transaction_value'].mean():,.0f}",
)

st.caption(
    "Metrics reflect the filtered localities. "
    "Currency units are not labelled until confirmed from source documentation."
)

st.divider()

# --------------------------------------------------
# Locality price chart
# --------------------------------------------------
st.subheader("Locality Price Comparison")

top_n = st.selectbox(
    "Number of localities to display",
    options=[10, 15, 20, 30],
    index=0,
)

chart_df = filtered_df.nlargest(top_n, "avg_price_per_sqm")
chart_df = chart_df.sort_values("avg_price_per_sqm")

fig = px.bar(
    chart_df,
    x="avg_price_per_sqm",
    y="locality",
    orientation="h",
    color="avg_price_per_sqm",
    color_continuous_scale="Blues",
    hover_data={
        "sales_records": True,
        "avg_transaction_value": ":,.2f",
        "avg_property_area": ":,.2f",
        "avg_price_per_sqm": ":,.2f",
    },
    labels={
        "avg_price_per_sqm": "Average price per m²",
        "locality": "Locality",
        "sales_records": "Sales records",
        "avg_transaction_value": "Average transaction value",
        "avg_property_area": "Average property area",
    },
)

fig.update_layout(
    height=max(450, len(chart_df) * 34),
    coloraxis_showscale=False,
    yaxis_title=None,
    xaxis_title="Average price per square meter",
    margin=dict(l=10, r=20, t=25, b=10),
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Locality data table
# --------------------------------------------------
st.subheader("Locality Details")

search = st.text_input("Search for a locality")

table_df = filtered_df.copy()

if search.strip():
    table_df = table_df[
        table_df["locality"].str.contains(
            search.strip(),
            case=False,
            na=False,
        )
    ]

st.dataframe(
    table_df.sort_values("avg_price_per_sqm", ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "locality": st.column_config.TextColumn("Locality"),
        "sales_records": st.column_config.NumberColumn(
            "Sales Records", format="%d"
        ),
        "avg_transaction_value": st.column_config.NumberColumn(
            "Average Transaction Value", format="%,.2f"
        ),
        "avg_price_per_sqm": st.column_config.NumberColumn(
            "Average Price / m²", format="%,.2f"
        ),
        "avg_property_area": st.column_config.NumberColumn(
            "Average Property Area", format="%,.2f"
        ),
    },
)

st.download_button(
    "Download filtered locality data (CSV)",
    data=table_df.to_csv(index=False).encode("utf-8"),
    file_name="dubai_locality_analysis.csv",
    mime="text/csv",
)


# --------------------------------------------------
# Property type analysis
# --------------------------------------------------
st.divider()
st.subheader("Property Type Analysis")


@st.cache_data(ttl=300)
def load_property_types():
    query = text("""
        SELECT
            property_type,
            property_sub_type,
            sales_records,
            avg_transaction_value,
            avg_price_per_sqm,
            avg_property_area
        FROM property_type_analysis
        ORDER BY sales_records DESC
    """)

    with get_engine().connect() as connection:
        return pd.read_sql(query, connection)


try:
    property_df = load_property_types()

    if not property_df.empty:
        property_df["property_category"] = (
            property_df["property_type"].fillna("Unknown")
            + " / "
            + property_df["property_sub_type"].fillna("Unspecified")
        )

        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown("#### Sales by property category")

            sales_fig = px.bar(
                property_df.head(10).sort_values("sales_records"),
                x="sales_records",
                y="property_category",
                orientation="h",
                labels={
                    "sales_records": "Sales records",
                    "property_category": "Property category",
                },
                color="sales_records",
                color_continuous_scale="Blues",
            )

            sales_fig.update_layout(
                height=480,
                coloraxis_showscale=False,
                yaxis_title=None,
            )

            st.plotly_chart(sales_fig, use_container_width=True)

        with right_col:
            st.markdown("#### Average price per square meter")

            price_fig = px.bar(
                property_df.nlargest(
                    10, "avg_price_per_sqm"
                ).sort_values("avg_price_per_sqm"),
                x="avg_price_per_sqm",
                y="property_category",
                orientation="h",
                labels={
                    "avg_price_per_sqm": "Average price per m²",
                    "property_category": "Property category",
                },
                color="avg_price_per_sqm",
                color_continuous_scale="Teal",
            )

            price_fig.update_layout(
                height=480,
                coloraxis_showscale=False,
                yaxis_title=None,
            )

            st.plotly_chart(price_fig, use_container_width=True)

        st.markdown("#### Detailed property statistics")

        display_property_df = property_df[
            [
                "property_type",
                "property_sub_type",
                "sales_records",
                "avg_transaction_value",
                "avg_price_per_sqm",
                "avg_property_area",
            ]
        ].rename(
            columns={
                "property_type": "Property Type",
                "property_sub_type": "Property Subtype",
                "sales_records": "Sales Records",
                "avg_transaction_value": "Average Transaction Value",
                "avg_price_per_sqm": "Average Price / m²",
                "avg_property_area": "Average Property Area",
            }
        )

        st.dataframe(
            display_property_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sales Records": st.column_config.NumberColumn(
                    format="%d"
                ),
                "Average Transaction Value": st.column_config.NumberColumn(
                    format="%,.2f"
                ),
                "Average Price / m²": st.column_config.NumberColumn(
                    format="%,.2f"
                ),
                "Average Property Area": st.column_config.NumberColumn(
                    format="%,.2f"
                ),
            },
        )

    else:
        st.info("No property-type data is available.")

except Exception as error:
    st.error("Could not load property-type analysis.")
    st.caption(f"Error type: {type(error).__name__}")


st.caption(
    "Data source: PostgreSQL analytical view. "
    "Figures are descriptive and are not investment advice."
)

# --------------------------------------------------
# Monthly market trends
# --------------------------------------------------
st.divider()
st.subheader("Monthly Sales Trends")

@st.cache_data(ttl=300)
def load_monthly_trends():
    query = text("""
        SELECT
            sales_month,
            total_sales_records,
            total_transaction_value,
            avg_transaction_value
        FROM monthly_sales_trends
        ORDER BY sales_month
    """)

    with get_engine().connect() as connection:
        return pd.read_sql(query, connection)


try:
    monthly_df = load_monthly_trends()

    if not monthly_df.empty:
        monthly_df["sales_month"] = pd.to_datetime(
            monthly_df["sales_month"]
        )

        metric_choice = st.radio(
            "Choose a trend",
            ["Number of sales", "Total transaction value"],
            horizontal=True,
        )

        if metric_choice == "Number of sales":
            y_column = "total_sales_records"
            y_label = "Sales records"
        else:
            y_column = "total_transaction_value"
            y_label = "Total transaction value (source currency)"

        monthly_fig = px.line(
            monthly_df,
            x="sales_month",
            y=y_column,
            markers=True,
            title=metric_choice + " by month",
            labels={
                "sales_month": "Month",
                y_column: y_label,
            },
        )

        monthly_fig.update_layout(
            xaxis_title="Month",
            yaxis_title=y_label,
        )

        st.plotly_chart(
            monthly_fig,
            use_container_width=True,
        )

       
        display_monthly = monthly_df.copy()

        display_monthly["sales_month"] = (
            display_monthly["sales_month"].dt.strftime("%b %Y")
        )

        display_monthly = display_monthly.rename(
            columns={
                "sales_month": "Month",
                "total_sales_records": "Sales Records",
                "total_transaction_value": "Total Transaction Value",
                "avg_transaction_value": "Average Transaction Value",
            }
        )

        st.dataframe(
            display_monthly,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Sales Records": st.column_config.NumberColumn(
                    format="%d"
                ),
                "Total Transaction Value": st.column_config.NumberColumn(
                    format="%,.2f"
                ),
                "Average Transaction Value": st.column_config.NumberColumn(
                    format="%,.2f"
                ),
            },
        )

    else:
        st.info("No monthly trend data is available.")

except Exception as error:
    st.error("Could not load monthly sales trends.")
    st.caption(f"Error type: {type(error).__name__}")
