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

```text
├── databricks/
│   ├── 01_mount_adls.py         # Script to mount ADLS Gen2 to Databricks
│   ├── 02_silver_layer.ipynb    # Cleaning, joining, and Delta table creation
│   └── 03_gold_layer.ipynb      # Business aggregations and final dataset generation
├── adf_pipelines/
│   └── Ingestion_Pipeline.json  # Exported ARM template/JSON for Data Factory
├── docs/
│   ├── architecture_diagram.png # Visual representation of the Azure pipeline
│   └── Technical_Report.pdf     # Detailed documentation of services and end-to-end flow
├── powerbi/
│   └── Retail_Dashboard.pbix    # Final Power BI Dashboard
└── README.md
````

## 🚀 How to Run the Project

**1. Environment Setup:**
* Provision an Azure SQL Database and execute the initial DDL/DML scripts to generate the dummy data.
* Provision an Azure Storage Account, enabling Hierarchical Namespace (ADLS Gen2), and create the `bronze`, `silver`, and `gold` directory structure.

**2. Orchestration:**
* Import the pipeline JSON into Azure Data Factory.
* Configure the Linked Services for Azure SQL, the HTTP API, and ADLS Gen2.
* Trigger the pipeline to populate the Bronze layer.

**3. Data Transformation:**
* Import the notebooks into Databricks.
* Execute `01_mount_adls.py` to establish the connection with your Azure Storage.
* Run the Silver and Gold notebooks sequentially to clean, transform, and aggregate the data.

**4. Visualization:**
* Open `Retail_Dashboard.pbix` in Power BI Desktop.
* Refresh the data source to pull the latest Gold layer dataset.

---

## 👨‍💻 Author

**Marra Mohamed**  
*Data Analyst & Data Engineer*  
[LinkedIn](https://www.linkedin.com/in/marra-mohamed/) | [Portfolio](#)
