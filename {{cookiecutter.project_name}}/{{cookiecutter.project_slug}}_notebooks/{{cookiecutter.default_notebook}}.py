# Databricks notebook source
# MAGIC %run ../{{cookiecutter.project_slug}}_notebooks/Code1

# COMMAND ----------

# MAGIC %run ../{{cookiecutter.project_slug}}_notebooks/Code2

# COMMAND ----------

generate_data1()
display(spark.sql("select * from my_cool_data"))
