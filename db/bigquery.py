from typing import Callable, Any

from google.cloud import bigquery

BQ_CLIENT = bigquery.Client()

DATASET = "JobNimbus"
ID_KEY = "_id"
TIME_KEY = "_batched_at"

Schema = list[dict[str, Any]]


def id_schema(schema: Schema) -> Schema:
    return [
        {"name": ID_KEY, "type": "STRING"},
        *schema,
        {"name": "_batched_at", "type": "TIMESTAMP"},
    ]


def load(table: str, schema: Schema, update=False) -> Callable[[list[dict]], int]:
    def _load(rows: list[dict]) -> int:
        if len(rows) == 0:
            return 0

        output_rows = (
            BQ_CLIENT.load_table_from_json(
                rows,
                f"{DATASET}.{table}",
                job_config=bigquery.LoadJobConfig(
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_APPEND" if update else "WRITE_TRUNCATE",
                    schema=schema,
                ),
            )
            .result()
            .output_rows
        )
        
        if update:
            _update(table)

        return output_rows

    return _load


def _update(table: str) -> None:
    BQ_CLIENT.query(
        f"""
    CREATE OR REPLACE TABLE {DATASET}.{table} AS
    SELECT * EXCEPT (row_num)
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY {ID_KEY} ORDER BY {TIME_KEY} DESC)
            AS row_num
        FROM {DATASET}.{table}
    ) WHERE row_num = 1"""
    ).result()
