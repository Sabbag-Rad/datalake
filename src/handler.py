import os
import json

def main(event, context):
    if isinstance(event, str):
        event = json.loads(event)

    table = event.get("target_table") or os.environ.get("TARGET_TABLE")
    if not table:
        raise ValueError("No se recibió 'target_table' ni variable de entorno")

    os.environ["TARGET_TABLE"] = table
    from src.etl import run_etl
    run_etl()
