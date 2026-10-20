# Real Estate Investment & Property Analytics System

## Project Overview

A PostgreSQL-based analytics project that explores Dubai real estate transaction data to compare property prices, analyze sales activity, and investigate differences across localities and property categories.

## Objectives

- Analyze property sales across localities.
- Compare average transaction values and prices per square meter.
- Examine monthly sales activity and transaction values.
- Compare residential and commercial property transactions.
- Explore relationships between property characteristics and recorded prices.

## Technology Stack

- **Database:** PostgreSQL
- **Query Language:** SQL
- **Database Client:** pgAdmin 4
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## Dataset

The project uses a CSV dataset containing Dubai real estate transaction records.

The source includes fields such as transaction date, transaction group, locality, property type, transaction value, property area, ownership type, and nearest metro station.

## Project Structure

```text
real-estate-investment-analytics/
├── data/
├── sql/
│   ├── 01_create_analysis_views.sql
│   └── 02_business_analysis.sql
├── analysis/
├── dashboard/
├── README.md
└── .gitignore
```

## Work Completed

- Created a PostgreSQL database and transaction table.
- Inspected the source dataset and its columns.
- Developed exploratory SQL queries using aggregation, grouping, filtering, and sorting.
- Created reusable views for locality pricing, monthly sales trends, and property usage.
- Created an initial deduplicated working table.
- Began validating data quality and repeated records.

## Current Status

**In progress.** The analytical queries are exploratory. Duplicate imports and source-data duplication still require validation before final transaction counts or investment conclusions can be trusted.

## Planned Improvements

- Validate and clean the dataset.
- Confirm source-data completeness and record uniqueness.
- Add further SQL analyses and documented findings.
- Build visualizations and an interactive dashboard.
- Document reproducible setup and execution steps.

## Disclaimer

This project is intended for educational and exploratory market analysis. Its outputs are not financial advice or guaranteed investment recommendations.