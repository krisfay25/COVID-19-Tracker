# File that cleans the .csv data files for Rhode Island COVID-19 Data and inserts rows into database table
#
# CMSC 447 Team 1 - Fall 2021
#
# NOT FINISHED DO NOT DOWNLOAD


import pandas as pd
import counties_municipalities
import mysql.connector

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



def main():

    # Cleans the .csv and inserts records into the Municipality table
    clean_municipality_data()



if __name__ == "__main__":
    main()