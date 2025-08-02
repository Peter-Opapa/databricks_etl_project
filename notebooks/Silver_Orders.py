# Databricks notebook source
# MAGIC %md
# MAGIC ### **Data Reading**

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

df=spark.table("databricks_etl.bronze.orders_raw")

# COMMAND ----------

display(df)

# COMMAND ----------

df=df.drop("_rescued_data")
df.display()

# COMMAND ----------

df=df.withColumn("order_date",to_timestamp(col("order_date")))
df.display()


# COMMAND ----------

df=df.withColumn("Year", year(col("order_date")))
df.display()

# COMMAND ----------

df1=df.withColumn("flag",expr("dense_rank() over (partition by Year order by total_amount desc)")).withColumn("rank_flag",expr("rank() over (partition by Year order by total_amount desc)")).withColumn("row_number",expr("row_number() over (partition by Year order by total_amount desc)"))
df1.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Object Oriented Programming: Class**

# COMMAND ----------

class windows:
    def dense_rank(self,df):
        df_dense_rank=df.withColumn("dense_rank",expr("dense_rank() over (partition by Year order by total_amount desc)")) 
        return df_dense_rank
    def rank(self,df):
        df_rank=df.withColumn("rank",expr("rank() over (partition by Year order by total_amount desc)")) 
        return df_rank
    def row_number(self,df):
        df_row_number=df.withColumn("row_number",expr("row_number() over (partition by Year order by total_amount desc)")) 
        return df_row_number
 

# COMMAND ----------

win = windows()

df1 = win.dense_rank(df)
df2 = win.rank(df1)
df3 = win.row_number(df2)
df3.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Data Writing**

# COMMAND ----------

df.write.mode("overwrite").format("delta").saveAsTable("databricks_etl.silver.orders")

