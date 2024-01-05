# Notes from Week 3

## Data Warehouse and BigQuery

### OLAP vs OLTP

* ***OLTP***: Online Transaction Processing. It is used to control and run essential business operations in real time. These are typically normalized databases for efficiency, and are generally small if historical data is backed up.
* ***OLAP***: Online Analytical Processing. Used to plan, solve problems, support decisions and discover hidden insights. They are typically demoralized for analysis. They are generally large due to aggregating large data. Lost data can usually be retrived from OLTP databases.

Basically OLTP systems are "classic databases" for running bussiness (_Transactions_) whereas OLAP systems are for data analytics, and data science purposes.


|   | OLTP | OLAP |
|---|---|---|
| Data updates | Short, fast updates initiated by user | Data periodically refreshed with scheduled, long-running batch jobs |
| Database design | Normalized databases for efficiency | Denormalized databases for analysis |
| Space requirements | Generally small if historical data is archived | Generally large due to aggregating large datasets |
| Backup and recovery | Regular backups required to ensure business continuity and meet legal and governance requirements | Lost data can be reloaded from OLTP database as needed in lieu of regular backups |
| Productivity | Increases productivity of end users | Increases productivity of business managers, data analysts and executives |
| Data view | Lists day-to-day business transactions | Multi-dimensional view of enterprise data |
| User examples | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts and executives |

### So.. What is a Data Warehouse?

It is an _OLAP_ that is used for reporting, data analysis and data science _(yes, it is an OLAP used for OLAP stuff ._.)_ But so is a Data Mart and a Data Lake (_gotcha!_)

This is how to differentiate between each: A _data warehouse_ stores data in a structured format. It is a central repository of preprocessed data for analytics and business intelligence. A _data mart_ is a data warehouse that serves the needs of a specific business unit, like a company’s finance, marketing, or sales department. Finally, a _data lake_ is a central repository for raw data and unstructured data. You can store data first and process it later on. 

Another point is that Data Warehouse commonly uses ETL and Data Lake is commonly using ELT. Data Marts can be then further created from Data Warehouses for a specific department or use-case.

### BigQuery Time!

BigQuery (BQ) is a Data Warehouse solution offered by Google Cloud Platform (GCP).

- BQ is serverless. Servers or database software is managed by Google and it's transparent.
- BQ is scalable and has high availability. Google takes care of the underlying software and infrastructure.
- BQ has cool features like Machine Learning, Geospatial Analysis and Business Intelligence.
- BQ maximizes flexibility by separating data analysis and storage in different compute engines, allowing the customers to budget accordingly and reduce costs.

BigQuery is to GCP as AWS Redshift is to AWS or Azure Synapse Analytics is to Microsoft Azure.

Basically only pay for what you use and it is super fast. 

> Note: BigQuery stores data in a columnar storage format which is optimized for analytical queries, and storage is replicated across multiple locations for high availability.

Data processing has a [2-tier pricing model](https://cloud.google.com/bigquery/pricing#analysis_pricing_models):
*  On demand pricing (default): US$5 per TB per month; the first TB of the month is free.
*  Flat rate pricing: based on the number of pre-requested _slots_ (virtual CPUs).
   *  A minimum of 100 slots is required for the flat-rate pricing which costs US$2,000 per month.
   *  Queries take up slots. If you're running multiple queries and run out of slots, the additional queries must wait until other queries finish in order to free up the slot. On demand pricing does not have this issue.
   *  The flat-rate pricing only makes sense when processing more than 400TB of data per month.

### Working with BQ

BigQuery has internal and external tables. Internal tabels are normal tables. 

An _external table_ is a table that acts like a standard BQ table. The table metadata is stored in BQ but the data itself is external. BigQuery supports a few [_external data sources_](https://cloud.google.com/bigquery/external-data-sources): you may query these sources directly from BigQuery even though the data itself isn't stored in BQ.

Creating an external table
```sql
CREATE OR REPLACE EXTERNAL TABLE `silent-oasis-338916.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_silent-oasis-338916/raw/yellow_tripdata_2019-*.parquet', 'gs://dtc_data_lake_silent-oasis-338916/raw/yellow_tripdata_2020-*.parquet ']
);
```
here `gs://` is google storage, then the bucket and then the folder/file. 




