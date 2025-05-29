# Proyecto: ETL Data Lake - RIS

Este proyecto construye un pipeline de ingesta cruda de datos médicos desde una base de datos PostgreSQL hacia un data lake en AWS. Los datos se exponen para consulta analítica mediante Athena.

---

## 🧱 Arquitectura General

```
PostgreSQL → Lambda ETL → S3 (raw/ris) → Glue Crawler → Glue Catalog → Athena
```

---

## 📂 Estructura del proyecto

```
etl-data-lake/
├── src/
│   ├── etl.py
│   ├── secrets.py
│   └── s3_utils.py
├── handler.py
├── requirements.txt
├── serverless.yml
├── events.yml
├── .env
```

---

## ✅ Servicios AWS utilizados

| Servicio         | Función                                      |
|------------------|----------------------------------------------|
| Lambda           | Extrae y carga `.csv` por tabla              |
| EventBridge      | Ejecuta la misma función Lambda múltiples veces por tabla |
| S3               | Almacén de archivos `.csv` (`raw/ris/`)      |
| Glue Catalog     | Registra los `.csv` como tablas              |
| Glue Crawler     | Detecta y cataloga los archivos en S3        |
| Athena           | Consulta directa con SQL sobre los `.csv`    |
| Secrets Manager  | Guarda credenciales de PostgreSQL            |
| SNS + CloudWatch | (opcional) alertas de error y monitoreo      |

---

## ⏱️ Tiempos de ejecución

| Componente   | Hora COL | Hora UTC | Cron                |
|--------------|----------|----------|---------------------|
| Lambda ETL   | 12 AM    | 5 AM     | `cron(0 5 * * ? *)` |
| Glue Crawler | 1 AM     | 6 AM     | `cron(0 6 * * ? *)` |

---

## 🛠️ Configuración manual

### S3:
- Bucket: `sabbag-data-lake-bucket`
- Carpeta: `raw/ris/`

### Glue:
- Database: `sabbag_data_lake_raw`
- Crawler:
  - Ruta: `s3://sabbag-data-lake-bucket/raw/ris/`
  - Horario: 1 AM Colombia
  - Rol: `glue-crawler-role`

### Athena:
- Base: `sabbag_data_lake_raw`
- Resultados: `s3://sabbag-data-lake-bucket/athena-results/`
- Consulta de prueba:
  ```sql
  SELECT * FROM pacientes LIMIT 10;
  ```

---

## 🔐 Política IAM para Glue Crawler

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::sabbag-data-lake-bucket",
        "arn:aws:s3:::sabbag-data-lake-bucket/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["glue:*", "logs:*"],
      "Resource": "*"
    }
  ]
}
```

---

## 📦 Deploy con Serverless

```bash
serverless deploy
```

---

## 🔁 EventBridge externo (`events.yml`)

Las ejecuciones por tabla están definidas en un archivo externo `events.yml` y referenciadas así:

```yaml
functions:
  etlIngest:
    handler: handler.main
    timeout: 300
    environment:
      BUCKET_NAME: sabbag-data-lake-bucket
      DB_MEDILAB_SECRET_ARN: ${env:DB_MEDILAB_SECRET_ARN}
    events: ${file(./events.yml):etlIngest}
```

Cada entrada programada ejecuta la función con un `input` diferente como:

```yaml
- eventBridge:
    schedule: cron(0 5 * * ? *)
    input:
      target_table: usuarios
```

---

