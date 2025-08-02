# 🔁 End-to-End Data Pipeline: Fivetran → Databricks Lakehouse (DLT, CDC, SCD)

This project showcases a production-grade data pipeline using **Fivetran**, **Google Drive**, **PySpark**, **Databricks**, **Delta Live Tables (DLT)**, and **Delta Lake**. The pipeline automates ingestion, transformation, and CDC/SCD handling on top of a Lakehouse architecture using **LakeFlow** declarative pipelines.

---

## 📐 Architecture Overview

> 📌 *Embed your architecture diagram below:*

![Architecture Diagram](images/architecture-diagram.png)

---

## 🧰 Tools & Technologies

| Tool                     | Purpose                                                       |
|--------------------------|---------------------------------------------------------------|
| **Fivetran**             | Automated ingestion from Google Drive                         |
| **Google Drive**         | Source of raw CSV/Excel data                                  |
| **Databricks**           | Cloud data platform for large-scale data processing           |
| **Auto Loader**          | Efficient schema evolution + file streaming into Bronze layer |
| **PySpark & Spark SQL**  | Batch + streaming transformations in Silver layer             |
| **Delta Live Tables (DLT)** | CDC and SCD management using declarative pipelines       |
| **LakeFlow**             | Visual orchestration of pipelines and job management          |
| **Delta Lake**           | ACID-compliant data lake storage with time travel             |

---

## 🔄 Pipeline Flow

1. **Ingestion (Bronze Layer)**
   - Raw data is ingested from Google Drive using Fivetran.
   - Databricks Auto Loader streams data into the Bronze Delta table with schema inference.

2. **Transformation (Silver Layer)**
   - PySpark and Spark SQL clean, filter, normalize, and enrich data.
   - Stored as structured Delta tables.

3. **CDC & SCD Handling (Gold Layer)**
   - Delta Live Tables (DLT) applies declarative CDC and SCD logic.
   - Runs on LakeFlow for orchestration, scheduling, and lineage tracking.

4. **Output**
   - Final business-ready datasets stored in Delta format.
   - Ready for BI tools, analytics, or ML consumption.

---

## 🧪 Code Example (DLT CDC Table)

```python
@dlt.table(
    comment="Gold table with CDC applied"
)
@dlt.expect_or_drop("not_null_id", "customer_id IS NOT NULL")
def gold_customers():
    df = dlt.read_stream("silver_customers")
    return (
        df.dropDuplicates(["customer_id"])
          .withWatermark("updated_at", "2 hours")
    )
# databricks_etl_project
