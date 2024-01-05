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
CREATE OR REPLACE EXTERNAL TABLE `silent-oasis.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://dtc_data_lake_silent-oasis/raw/yellow_tripdata_2019-*.parquet']
);
```
here `gs://` is google storage, then the bucket and then the folder/file. 

### Partitioning in BQ

Partitioning is awesome if you partition by what is most likely to be queried or filtered on. It will reduce cost if you use it smartly. 

>Note: You can highlight your query and it will show an estimate of how much data will be read. This is not available in Clustering. More on that later.

Syntax:
```sql
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE silent-oasis.trips_data_all.external_yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM silent-oasis.trips_data_all.external_yellow_tripdata;
```
Partition a table by:
- _Time-unit column_: based on a `TIMESTAMP`, `DATE`, or `DATETIME` column.
- _Ingestion time_ (`_PARTITIONTIME`): based on the timestamp when BQ ingests the data.
- _Integer range_: based on an integer column.

For time columns, the partition can be daily (default), hourly, monthly or yearly.

>Note: BigQuery limits the amount of partitions to 4000 per table. Consider clustering if you want to further divide you table.

[Read more about partitions.](https://cloud.google.com/bigquery/docs/partitioned-tables)

We can also take a look into the information of the partition by:
```sql
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;
```
> Every table in BQ has `INFORMATION_SCHEMA`

### Clustering in BQ

_Clustering_ consists of arranging/sorting a table based on the values of its columns. Again clustering should depend on how you query and filter the data.
- Clustering can be done based on one or multiple columns up to ***4***.
- The order of the columns is important in order to determine the column priority.
- Clustering provides more granularity.
- ***Automatic reclustering*** as more data is inserted into the table (clustering can become weak as there can be overlapping keys), BQ will automatically re-cluster the table in the background with no cost.
- Do not use partitioning on columns with high cardinality or on columns that will change frequently and cause the partitions to be frequently recalculated.
- Clustering may improve performance and lower costs on big datasets for queries that use filter clauses and aggregate data.

>Note: tables with less than 1GB don't show significant improvement with partitioning and clustering; doing so in a small table could even lead to increased cost due to the additional metadata reads and metadata maintenance.

Clustering columns must be top-level, non-repeated columns(Categorical Values). The datatypes supported:
* `DATE`
* `DATETIME`
* `TIMESTAMP`
* `BOOL`
* `GEOGRAPHY`
* `INT64`
* `NUMERIC`
* `BIGNUMERIC`
* `STRING`

Syntax:
```sql
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```

> As mentioned above, when you highlight the query on a clustered table, the estimate stated does not take the clustered into play and is wrong.

| Clustering | Partitioning |
|---|---|
| Cost estimate unknown. BQ cannot estimate the reduction in cost before running a query. | Cost known upfront. |
| High granularity. Multiple criteria can be used to sort the table. | Low granularity. Only a single column can be used to partition the table. You need partition-level management |
| Clusters are "fixed in place". | Partitions can be added, deleted, modified or even moved between storage options. |
| Queries that commonly filters or aggregation against multiple particular columns. | Filter or aggregate on a single column. |
| The cardinality of the number of values in a column or group of columns is large. | Limited to 4000 partitions; cannot be used in columns with larger cardinality. |

### When to choose Clustering over Partitioning?

- Partitioning results in a small amount of data per partition (approximately < 1 GB).
- Partitioning results in a large number of partitions beyond the limits on partitioned tables (> 4000 partitions).
- Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (for example, writing to the table every few minutes or every hour which makes the partitions change and writing to most of the partitions each time rather than just a handful).

### How to get the best out of BQ

Here's a list of [best practices for BigQuery](https://cloud.google.com/bigquery/docs/best-practices-performance-overview):

* Cost reduction
  * Avoid `SELECT *` . Reducing the amount of columns to display will drastically reduce the amount of processed data and lower costs.
  * Price your queries before running them. Price can be seen in the top right.
  * Use clustered and/or partitioned tables if possible.
  * Use [streaming inserts](https://cloud.google.com/bigquery/streaming-data-into-bigquery) with caution. They can easily hike up the cost.
  * [Materialize query results](https://cloud.google.com/bigquery/docs/materialized-views-intro) and CTE's in different stages.

* Query performance
  * Filter on partitioned columns.
  * [Denormalize data](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-explained-working-joins-nested-repeated-data).
  * Use [nested or repeated columns](https://cloud.google.com/blog/topics/developers-practitioners/bigquery-explained-working-joins-nested-repeated-data).
  * Use external data sources appropiately. Constantly reading data from a bucket may incur in additional costs and has worse performance. Don't use external tables if high performance is critical.
  * Reduce data before using a `JOIN`.
  * Do not threat `WITH` clauses as [prepared statements](https://www.wikiwand.com/en/Prepared_statement).
  * Avoid [oversharding tables](https://cloud.google.com/bigquery/docs/partitioned-tables#dt_partition_shard).
  * Avoid JavaScript user-defined functions.
  * Use [approximate aggregation functions](https://cloud.google.com/bigquery/docs/reference/standard-sql/approximate_aggregate_functions) rather than complete ones such as [HyperLogLog++](https://cloud.google.com/bigquery/docs/reference/standard-sql/hll_functions).
  * Order statements should be the last part of the query.
  * [Optimize join patterns](https://cloud.google.com/bigquery/docs/best-practices-performance-compute#optimize_your_join_patterns).
  * Place the table with the _largest_ number of rows first, followed by the table with the _fewest_ rows, and then place the remaining tables by decreasing size.
    * This is due to how BigQuery works internally: the first table will be distributed evenly and the second table will be broadcasted to all the nodes. Check the [Internals section](#internals) for more details.

    
