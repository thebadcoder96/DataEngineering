
# Some notes from Week 1
To run docker Postgres:
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/data_postgres:/var/lib/postgresql/data \
    -p 5432:5432
    postgres:13
```


### To use pgcli
Make sure to pip install psycopg-binary if you have any porblems. 
```pgcli -h localhost -p 5432 -u root -d ny_taxi```




### Downloading data
```curl``` for Mac and ```wget``` for Linux/AWS
- Link to data: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Data Dictionary: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

```curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet -o yellow_tripdata_2023-09.parquet```

### Working with paraquet files
Simple way to convert to pandas df:
```
import pyarrow.parquet as pq
table = pq.read_table('data.parquet')
df = table.to_pandas()
```
Geting the metadata for paraquet file
```metadata = pq.read_metadata('data.parquet')```

Reading the file, reading the table from file and checking schema:
```
file = pq.ParquetFile('yellow_tripdata_2023-09.parquet')
table = file.read()
table.schema
```

Creating an iterable with a batch_size from the paraquet file:
```file.iter_batches(batch_size=100000)```


