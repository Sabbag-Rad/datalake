# 📊 Conexión de Power BI / R a Data Lake (AWS S3) vía Athena

Este documento describe cómo conectar herramientas de análisis como **Power BI** y **R** al Data Lake almacenado en **Amazon S3**, utilizando **Amazon Athena** como motor de consulta.

---

## ✅ Requisitos Previos

* Acceso a **AWS Athena**
* Permisos para consultar la base de datos: `sabbag_data_lake_raw`
* Athena configurado con S3 para resultados (output location)
* Driver ODBC para Athena instalado
* Power BI Desktop o RStudio instalado

---

## 🔌 Configuración de Athena

* **Bucket de datos:** `sabbag-data-lake-bucket/raw/ris/`
* **Base de datos Glue Catalog:** `sabbag_data_lake_raw`
* **Ubicación de resultados de Athena (Query Result Location):**

  ```
  s3://sabbag-data-lake-bucket/athena/results/
  ```

> Este path debe configurarse en el panel de Athena antes de comenzar.

---

## 🟡 Conexión desde Power BI

### 1. Instalar el Driver ODBC de Athena

* Descargar desde: [https://docs.aws.amazon.com/athena/latest/ug/athena-odbc.html](https://docs.aws.amazon.com/athena/latest/ug/athena-odbc.html)
* Instalar en el equipo local

### 2. Configurar DSN

* Abre `ODBC Data Sources (64-bit)`
* Añade un nuevo DSN:

  * **Driver:** Amazon Athena ODBC
  * **S3 Output Location:** `s3://sabbag-data-lake-bucket/athena/results/`
  * **AWS Region:** `us-east-1`
  * **Authentication Type:** IAM Credentials o Profile (según configuración)
  * **Catalog:** `AwsDataCatalog`
  * **Database:** `sabbag_data_lake_raw`

### 3. Conectarse desde Power BI

* Abrir Power BI Desktop
* Ir a **Inicio → Obtener datos → Otros → ODBC**
* Seleccionar el DSN creado
* Escribir una consulta SQL, por ejemplo:

```sql
SELECT * FROM "sabbag_data_lake_raw"."pacientes" LIMIT 10;
```

---

## 🟢 Conexión desde R

### 1. Instalar paquete `odbc` y `DBI`

```r
install.packages("odbc")
install.packages("DBI")
```

### 2. Conectarse

```r
library(DBI)
library(odbc)

con <- dbConnect(odbc::odbc(),
                 Driver = "Simba Athena ODBC Driver",
                 AwsRegion = "us-east-1",
                 S3OutputLocation = "s3://sabbag-data-lake-bucket/athena/results/",
                 Catalog = "AwsDataCatalog",
                 Schema = "sabbag_data_lake_raw")

df <- dbGetQuery(con, "SELECT * FROM pacientes LIMIT n")
```

> Si usas perfiles de AWS CLI puedes usar `AuthenticationType = "IAM Profile"`.

---

## 📁 Tablas disponibles

* `pacientes`
* `usuarios`
* `convenios`
* `exames`
* `caixa`
* `clinica`
* `contas`
* `dm_tipos_convenio`
* `equip_agendas`
* `equipamentos`
* `faturas`
* `medicos_solicitante`
* `modalidades`
* `planos`
* `procedencias`
* `servicios`

---

## 🧠 Notas

* Power BI y R se conectan a los datos crudos mediante SQL estándar.
* Athena cobra por escaneo de datos → optimiza tus consultas (`LIMIT`, filtros).
* Se recomienda usar particionamiento en S3 para mejor performance.

---

¿Preguntas o problemas? Contacta al equipo de transformación digital.
