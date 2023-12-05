#Cleaned up version of data-loading.ipynb
import argparse, os
from time import time
import pandas as pd 
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    tb = params.tb
    url = params.url
    
    # Get the name of the file from url
    paraquet_name = url.rsplit('/', 1)[-1].strip()
    
    # Download file from url
    os.system(f'curl {url.strip()} -o {paraquet_name}')
    print('\n')

    # Create SQL engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Read file
    file = pq.ParquetFile(paraquet_name)
    df = file.read().to_pandas()

    # Create the table
    df.head(0).to_sql(name=tb, con=engine, if_exists='replace')


    # Insert values
    t_start = time()
    count = 0
    for batch in file.iter_batches(batch_size=100000):
        count+=1
        batch_df = batch.to_pandas()
        print(f'inserting batch {count}...')
        b_start = time()
        
        batch_df.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time()
        print(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')
        
    t_end = time()   
    print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    



if __name__ == '__main__':
    #Parsing arguments 
    parser = argparse.ArgumentParser(description='Loading data from .paraquet file link to a Postgres datebase.')

    parser.add_argument('--user', help='Username for Postgres.')
    parser.add_argument('--password', help='Password to the username for Postgres.')
    parser.add_argument('--host', help='Hostname for Postgres.')
    parser.add_argument('--port', help='Port for Postgres connection.')
    parser.add_argument('--db', help='Databse name for Postgres')
    parser.add_argument('--tb', help='Destination table name for Postgres.')
    parser.add_argument('--url', help='URL for .paraquet file.')

    args = parser.parse_args()
    main(args)




