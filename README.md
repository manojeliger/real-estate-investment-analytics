<<<<<<< HEAD

# Dubai Real Estate Investment & Property Analytics

An end-to-end data analytics project using PostgreSQL, Python, Pandas, Plotly, and Streamlit to explore Dubai property transaction records.

## Project Objectives

- Analyze property sales across localities.
- Compare average transaction values and prices per square meter.
- Explore monthly sales activity and transaction-value trends.
- Compare property types and usage categories.
- Present insights through an interactive dashboard.

## Technology Stack

- **Database:** PostgreSQL
- **Querying:** SQL, analytical views, aggregations
- **Application:** Python, Streamlit
- **Data processing:** Pandas
- **Visualization:** Plotly
- **Version control:** Git and GitHub

## Dashboard Features

- KPI cards summarizing locality-level results.
- Interactive locality price comparison.
- Minimum-sales filter and searchable locality table.
- CSV export of filtered locality data.
- Monthly sales and transaction-value trends.
- Property-type and property-usage comparisons.

## Project Structure

```text
real-estate-investment-analytics/
├── .streamlit/          # Local Streamlit configuration
├── analysis/            # Analysis work
├── dashboard/           # Dashboard-related assets
├── data/                # Local datasets (not committed)
├── sql/                 # SQL analysis scripts
├── app.py               # Streamlit application
├── test_connection.py   # PostgreSQL connection test
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

## Run Locally

1. Install Python and PostgreSQL.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create `.streamlit/secrets.toml` with your local PostgreSQL credentials:

   ```toml
   [postgres]
   host = "localhost"
   port = 5432
   database = "postgres"
   username = "postgres"
   password = "YOUR_LOCAL_PASSWORD"
   ```

5. Ensure the database contains the required analytical views.
6. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Data Quality and Limitations

- The raw dataset contains 179,229 records.
- Exact full-row deduplication produced 178,744 distinct rows.
- Repeated transaction IDs do not necessarily indicate duplicate transactions.
- Current analytical views use `property_transactions_analytics`.
- September 2025 is incomplete in the available dataset.
- Currency units must be confirmed against the source documentation before interpreting monetary figures.
- Results are descriptive and are not investment advice.

## Future Improvements

- Validate transaction semantics and source currency.
- Add data-quality reporting and clearer metric definitions.
- Add locality and property filters across all dashboard sections.
- Improve deployment and automated testing.
- Publish a demo and dashboard screenshots.

## Status

The local Streamlit dashboard is connected to PostgreSQL and includes locality, monthly trend, property-type, and property-usage analysis.
=======
# real-estate-investment-analytics
Interactive real estate analytics dashboard using PostgreSQL, Python, and Streamlit.
>>>>>>> origin/main
