# Data-Engineering-Disruption-Recovery

**Problem**: Disruption recovery intelligence system for a travel platform experiencing conflicting airline event signals and internal booking state during large-scale outages

**Goals**: Decision ready signals under disruption

# Disruption Recovery Pipeline

This project demonstrates a simple disruption recovery pipeline for a travel agency using Apache Airflow.

## Architecture
- Raw logs are ingested as-is
- Bronze layer structures raw events
- Silver layer detects booking instability
- Gold layer produces a decision-ready view using booking truth


## How to Run
1. Start Airflow using docker-compose
2. Open Airflow UI at http://localhost:8080
3. Enable `disruption_recovery_medallion`
4. Trigger the DAG manually

## Output
Final output is written to:
`data/gold/booking_decision_view.parquet`

