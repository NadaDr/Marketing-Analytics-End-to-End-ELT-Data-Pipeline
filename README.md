# Marketing Analytics — End-to-End ELT Data Pipeline

An end-to-end data engineering project that builds a marketing analytics pipeline using Python, Snowflake, dbt, Apache Airflow, Docker, and Power BI.

The project demonstrates how raw marketing data can be ingested, transformed, tested, and prepared for business intelligence and analytical reporting.

## Architecture

```text
             Raw Marketing Data
                      |
                      v
              Python Ingestion
                      |
                      v
                  Snowflake
                 RAW Layer
                      |
                      v
                 dbt Models
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Staging   Intermediate    Marts
          |           |           |
          +-----------+-----------+
                      |
                      v
              Analytics Tables
                      |
                      v
                 Power BI
                      |
                      v
             Marketing Dashboards

          Apache Airflow
       Pipeline Orchestration
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data ingestion and loading |
| Snowflake | Cloud data warehouse |
| dbt | SQL transformations and data testing |
| Apache Airflow | Workflow orchestration |
| Docker | Containerized environment |
| Power BI | Business intelligence and visualization |
| Git & GitHub | Version control |

## Dataset

The project uses a synthetic marketing campaigns dataset containing five Parquet files:

| Dataset | Description | Rows |
|---|---|---:|
| Channels | Marketing channel information | 9 |
| Campaigns | Campaign details and budgets | 600 |
| Ad Groups | Advertising group information | 3,000 |
| Daily Performance | Daily advertising metrics | 260,000 |
| Conversions | Conversion events and attribution | 40,000 |
| **Total** | | **303,609** |

## Data Pipeline

### 1. Data Ingestion — Python

- Read source Parquet files.
- Inspect and validate incoming data.
- Load raw datasets into Snowflake.
- Handle timestamp formatting during ingestion.

### 2. Data Warehouse — Snowflake

Raw data is stored in the `MARKETING_ANALYTICS_DB` database, under the `RAW` schema.

### 3. Data Transformation — dbt

The dbt project follows a layered transformation approach:

**Staging**
- Standardizes and prepares raw source data.
- Creates one staging model for each source table.

**Intermediate**
- Applies business logic.
- Prepares campaign, ad group, daily performance, and conversion attribution data.

**Marts**
- Builds analytics-ready dimensions and fact tables.

| Model | Type |
|---|---|
| DIM_CHANNELS | Dimension |
| DIM_CAMPAIGNS | Dimension |
| DIM_AD_GROUPS | Dimension |
| DIM_DATE | Dimension |
| FCT_DAILY_PERFORMANCE | Fact |
| FCT_CONVERSION_ATTRIBUTION | Fact |

### 4. Data Quality

dbt tests are used to validate model quality, including key constraints and data integrity.

**Latest validation results:**
- Staging: 18 tests passed
- Intermediate: 14 tests passed
- Marts: 23 tests passed

### 5. Orchestration — Apache Airflow

Airflow is used to define and orchestrate the pipeline workflow. The DAG and containerized environment are included in this repository. The orchestration workflow is still being aligned with the final ingestion implementation.

### 6. Business Intelligence — Power BI

The Snowflake Gold-layer tables are connected to Power BI to support marketing performance analysis.

Planned dashboard areas include:

- Marketing Overview
- Performance & Optimization
- Advanced Marketing Intelligence

## Key Marketing Metrics

The analytics layer supports metrics such as:

- Impressions and clicks
- Click-through rate (CTR)
- Cost per click (CPC)
- Conversion rate
- Advertising spend
- Revenue
- Return on ad spend (ROAS)
- First-touch and last-touch attribution

## Project Structure

```text
marketing-analytics-elt/
│
├── airflow/
│   ├── dags/
│   ├── Dockerfile
│   └── docker-compose.yaml
│
├── data