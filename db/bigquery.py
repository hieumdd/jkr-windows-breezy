from typing import Any

from google.cloud import bigquery

BQ_CLIENT = bigquery.Client()

DATASET = "Breezy"


def load(table: str, schema: list[dict[str, Any]]):
    def _load(rows: list[dict]) -> int:
        if len(rows) == 0:
            return 0

        output_rows = (
            BQ_CLIENT.load_table_from_json(
                rows,
                f"{DATASET}.{table}",
                job_config=bigquery.LoadJobConfig(
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_TRUNCATE",
                    schema=schema,
                ),
            )
            .result()
            .output_rows
        )

        return output_rows

    return _load
