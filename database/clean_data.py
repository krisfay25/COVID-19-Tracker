# File that cleans the .csv data files for Rhode Island COVID-19 Data and inserts rows into database table
#
# CMSC 447 Team 1 - Fall 2021
#
# NOT FINISHED DO NOT DOWNLOAD


import pandas as pd
import counties_municipalities
import mysql.connector

# This function cleans and inserts the data for the 'Municipality' table
def clean_municipality_data():

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



def main():
    clean_municipality_data()
    clean_infection_rate_data()



if __name__ == "__main__":
    main()