import pandas as pd
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq

def normalize_price(value):
    """
    Normalizes price to a numeric amount.
    Handles:
    - float / int
    - {"amount": x, "currency": y}
    - null / missing
    """
    if isinstance(value, dict):
        return value.get("amount")
    return value

def build_bronze():
    base = Path("/opt/airflow/dags")

    raw_path = base / "data/raw/stream_logs.jsonl"
    bronze_path = base / "data/bronze/stream_logs_bronze.parquet"

    bronze_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "event_id",
        "booking_id",
        "airline",
        "action",
        "status",
        "timestamp",
        "price_amount",
    ]

    writer = None

    for chunk in pd.read_json(raw_path, lines=True, chunksize=20_000):
        # Normalize price
        chunk["price_amount"] = chunk.get("price").apply(normalize_price)

        # Ensure all expected columns exist
        for col in columns:
            if col not in chunk.columns:
                chunk[col] = None

        # Enforce canonical schema
        chunk = chunk[columns]

        table = pa.Table.from_pandas(chunk, preserve_index=False)

        if writer is None:
            writer = pq.ParquetWriter(bronze_path, table.schema)

        writer.write_table(table)

    if writer:
        writer.close()
