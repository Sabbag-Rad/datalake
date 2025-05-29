import boto3
from io import StringIO

def upload_csv_to_s3(df, bucket_name, key):
    try:
        s3 = boto3.client('s3')
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        s3.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())
        print(f"[S3] ✅ Archivo CSV subido a {bucket_name}/{key}")
    except Exception as e:
        print(f"[S3] 🔴 Error al subir archivo CSV: {str(e)}")
        raise
