
# Notes from Week 1
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
- Note: Ctrl+C for stop running the docker database. 


### To use pgcli
Make sure to pip install pgcli and psycopg-binary if you have any porblems.

```pgcli -h localhost -p 5432 -u root -d ny_taxi```

- Note: Ctrl+D for exiting pcli 


### Downloading data
```curl``` for Mac and ```wget``` for Linux/AWS
- Link to data: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Data Dictionary: https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

```curl https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet -o yellow_tripdata_2023-09.parquet```

### Working with paraquet files
- Simple way to convert to pandas df:
```
import pyarrow.parquet as pq
table = pq.read_table('data.parquet')
df = table.to_pandas()
```
- Geting the metadata for paraquet file

```metadata = pq.read_metadata('data.parquet')```

- Reading the file, reading the table from file and checking schema:
```
file = pq.ParquetFile('yellow_tripdata_2023-09.parquet')
table = file.read()
table.schema
```

- Creating an iterable with a batch_size from the paraquet file:

```file.iter_batches(batch_size=100000)```

### Using pgAdmin 
Using pgAdmin to connect to the database is better since the UI for querying is much clean when compared to pgcli (in terminal or cmd)

Of course we will use Docker to run pgAdmin but the problem is that the database is in a seperate container. To connect both containers we can put them in the same *network*. To do that first we have to create a network and then run both the containers again; but now we add them both in our network. 

- Creating a network in docker:
```
docker network create <networkname>
```

Now we stop the docker postgres and then run it again within the network. We should name the docker image so we can connect to it suing the name.
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/data_postgres:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13

```

To run pgAdmin:
```
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="mishal@mazin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root"  \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
```

- pgAdmin will be accessible at ```localhost:8080``` in your browser.



