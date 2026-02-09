import pandas as pd
from pathlib import Path

# Business priority mapping
TIER_PRIORITY = {
    "PLATINUM": 4,
    "GOLD": 3,
    "SILVER": 2,
    "BRONZE": 1,
}

def build_gold():
    base = Path("/opt/airflow/dags")

    silver_path = base / "data/silver/booking_instability.parquet"
    master_path = base / "bookings_master.parquet"
    gold_path   = base / "data/gold/booking_decision_view.parquet"

    gold_path.parent.mkdir(parents=True, exist_ok=True)

    # Read inputs
    silver_df = pd.read_parquet(silver_path)
    master_df = pd.read_parquet(master_path)

    # Join instability signals with customer ownership
    df = silver_df.merge(
        master_df,
        on="booking_id",
        how="left"
    )

    # Map customer tier to numeric priority
    df["tier_priority"] = (
        df["tier"]
        .map(TIER_PRIORITY)
        .fillna(0)
        .astype(int)
    )

    # Final decision score
    df["decision_score"] = (
        df["instability_score"] * 10
        + df["tier_priority"]
    )

    # Sort for operational consumption
    df = df.sort_values(
        by="decision_score",
        ascending=False
    )

    # Persist Gold layer
    df.to_parquet(gold_path, index=False)
