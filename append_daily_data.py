import pandas as pd
import numpy as np
import json
from datetime import date
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os
import warnings
from datetime import datetime, timedelta
import sys
import shutil

destination_directory = r'Z:\Cylinders Analytics\Akshit-Data Source\Raw Sievert JSON Files'

warnings.filterwarnings("ignore")

def first_time_push_to_snowflake():
    user = 'ATAYADE'
    password = 'Worthington$123'
    account = 'eab42642.us-east-1'
    database = 'EDP_NP'
    warehouse = 'DEFAULT_WH'
    schema = 'RAW_SIEVERT'
    conn = None

    try:
        with snowflake.connector.connect(
                user = user,
                password = password,
                account = account,
                database = database,
                warehouse = warehouse,
                schema = schema) as conn:
            
            with conn.cursor() as cur:

                create_script = ''' CREATE TABLE IF NOT EXISTS DAILY_SIEVERT_DATA(
                                    Date                 string,
                                    Store_Num               int, 
                                    Morning              float,                
                                    Evening              float
                                    )
                                '''

                cur.execute(create_script)

    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def get_morning_combined():

    morning = []

    morn_part_1 = f'Morning/brickseek_temp_json_morning_homedepot_{datetime.now().date()-timedelta(days=1)}_part1'
    morn_part_2 = f'Morning/brickseek_temp_json_morning_homedepot_{datetime.now().date()-timedelta(days=1)}_part2'
    print(morn_part_1)

    for each_json in os.listdir(morn_part_1):
        if each_json == 'already_scraped.json':
            pass

        else:
            data = json.load(open(os.path.join(morn_part_1, each_json)))
            morning.append(data[0])
  
    for each_json in os.listdir(morn_part_2):
        if each_json == 'already_scraped.json':
            pass

        else:
            data = json.load(open(os.path.join(morn_part_2, each_json)))
            morning.append(data[0])

    return(morning)

def get_night_combined():

    night = []

    night_part_1 = f'Night/brickseek_temp_json_night_homedepot_{datetime.now().date()-timedelta(days=1)}_part1'
    night_part_2 = f'Night/brickseek_temp_json_night_homedepot_{datetime.now().date()-timedelta(days=1)}_part2'
    print(night_part_1)

    for each_json in os.listdir(night_part_1):
        if each_json == 'already_scraped.json':
            pass

        else:
            data = json.load(open(os.path.join(night_part_1, each_json)))
            night.append(data[0])
  
    for each_json in os.listdir(night_part_2):
        if each_json == 'already_scraped.json':
            pass

        else:
            data = json.load(open(os.path.join(night_part_2, each_json)))
            night.append(data[0])

    return(night)

def combineAll():
    morning = get_morning_combined()
    night = get_night_combined()

    # Create DataFrames from the NumPy arrays
    df1 = pd.DataFrame(morning, columns=['Key', 'Value1'])
    df2 = pd.DataFrame(night, columns=['Key', 'Value2'])

    # Merge the DataFrames on the common column 'Key'
    df = pd.merge(df1, df2, on='Key', how='outer')
    df.columns = ['Store_Num', 'Morning', 'Evening']
    df = df.drop_duplicates()
    df.insert(0, 'Date', datetime.now().date()-timedelta(days=1))

    return(df)

def existing_data():
    df = pd.read_excel('sievert_daily_data.xlsx')

    return(df)

def append_new_data():

    old_df = existing_data()
    new_df = combineAll()

    pushTodatabase(new_df)

    updated_df = pd.concat([old_df, new_df])
    updated_df.drop('Unnamed: 0', axis=1, inplace=True)
    # print(updated_df)

    # updated_df.to_excel("Z:/Cylinders Analytics/Akshit-Data Source/sievert_daily_data.xlsx")
    updated_df.to_excel("sievert_daily_data.xlsx")

def pushTodatabase(dataframe):

    df = dataframe

    # df.replace(['$14', '$14.97'], None, inplace=True)
    # df['Morning'] = pd.to_numeric(df['Morning'])
    # df['Evening'] = pd.to_numeric(df['Evening'])
    # # df['Date'] = 
    # df['Date'] = pd.to_datetime(df['Date'])
    df.columns = map(lambda x: str(x).upper(), df.columns)
    
    user = 'ATAYADE'
    password = 'Worthington$123'
    account = 'eab42642.us-east-1'
    database = 'EDP_NP'
    warehouse = 'DEFAULT_WH'
    schema = 'RAW_SIEVERT'
    conn = None

    try:
        with snowflake.connector.connect(
                user = user,
                password = password,
                account = account,
                database = database,
                warehouse = warehouse,
                schema = schema) as conn:
            
            with conn.cursor() as cur:

                print("Dataframe Created, Pushing into Snowflake")

                # Write the data from the DataFrame to the table named "customers".
                success, nchunks, nrows, _ = write_pandas(conn, df, table_name='DAILY_SIEVERT_DATA') 
                print(f"{nrows} - {success}")

                    
    except Exception as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

def moveAllFiles():
    morn_part_1 = f'Morning/brickseek_temp_json_morning_homedepot_{datetime.now().date()-timedelta(days=1)}_part1'
    morn_part_2 = f'Morning/brickseek_temp_json_morning_homedepot_{datetime.now().date()-timedelta(days=1)}_part2'
    night_part_1 = f'Night/brickseek_temp_json_night_homedepot_{datetime.now().date()-timedelta(days=1)}_part1'
    night_part_2 = f'Night/brickseek_temp_json_night_homedepot_{datetime.now().date()-timedelta(days=1)}_part2'

    shutil.rmtree(morn_part_1)
    shutil.rmtree(morn_part_2)
    shutil.rmtree(night_part_1)
    shutil.rmtree(night_part_2)

if __name__ == "__main__":

    append_new_data()

    print("Deleting files")
    moveAllFiles()

    print("Succesfull")

