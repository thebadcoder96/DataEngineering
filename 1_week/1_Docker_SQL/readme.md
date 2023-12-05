
# Notes from Week 1

## Docker and SQL
- To check what containers are running: ```docker ps```.
- To kill running containers: ```docker kill <containername>```.
- To remove containers: ```docker rm <containername>```.
- To list docker images ```docker images```.
- To remove docker images ```docker rmi <name>:<tag>```.

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
- Link to data page: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Link to download dataset used here: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet 
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

## Dockerize Everything

We can dockerize everything mentioned above to be able to run in one line of code. First, we need to convert our jupyter notebook to a proper python script. 

To convert notebook to .py file:
```
jupyter nbconvert --to=script <notebook.ipynb>
```

### Clean .py file

Use ```argparse``` to add arguements that can be run from command line/terminal. 

```
parser = argparse.ArgumentParser(description='This will show in help.')
parser.add_argument('--user', help='description')
parser.add_argument('--pass', help='description')
args = parser.parse_args()
```
- Note: It is not a good idea to create take in any ```password``` related arguments since terminal/cmd keeps a history for what you typed and it was be leaked very easily. It is better to use environment variables or something else to keep your passwords protected.

Rest of the cleaning can be found in the ```data-loading.py``` file.

### Command Line code to run file
This code for my MacOS terminal, which is why I am using ```python3``` and ```curl```.
```
python3 data-loading.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --tb=yellow_taxi_data \
    --url=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet \
```

After updating the Docker file, build the docker image and run it. 
- Build Docker image:

```docker build -t <imagename>:<versionname>  <path of docker file>```

- Run Docker image with the arguments. Make sure to run it in the same network as the docker postgres so we can connect to it.
```
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet"

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --tb=yellow_taxi_data \
    --url=${URL} \
```
Note: The parameters after the docker image name are the arguments for the python file and the parameters before are the parameters for the docker image to run. 

### Docker Compose

This allows for multiple container to run together. Create a ```.yaml``` file which stores the configurations of the docker containers needed. 