import os
import pandas as pd
import psycopg2
from src.secrets import get_db_credentials
from src.s3_utils import upload_csv_to_s3

def run_etl():
    table = os.environ.get("TARGET_TABLE")
    if not table:
        raise ValueError("Falta la variable de entorno TARGET_TABLE.")

    print(f"[ETL][{table}] 🟡 Iniciando proceso...")

    try:
        creds = get_db_credentials()
        print("[ETL] ✅ Credenciales obtenidas")

        conn = psycopg2.connect(
            host=creds['host'],
            port=creds['port'],
            dbname=creds['dbname'],
            user=creds['username'],
            password=creds['password']
        )
        print(f"[ETL][{table}] 🔌 Conectado a PostgreSQL")

        query = f'SELECT * FROM {table}'
        df = pd.read_sql(query, conn)
        conn.close()

        if df.empty:
            print(f"[ETL][{table}] ⚠️ Tabla sin registros. Se omitirá carga en S3.")
            return

        print(f"[ETL][{table}] ✅ Registros extraídos: {len(df)}")

        bucket = os.environ['BUCKET_NAME']
        s3_key = f'raw/ris/{table}.csv'

        upload_csv_to_s3(df, bucket, s3_key)
        print(f"[ETL][{table}] 🟢 Carga exitosa a s3://{bucket}/{s3_key}")

    except Exception as e:
        print(f"[ETL][{table}] 🔴 Error en la ejecución: {str(e)}")
        raise