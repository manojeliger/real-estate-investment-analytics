
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

db = st.secrets["postgres"]

connection_url = URL.create(
    drivername="postgresql+psycopg",
    username=db["username"],
    password=db["password"],
    host=db["host"],
    port=db["port"],
    database=db["database"],
)

engine = create_engine(connection_url)

try:
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    locality,
                    sales_records,
                    avg_transaction_value,
                    avg_price_per_sqm,
                    avg_property_area
                FROM locality_price_analysis
                ORDER BY avg_price_per_sqm DESC
                LIMIT 10
            """)
        )

        rows = result.fetchall()

        print("View query successful!")
        print("Rows returned:", len(rows))
        print()
        print(
            f"{'Locality':<30} {'Sales':>8} "
            f"{'Avg Price/m²':>15}"
        )
        print("-" * 58)

        for row in rows:
            print(
                f"{row.locality[:29]:<30} "
                f"{row.sales_records:>8} "
                f"{row.avg_price_per_sqm:>15,.2f}"
            )

except Exception as error:
    print("View query failed.")
    print("Error type:", type(error).__name__)
    print("Check that the view exists in the configured database.")

finally:
    engine.dispose()
