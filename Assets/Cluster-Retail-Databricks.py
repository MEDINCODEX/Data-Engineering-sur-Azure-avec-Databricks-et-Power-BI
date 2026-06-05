# Databricks notebook source
import os
from pyspark.sql.functions import col, current_timestamp, to_date

# 1. définir le chemin d'accès aux fichiers Parquet et lire les données brutes (Bronze Layer)
current_path = os.getcwd()
df_transactions_bronze = spark.read.parquet(f"file:{current_path}/transactions.parquet")

# 2.opération de nettoyage et de transformation (Silver Transformations)
df_transactions_silver = df_transactions_bronze \
    .dropDuplicates() \
    .dropna(subset=["transaction_id", "customer_id"]) \
    .withColumn("transaction_date", to_date(col("transaction_date"))) \
    .withColumn("silver_ingestion_ts", current_timestamp())

# 3. afficher les données avant et après pour s'assurer de la qualité du nettoyage
print(f"Bronze Row Count: {df_transactions_bronze.count()}")
print(f"Silver Row Count: {df_transactions_silver.count()}")

display(df_transactions_silver)

# COMMAND ----------

import os
current_path = os.getcwd()

files_to_check = ["customers.parquet", "products.parquet", "stores.parquet", "transactions.parquet"]

print("🔍 Starting to check the content of the actual files:")
for file_name in files_to_check:
    try:
        df = spark.read.parquet(f"file:{current_path}/{file_name}")
        print(f"\n📁 File Name: {file_name}")
        print(f"✨ Columns present in the file are: {df.columns}")
    except Exception as e:
        print(f"\n❌ File {file_name} is not found in the workspace.")

# COMMAND ----------

import os
from pyspark.sql.functions import col, to_date

current_path = os.getcwd()

print("Starting Silver Layer Processing...")

# 1. nettoyage du tableau des transactions (Transactions)
df_transactions_silver = spark.read.parquet(f"file:{current_path}/transactions.parquet") \
    .dropDuplicates() \
    .dropna(subset=["transaction_id", "customer_id"]) \
    .withColumn("transaction_date", to_date(col("transaction_date")))

# 2. nettoyage du tableau des clients (Customers)
df_customers_silver = spark.read.parquet(f"file:{current_path}/customers.parquet") \
    .dropDuplicates() \
    .dropna(subset=["customer_id"])

# 3. nettoyage du tableau des produits (Products)
df_products_silver = spark.read.parquet(f"file:{current_path}/products.parquet") \
    .dropDuplicates() \
    .dropna(subset=["product_id"])

# 4. nettoyage du tableau des magasins (Stores)
df_stores_silver = spark.read.parquet(f"file:{current_path}/stores.parquet") \
    .dropDuplicates() \
    .dropna(subset=["store_id"])

print("Data cleaning completed. Saving to Silver Layer as Managed Tables...")

# 5. sauvegarde dans le Metastore en tant que tables gérées
df_transactions_silver.write.mode("overwrite").saveAsTable("silver_transactions")
df_customers_silver.write.mode("overwrite").saveAsTable("silver_customers")
df_products_silver.write.mode("overwrite").saveAsTable("silver_products")
df_stores_silver.write.mode("overwrite").saveAsTable("silver_stores")

print("Success! All tables are saved in the Silver Layer.")

# 6. afficher les tables pour s'assurer de leur présence dans la base de données
display(spark.sql("SHOW TABLES"))

# COMMAND ----------

from pyspark.sql.functions import sum, col, round

print("🚀 Starting Gold Layer Processing...")

# 1. Lecture des tables Silver nécessaires
df_transactions = spark.read.table("silver_transactions")
df_products = spark.read.table("silver_products")

# 2. Jointure pour enrichir les transactions avec les détails des produits
df_enriched = df_transactions.join(df_products, "product_id", "left")

# 3. Calcul de l'revenu: Ajout d'un nouveau colonne (l'revenu = la quantité × le prix)
df_enriched = df_enriched.withColumn("revenue", col("quantity") * col("price"))

# 4. Construction des KPI de l'or: Ventes totales et quantités vendues par catégorie de produit
df_gold_category_sales = df_enriched.groupBy("category") \
    .agg(
        round(sum("revenue"), 2).alias("total_sales"),
        sum("quantity").alias("total_units_sold")
    ).orderBy(col("total_sales").desc())

# 5. sauvegarde de cette synthèse comme table dorée finale dans le Metastore
df_gold_category_sales.write.mode("overwrite").saveAsTable("gold_category_sales")

print("✅ Success! Gold Layer table is ready for Data Visualization.")

# 6. afficher la résultat final (ce que verrait le directeur de l'entreprise)
display(df_gold_category_sales)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- requête financière simple pour connaître les catégories les plus vendues
# MAGIC SELECT category, total_sales, total_units_sold 
# MAGIC FROM gold_category_sales
# MAGIC ORDER BY total_sales DESC;

# COMMAND ----------

from pyspark.sql.functions import col

# 1. Lecture des tables Silver nécessaires
df_trans = spark.read.table("silver_transactions")
df_prod = spark.read.table("silver_products")

# 2. Jointure pour enrichir les transactions avec les détails des produits
df_gold_full = df_trans.join(df_prod, "product_id", "left") \
    .withColumn("revenue", col("quantity") * col("price")) \
    .select(
        col("transaction_id"),
        col("transaction_date"),
        col("product_name"),
        col("category"),
        col("quantity"),
        col("revenue")
    )

# 3. Sauvegarde dans le Metastore
df_gold_full.write.mode("overwrite").saveAsTable("gold_sales_analytics")

# 4. Affichage pour l'export
display(df_gold_full)