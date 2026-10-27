# Data Quality ETL Pipeline

## Overview
A Python-based ETL pipeline that cleans sales data, validates records, and loads valid and rejected records into separate SQLite tables.

## Technologies
- Python
- Pandas
- SQLite
- SQL
- Logging

## Workflow
1. Extract raw records from a CSV file.
2. Validate required values and numeric fields.
3. Detect duplicate order IDs and invalid quantities or prices.
4. Separate clean records from rejected records.
5. Calculate revenue for valid records.
6. Load results into SQLite.
7. Verify record counts and rejection reasons using SQL.

## Database Tables
- `sales`: validated sales records.
- `rejected_records`: rejected records with reasons.

## How to Run
1. Install dependencies: `python -m pip install pandas`
2. Run the pipeline: `python main.py`
3. Validate results: `python validate.py`

## Learning Outcomes
This project demonstrates ETL, data-quality validation, data cleaning, SQL database loading, logging, and rejected-record handling.

## Limitations
This is a local learning project using sample data and SQLite. It does not yet include scheduling, cloud deployment, or incremental loading.