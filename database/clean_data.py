# File that cleans the .csv data files for Rhode Island COVID-19 Data and inserts rows into database table
#
# CMSC 447 Team 1 - Fall 2021
#
# NOT FINISHED DO NOT DOWNLOAD


import pandas as pd
import counties_municipalities
import mysql.connector
from datetime import datetime
import json

rhode_island_fips = {"Kent County": 44003,
                    "Newport County": 44005,
                    "Bristol County": 44001,
                    "Providence County": 44007,
                    "Washington County": 44009}

state_ids = {"Rhode Island": 44}

# Thid function adds states to the "State" table
def add_states():
    
    #Establish parameters for connection to database
    config = {
    'user': 'placeholder', # USE YOUR USERNAME, NEVER PUSH THIS
    'password': 'placeholder', # USE YOUR PASSWORD, NEVER PUSH THIS
    'host': 'localhost',
    'port': 3306,
    'database': 'RI_DATA',
    'raise_on_warnings': True                    
    }
    
    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()
        
    # Inserts each row into table in database
    for key in state_ids:
        
        #print("start: " + str(i))
        
        #print(json.dumps(county_json['features'][i]))
        
        query = f''' INSERT INTO State VALUES ({state_ids[key]}, "{key}"); '''
        
        # Execute query and commit to database
        cur.execute(query)
        db_connection.commit()
        
        #print("end: " + str(i))
    
    # Closes database connection and closes cursor
    cur.close()
    db_connection.close()
    
    print("States data inserted.")

# This function cleans and inserts the data for the 'Counties' table
def clean_municipality_data():
    county_json = {}
    
    with open('RI_counties_geo.json') as f:
        county_json = json.load(f)


    # Reads csv
    RI_data = pd.read_csv('COVID-19 Rhode Island Data - Municipality.csv')

    # Deletes the rows that do not correspond to a municipality
    RI_data.drop(labels=[39, 40, 41, 42, 43, 44, 45], axis=0, inplace=True)

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    RI_data = RI_data.replace('<5', 3)

    # Changes values of '--' with 0
    RI_data = RI_data.replace('--', 0)  

    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                    counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    RI_data = RI_data.merge(counties, on='Municipality of residence', how='right')
    
    # Reorder the columns
    cols = RI_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    RI_data = RI_data[cols]

    # Drop Municipality column
    RI_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in RI_data.columns:
        if 'County' not in col:
            #print("ok")
            RI_data[col] = RI_data[col].astype('int')

    # Group by County name
    RI_data = RI_data.groupby(by='County', as_index=False).sum()
    
    RI_data['fips'] = RI_data['County'].map(rhode_island_fips)
    
    # Reorder the columns
    cols = RI_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    RI_data = RI_data[cols]

    #Establish parameters for connection to database
    config = {
    'user': 'placeholder', # USE YOUR USERNAME, NEVER PUSH THIS
    'password': 'placeholder', # USE YOUR PASSWORD, NEVER PUSH THIS
    'host': 'localhost',
    'port': 3306,
    'database': 'RI_DATA',
    'raise_on_warnings': True                    
    }
    
    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()

    result = RI_data.to_json()
    RI_json = json.loads(result)

    counter = 0
    num_rows = 0

    # Gets number of rows
    for row in RI_json:
        num_rows = len(RI_json[row])
        break
        
    records = []

    # Turns json dictionary into 2-dimensional list of rows
    for i in range(num_rows):
        curr_row = []
        for row in RI_json:
            curr_row.append(RI_json[row].get(str(i)))
            
        records.append(curr_row)
        
    # Inserts each row into table in database
    for i in range(len(records)):
        
        query = f''' INSERT INTO Counties VALUES ("{records[i][0]}",
        {state_ids['Rhode Island']},
        "{records[i][1]}",
        "{str(county_json['features'][i])}",
        {int(records[i][2])},
        {int(records[i][3])},
        {int(records[i][4])},
        {int(records[i][5])},
        {int(records[i][6])},
        {int(records[i][7])},
        {int(records[i][8])},
        {int(records[i][9])}); '''
        
        # Execute query and commit to database
        cur.execute(query)
        db_connection.commit()
    
    # Closes database connection and closes cursor
    cur.close()
    db_connection.close()

    print("Municipality data inserted.")



    # Reads csv
    RI_data = pd.read_csv('COVID-19 Rhode Island Data - Municipality.csv')

    # Deletes the rows that do not correspond to a municipality
    RI_data.drop(labels=[39, 40, 41, 42, 43, 44, 45], axis=0, inplace=True)

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    RI_data = RI_data.replace('<5', 3)

    # Changes values of '--' with 0
    RI_data = RI_data.replace('--', 0)  

    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                    counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    RI_data = RI_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder the columns
    cols = RI_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    RI_data = RI_data[cols]

    #Establish parameters for connection to database
    config = {
    'user': 'placeholder', # USE YOUR USERNAME, NEVER PUSH THIS
    'password': 'placeholder', # USE YOUR PASSWORD, NEVER PUSH THIS
    'host': 'localhost',
    'port': 3306,
    'database': 'RI_DATA',
    'raise_on_warnings': True                    
    }

    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()

    result = RI_data.to_json()
    RI_json = json.loads(result)

    counter = 0
    num_rows = 0

    # Gets number of rows
    for row in RI_json:
        num_rows = len(RI_json[row])
        break
        
    records = []

    # Turns json dictionary into 2-dimensional list of rows
    for i in range(num_rows):
        curr_row = []
        for row in RI_json:
            curr_row.append(RI_json[row].get(str(i)))
            
        records.append(curr_row)
        
    # Inserts each row into table in database
    for i in range(len(records)):
        query = f''' INSERT INTO Municipality VALUES ("{records[i][0]}",
        "{records[i][1]}",
        {int(records[i][2])},
        {int(records[i][3])},
        {int(records[i][4])},
        {int(records[i][5])},
        {int(records[i][6])},
        {int(records[i][7])},
        {int(records[i][8])},
        {int(records[i][9])}); '''
        
        # Execute query and commit to database
        cur.execute(query)
        db_connection.commit()
    
    # Closes database connection and closes cursor
    cur.close()
    db_connection.close()

    print("Municipality data inserted.")

# This function cleans and inserts the data for the 'Monthly_cases' table
def clean_infection_rate_data():
    
    # Reads csv
    monthly_case_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Case Trends by Municipality.csv')

    # Drop unnecessary rows
    monthly_case_data.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    monthly_case_data = monthly_case_data.T

    # Rename the columns so the dates are the column names
    monthly_case_data.columns = monthly_case_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    monthly_case_data = monthly_case_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    monthly_case_data['Month of Result Date'] = monthly_case_data['Month of Result Date'].apply(lambda x: x.title())

    monthly_case_data.rename(columns={'Month of Result Date': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    monthly_case_data = monthly_case_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = monthly_case_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_case_data = monthly_case_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    monthly_case_data = monthly_case_data.replace('<5', 3)
    
    # Drop Municipality column
    monthly_case_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in monthly_case_data.columns:
        if 'County' not in col:
            monthly_case_data[col] = monthly_case_data[col].astype('int')

    # Group by County name
    monthly_case_data = monthly_case_data.groupby(by='County', as_index=False).sum()
    
    monthly_case_data['fips'] = monthly_case_data['County'].map(rhode_island_fips)
    
    # Reorder the columns
    cols = monthly_case_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_case_data = monthly_case_data[cols]
    
    monthly_case_data = monthly_case_data.T

    #---------------------------------------------------------------------------------------------------------------------------
    #Establish parameters for connection to database
    config = {
       'user': 'placeholder', # USE YOUR USERNAME, NEVER PUSH THIS
       'password': 'placeholder', # USE YOUR PASSWORD, NEVER PUSH THIS
       'host': 'localhost',
       'port': 3306,
       'database': 'RI_DATA',
       'raise_on_warnings': True                    
    }

    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()


    for i in range(len(monthly_case_data.columns)):
        fips = monthly_case_data[i][0]
        for j in range(2, len(monthly_case_data) - 1):
            month, year = monthly_case_data.index[j].split(" ")
            #print(monthly_case_data[i][j])

            query = f''' INSERT INTO Monthly_Cases VALUES ({int(fips)}, {int(month_to_num[month])}, {int(year)}, {int(monthly_case_data[i][j])});'''
            cur.execute(query)
            db_connection.commit()

    cur.close()
    db_connection.close()
    
    print("Monthly_Cases data inserted.")



    
    # Reads csv
    monthly_case_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Case Trends by Municipality.csv')

    # Drop unnecessary rows
    monthly_case_data.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    monthly_case_data = monthly_case_data.T

    # Rename the columns so the dates are the column names
    monthly_case_data.columns = monthly_case_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    monthly_case_data = monthly_case_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    monthly_case_data['Month of Result Date'] = monthly_case_data['Month of Result Date'].apply(lambda x: x.title())

    monthly_case_data.rename(columns={'Month of Result Date': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    monthly_case_data = monthly_case_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = monthly_case_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_case_data = monthly_case_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    monthly_case_data = monthly_case_data.replace('<5', 3)

    #Establish parameters for connection to database
    config = {
       'user': 'placeholder', # USE YOUR USERNAME, NEVER PUSH THIS
       'password': 'placeholder', # USE YOUR PASSWORD, NEVER PUSH THIS
       'host': 'localhost',
       'port': 3306,
       'database': 'RI_DATA',
       'raise_on_warnings': True                    
    }

    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()

    result = monthly_case_data.to_json()
    monthly_case_json = json.loads(result)

    counter = 0
    num_rows = 0

    # Gets number of rows
    for row in monthly_case_json:
        num_rows = len(monthly_case_json[row])
        break

    records = []

    # Turns json dictionary into 2-dimensional list of rows
    for i in range(num_rows):
        curr_row = []
        for row in monthly_case_json:
            curr_row.append(monthly_case_json[row].get(str(i)))

        records.append(curr_row)


    # Inserts each row into table in database
    for i in range(len(records)):

        query = f''' INSERT INTO Monthly_Cases VALUES ("{records[i][0]}",
        "{records[i][1]}",
        {int(records[i][2])}, {int(records[i][3])}, {int(records[i][4])},
        {int(records[i][5])}, {int(records[i][6])}, {int(records[i][7])},
        {int(records[i][8])}, {int(records[i][9])}, {int(records[i][10])},
        {int(records[i][11])}, {int(records[i][12])}, {int(records[i][13])},
        {int(records[i][14])}, {int(records[i][15])}, {int(records[i][16])},
        {int(records[i][17])}, {int(records[i][18])}, {int(records[i][19])},
        {int(records[i][20])}, {int(records[i][21])}); '''

        cur.execute(query)
        db_connection.commit()


    cur.close()
    db_connection.close()
    
    print("Monthly_Cases data inserted.")

# This function cleans and inserts the data for the 'Monthly_Vax_Nums' table
def clean_vaccination_data():
    
    # Reads csv
    vax_data = pd.read_csv('COVID-19 Rhode Island Data - Municipal Vaccination Rate Trends - Full Vax.tsv', sep='\t')

    # Drop unnecessary rows
    vax_data.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    vax_data = vax_data.T

    # Rename the columns so the dates are the column names
    vax_data.columns = vax_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    vax_data = vax_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    vax_data['Week Vaccination Completed'] = vax_data['Week Vaccination Completed'].apply(lambda x: x.title())

    vax_data.rename(columns={'Week Vaccination Completed': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])
    
    # Merge dataframes 
    vax_data = vax_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = vax_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    vax_data = vax_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    vax_data = vax_data.replace('*', 3)

    vax_data = vax_data.replace(',','', regex=True)
        
    # Drop Municipality column
    vax_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in vax_data.columns:
        if 'County' not in col:
            vax_data[col] = vax_data[col].astype('int')

    # Group by County name
    vax_data = vax_data.groupby(by='County', as_index=False).sum()
    
    vax_data['fips'] = vax_data['County'].map(rhode_island_fips)
    
    # Reorder the columns
    cols = vax_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    vax_data = vax_data[cols]

    vax_cols = list(vax_data.columns)

    for col in vax_cols:

        separated_data = pd.DataFrame()

        if '-' in col:

            # Split the dates of the current column
            date1_str, date2_str = col.split('-')

            # Turn the dates from string to date objects
            date1 = datetime.strptime(date1_str, '%m/%d/%y').date()
            date2 = datetime.strptime(date2_str, '%m/%d/%y').date()

            # If the two months match, simply change the name of the column
            if date1.month == date2.month:
                new_col_name = num_to_months[str(date1.month)] + " " + str(date1.year) 
                vax_data = vax_data.rename(columns={col: new_col_name})

            # If the two months do not match, give an equal ratio of the number to each month based on the amount of days
            # that the month has in the week (e.g., 12/27/20 - 1/2/21, December gets ~5/7-ths of total, 
            #                                       January gets ~2/7-ths of total)
            else:
                num_days_in_week = 7

                # Figure out how many days are in each month in the column
                days_in_month1 = days_in_months[str(date1.month)] - date1.day + 1
                days_in_month2 = num_days_in_week - days_in_month1

                # Create columns names to be added to data
                new_col_name1 = num_to_months[str(date1.month)] + " " + str(date1.year) 
                new_col_name2 = num_to_months[str(date2.month)] + " " + str(date2.year) 
    
                separated_data[new_col_name1] = []
                separated_data[new_col_name2] = []

                # Fill in each row with the correct ratio of total into both columns
                for row in vax_data[col]:
                    month1_ratio = (days_in_month1 / num_days_in_week) * int(row)
                    month2_ratio = (days_in_month2 / num_days_in_week) * int(row)

                    to_append = [round(month1_ratio), round(month2_ratio)]
                    data_len = len(separated_data)
                    separated_data.loc[data_len] = to_append

                # Concatenate new dataframe with original data dataframe
                vax_data = pd.concat([vax_data, separated_data], axis=1)

                # Drop the original dataframe's column of the week with the combined month,
                # since the original dataframe now has the separated months
                vax_data = vax_data.drop(col, axis=1)

    # Sum the duplicate columns, so each column is unique and represents an individual
    # month of the year
    vax_data = vax_data.sum(axis=1, level=0)

    vax_data = vax_data.T

    #Establish parameters for connection to database
    config = {
        'user': 'placeholder', # USE YOUR USERNAME, NEVER PUSH THIS
        'password': 'placeholder', # USE YOUR PASSWORD, NEVER PUSH THIS
        'host': 'localhost',
        'port': 3306,
        'database': 'RI_DATA',
        'raise_on_warnings': True                    
    }

    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()

    for i in range(len(vax_data.columns)):
            fips = vax_data[i][0]
            for j in range(3, len(vax_data)):
                month, year = vax_data.index[j].split(" ")

                query = f''' INSERT INTO Monthly_Vax_Nums VALUES ({int(fips)}, {int(month_to_num[month])}, {int(year)}, {int(vax_data[i][j])});'''
                cur.execute(query)
                db_connection.commit()
    cur.close()
    db_connection.close()

    print("Monthly_Vax_Nums data inserted.")

def main():
    add_states()
    clean_municipality_data()
    clean_infection_rate_data()
    clean_vaccination_data()



if __name__ == "__main__":
    main()