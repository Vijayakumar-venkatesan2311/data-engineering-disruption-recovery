from pathlib import Path
from collections import defaultdict
import pyarrow.parquet as pq
import pandas as pd

def build_silver():
    base = Path("/opt/airflow/dags")

    bronze_path = base / "data/bronze/stream_logs_bronze.parquet"
    silver_path = base / "data/silver/booking_instability.parquet"

    silver_path.parent.mkdir(parents=True, exist_ok=True)

    # Accumulators
    total_events = defaultdict(int)
    statuses = defaultdict(set)
    airlines = defaultdict(set)
    cancel_signal = defaultdict(int)

    parquet = pq.ParquetFile(bronze_path)

    # Read ONE row group at a time (true streaming)
    for i in range(parquet.num_row_groups):
        table = parquet.read_row_group(i)
        df = table.to_pandas()

        for _, row in df.iterrows():
            booking_id = row["booking_id"]
            if pd.isna(booking_id):
                continue

            total_events[booking_id] += 1
            statuses[booking_id].add(row["status"])
            airlines[booking_id].add(row["airline"])

            if row["action"] in ("CANCEL_REQUEST", "REFUND"):
                cancel_signal[booking_id] = 1

        # Explicitly free memory
        del df
        del table

    records = []
    for booking_id in total_events:
        record = {
            "booking_id": booking_id,
            "total_events": total_events[booking_id],
            "distinct_statuses": len(statuses[booking_id]),
            "distinct_airlines": len(airlines[booking_id]),
            "has_cancel_signal": cancel_signal[booking_id],
        }
        record["instability_score"] = (
            record["distinct_statuses"]
            + record["distinct_airlines"]
            + record["has_cancel_signal"]
        )
        records.append(record)

    silver_df = pd.DataFrame(records)
    silver_df.to_parquet(silver_path, index=False)
