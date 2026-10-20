
-- Project: Real Estate Investment & Property Analytics System
-- Purpose: Create reusable SQL views for exploratory analysis.
-- Note: Validate source data and repeated imports before final reporting.

-- 1. Sales summary by locality
CREATE OR REPLACE VIEW sales_locality_summary AS
SELECT
    locality,
    COUNT(*) AS total_sales_records,
    ROUND(AVG(transaction_value), 2) AS avg_transaction_value,
    ROUND(AVG(actual_area), 2) AS avg_property_area
FROM property_transactions
WHERE transaction_group = 'Sales'
  AND transaction_value > 0
  AND actual_area > 0
GROUP BY locality;

-- 2. Price analysis by locality
CREATE OR REPLACE VIEW locality_price_analysis AS
SELECT
    locality,
    COUNT(*) AS sales_records,
    ROUND(AVG(transaction_value), 2) AS avg_transaction_value,
    ROUND(
        AVG(transaction_value / NULLIF(actual_area, 0)),
        2
    ) AS avg_price_per_sqm,
    ROUND(AVG(actual_area), 2) AS avg_property_area
FROM property_transactions_clean
WHERE transaction_group = 'Sales'
  AND transaction_value > 0
  AND actual_area > 0
GROUP BY locality
HAVING COUNT(*) >= 100;

-- 3. Localities eligible for further comparison
CREATE OR REPLACE VIEW top_investment_localities AS
SELECT
    locality,
    sales_records,
    avg_transaction_value,
    avg_price_per_sqm,
    avg_property_area
FROM locality_price_analysis
WHERE sales_records >= 200;

-- 4. Monthly sales trends
CREATE OR REPLACE VIEW monthly_sales_trends AS
SELECT
    DATE_TRUNC('month', instance_date)::DATE AS sales_month,
    COUNT(*) AS total_sales_records,
    ROUND(SUM(transaction_value), 2) AS total_transaction_value,
    ROUND(AVG(transaction_value), 2) AS avg_transaction_value
FROM property_transactions_clean
WHERE transaction_group = 'Sales'
  AND transaction_value > 0
GROUP BY DATE_TRUNC('month', instance_date)
;

-- 5. Comparison by property usage
CREATE OR REPLACE VIEW property_usage_analysis AS
SELECT
    property_usage,
    COUNT(*) AS sales_records,
    ROUND(AVG(transaction_value), 2) AS avg_transaction_value,
    ROUND(AVG(actual_area), 2) AS avg_property_area,
    ROUND(
        AVG(transaction_value / NULLIF(actual_area, 0)),
        2
    ) AS avg_price_per_sqm
FROM property_transactions_clean
WHERE transaction_group = 'Sales'
  AND transaction_value > 0
  AND actual_area > 0
GROUP BY property_usage;
