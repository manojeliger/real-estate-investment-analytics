
-- Project: Real Estate Investment & Property Analytics System
-- Purpose: Answer business questions using analytical views.

-- 1. Top 10 localities by average price per square meter
SELECT
    locality,
    sales_records,
    avg_transaction_value,
    avg_price_per_sqm,
    avg_property_area
FROM locality_price_analysis
ORDER BY avg_price_per_sqm DESC
LIMIT 10;

-- 2. Localities with high prices and sufficient sales activity
SELECT
    locality,
    sales_records,
    avg_price_per_sqm
FROM top_investment_localities
ORDER BY avg_price_per_sqm DESC
LIMIT 10;

-- 3. Monthly sales trends
SELECT
    sales_month,
    total_sales_records,
    total_transaction_value,
    avg_transaction_value
FROM monthly_sales_trends
ORDER BY sales_month;

-- 4. Compare property usage categories
SELECT
    property_usage,
    sales_records,
    avg_transaction_value,
    avg_property_area,
    avg_price_per_sqm
FROM property_usage_analysis
ORDER BY sales_records DESC;
