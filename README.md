# 🛒 Retail Data Platform Modernization: End-to-End Azure Data Engineering Pipeline

## 📌 Project Overview
In today’s retail landscape, fragmented data across IT, marketing, and finance departments often leads to slow, inconsistent, and error-prone decision-making. This project addresses these challenges by implementing a highly automated, end-to-end cloud data architecture on **Microsoft Azure**. 

By orchestrating data ingestion, transformation, and serving, this pipeline guarantees that business stakeholders have access to reliable, high-quality, and up-to-date metrics. The solution leverages the **Medallion Architecture (Bronze, Silver, Gold)** to process raw transactional data into actionable business intelligence, ultimately enabling data-driven strategies for inventory management, sales tracking, and customer segmentation.

## 🛠️ Tech Stack & Services
* **Ingestion & Orchestration:** Azure Data Factory (ADF)
* **Storage:** Azure Data Lake Storage Gen2 (ADLS Gen2)
* **Processing & Transformation:** Databricks (Community Edition), Apache Spark / PySpark
* **Data Formats:** Parquet, Delta Lake
* **Database / Sources:** Azure SQL Database, GitHub API (JSON)
* **Business Intelligence & Visualization:** Power BI Desktop

---

## 🏗️ Architecture & Data Workflow

The pipeline strictly adheres to the Medallion Architecture to ensure data quality and scalability:

### 1. Data Ingestion (Azure Data Factory)
* **Sources:** Connects to an **Azure SQL Database** (Products, Stores, Transactions) and a **Public GitHub API** (Customer JSON data).
* **Process:** Automated ADF pipelines utilize Copy Activities to extract data and load it into the Data Lake.

### 2. Bronze Layer (Raw Data)
* **Storage:** ADLS Gen2.
* **Format:** Parquet.
* **State:** Unmodified, raw data exactly as ingested from the source systems, serving as the historical truth.

### 3. Silver Layer (Cleansed & Conformed Data)
* **Processing:** Databricks (PySpark) mounts the ADLS container to process the Bronze data.
* **Transformations:** * Schema enforcement and data type casting.
  * Deduplication and data quality checks.
  * Joins across `transactions`, `products`, `stores`, and `customers`.
  * Creation of calculated business indicators (e.g., `total_amount = quantity × price`).
* **Format:** Delta Lake for ACID transaction compliance and time travel capabilities.

### 4. Gold Layer (Business Aggregations)
* **Processing:** Databricks aggregates the Silver data to answer specific business questions.
* **Metrics Computed:** Total Quantity Sold, Total Revenue (Chiffre d’affaires), Total Transaction Count, and Average Transaction Value.
* **Format:** Exported for BI consumption.

### 5. Serving & Visualization (Power BI)
* **Dashboarding:** The Gold dataset is connected to Power BI to deliver strategic, interactive dashboards.
* **Key Visuals:** Sales by Date, Sales by Product, Sales by Category, Quantity Sold, and Average Transaction Value.

---

## 📂 Repository Structure
Markdown
# 🛒 Retail Analytics Data Lakehouse on Microsoft Azure

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Apache Spark](https://img.shields.io/badge/apache%20spark-%23E25A1C.svg?style=for-the-badge&logo=apachespark&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=Databricks&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## 📌 Project Overview
This repository contains an end-to-end Data Engineering project implementing a modern **Data Lakehouse** using the **Medallion Architecture (Bronze, Silver, Gold)**. 

The goal of this project is to extract highly normalized transactional and dimensional data from heterogeneous sources (Azure SQL DB and REST APIs), centralize it in a Data Lake, and transform it into a denormalized, business-ready format for Business Intelligence (BI) reporting.

## 🏗️ Architecture & Tech Stack

*(Insert your architecture diagram here. You can upload an image to your `Assets` folder and link it like this: `![Architecture Diagram](Assets/architecture.png)`)*

* **Source Systems:** Azure SQL Database (OLTP), REST API (JSON).
* **Orchestration (ETL/ELT):** Azure Data Factory (ADF).
* **Storage:** Azure Data Lake Storage Gen2 (ADLS Gen2).
* **Compute & Transformation:** Azure Databricks, PySpark.
* **Data Format:** Delta / Parquet.

## 📂 Repository Structure

```text
├── Assets/                                      # Diagrams, screenshots, and architecture images
├── .env                                         # Environment variables (Storage Keys - GitIgnored)
├── .gitignore                                   # Ignored files to maintain repository security
├── Azure Data Lakehouse Implementation.pdf      # Comprehensive technical thesis & project report
├── README.md                                    # Project documentation
└── Retail Analytics with azure.ipynb            # Databricks PySpark notebook (Silver & Gold logic)
⚙️ Data Pipeline Workflow (Medallion Architecture)
🥉 1. Bronze Layer (Raw Data Ingestion)
Orchestrated entirely via Azure Data Factory.

Parallel Execution: Dimension tables (Products, Stores, Customers) are ingested in parallel to optimize DIU (Data Integration Units) usage and reduce latency.

Sequential Dependency: The Fact table (Transactions) is only ingested upon the successful completion of the dimension pipelines to ensure strict referential integrity.

Data is stored in ADLS Gen2 exactly as it appears in the source systems to allow for historical replayability.

🥈 2. Silver Layer (Cleansed & Conformed Data)
Processed using Databricks (PySpark).

Applied strict Data Quality rules: Deduplication (.dropDuplicates()), Null handling (.dropna()), and Data Type Casting.

Enforced Delta Lake Schema Enforcement (overwriteSchema) to protect downstream processes from upstream schema drift.

Added auditing metadata (e.g., ingestion timestamps).

Cleaned data is written back to the silver folder in ADLS Gen2 as Parquet/Delta files.

🥇 3. Gold Layer (Business Aggregations)
Designed for Analytics and BI consumption.

KPI Generation: Joined Fact and Dimension tables to calculate business metrics (e.g., total revenue and units sold per product category).

One Big Table (OBT): Created a denormalized flat table (gold_sales_analytics) to maximize query performance for BI tools like Power BI, preventing the BI engine from executing heavy runtime joins.

Final models are saved to the gold folder in ADLS Gen2.

🚀 How to Run the Project
Clone the repository:

Bash
git clone [https://github.com/yourusername/retail-data-lakehouse-azure.git](https://github.com/yourusername/retail-data-lakehouse-azure.git)
Environment Setup:

Create an Azure Storage Account (ADLS Gen2).

Update the .env file with your specific STORAGE_ACCOUNT_NAME, CONTAINER_NAME, and STORAGE_ACCOUNT_KEY. (Note: Never commit your .env file).

Databricks Execution:

Import Retail Analytics with azure.ipynb into your Databricks workspace.

Attach it to a compute cluster and Run All cells to process the data from Bronze ➔ Silver ➔ Gold.

📄 Detailed Report
For a deep dive into the architectural decisions, pipeline configurations, and linked services setup, please refer to the attached Azure Data Lakehouse Implementation.pdf included in this repository.

Developed by Mohamed Marra | LinkedIn Profile


***

### 💡 Final Steps for you:
1. Copy the Markdown above into your `README.md`.
2. Replace `yourusername` and `yourprofile` in the links near the bottom with your actual GitHub username and LinkedIn URL.
3. If you have a nice picture of your ADF pipeline or an architecture diagram, put it in the `Assets` folder and uncomment the image link in the README.
4. Commit and push! 

This repository is now officially a top-tier showcase of your Data Engineering skills. Excellent work getting this all put together! Ready to tackle the next project for the portfolio?
