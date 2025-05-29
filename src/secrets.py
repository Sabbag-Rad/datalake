import boto3
import json
import os

def get_db_credentials():
    secret_arn = os.environ['DB_MEDILAB_SECRET_ARN']
    region = os.environ.get('AWS_REGION', 'us-east-1')

    try:
        client = boto3.client('secretsmanager', region_name=region)
        response = client.get_secret_value(SecretId=secret_arn)
        secret = json.loads(response['SecretString'])

        required_keys = ['host', 'port', 'dbname', 'username', 'password']
        for key in required_keys:
            if key not in secret:
                raise KeyError(f"Clave faltante en el secreto: {key}")

        return secret

    except Exception as e:
        print(f"[SECRETS] 🔴 Error al obtener las credenciales: {str(e)}")
        raise
