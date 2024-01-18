## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".
>HINT: ```docker run --help```

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

>Ans: `--rm` 

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 
>HINT: ```docker run -it --entrypoint bash python:3.9```
```pip list``` in the bash.

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0
>Ans: `0.42.0`

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)
>Hint: `docker-compose up` to build the postgres and pgadmin. 
`docker network ls` to find the network or you can check the first few lines of the previous code.
`docker build -t dataload:0.1 .` build docker image from our code.
  
  ```bash
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

    docker run -it \
        --network=1_docker_sql_default \
        taxidata-load:0.1.0 \
        --user=root \
        --password=root \
        --host=pgdatabase \
        --port=5432 \
        --db=ny_taxi \
        --tb=green_taxi \
        --url=${URL} \
  ```
the above to insert the green taxi trips and the same with `url` and `db` change for zones

## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

```sql
    SELECT COUNT(*) FROM green_taxi 
    WHERE CAST(lpep_pickup_datetime as DATE) = '2019-09-18'
    AND CAST(lpep_dropoff_datetime as DATE) = '2019-09-18';
  ```

- 15767
- 15612
- 15859
- 89009
>Ans: `15612`

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

```sql
SELECT trip_distance, lpep_pickup_datetime FROM green_taxi
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi);
```

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21
>Ans: `2019-09-26` 

## Question 5. The number of passengers

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 ```sql
SELECT puz."Borough", SUM(total_amount) AmountSum
FROM green_taxi gt
INNER JOIN zones puz ON gt."PULocationID" = puz."LocationID"
INNER JOIN zones doz ON gt."DOLocationID" = doz."LocationID"
WHERE CAST(gt."lpep_pickup_datetime" as DATE) = '2019-09-18'
GROUP BY puz."Borough" 
HAVING SUM(total_amount) > 50000;
```

- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"
>Ans: `"Brooklyn" "Manhattan" "Queens"`

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```sql
SELECT puz."Zone", doz."Zone", tip_amount
FROM green_taxi gt
INNER JOIN zones puz ON gt."PULocationID" = puz."LocationID"
LEFT JOIN zones doz ON gt."DOLocationID" = doz."LocationID"
WHERE puz."Zone" = 'Astoria'
ORDER BY 3 DESC 
LIMIT 1;
```

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza
>Ans: `JFK Airport`

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: 
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET