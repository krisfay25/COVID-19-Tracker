# File that cleans the .csv data files for Rhode Island COVID-19 Data and inserts rows into database table
#
# CMSC 447 Team 1 - Fall 2021

import sys
import subprocess
import pkg_resources

required = {'mysql-connector-python'} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed


if missing:
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',*missing])

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

month_to_num = {'January': 1, 'February': 2, 'March': 3,
    'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12}

num_to_months = {'1': 'January', '2': 'February', '3': "March",
'4': "April", '5': 'May', '6': 'June', '7': 'July', '8': 'August',
'9': 'September', '10': 'October', '11': 'November', '12': 'December'}

days_in_months = {'1': 31, '2': 28, '3': 31,
'4': 30, '5': 31, '6': 30, '7': 31, '8': 31,
'9': 30, '10': 31, '11': 30, '12': 31}

num_municips_in_county = {'Kent County': 5,
                         'Newport County': 6,
                         'Bristol County': 3,
                         'Providence County': 16,
                         'Washington County': 9}

# This function adds states to the "State" table
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
        
        query = f''' INSERT INTO State VALUES ({state_ids[key]}, "{key}"); '''
        
        # Execute query and commit to database
        cur.execute(query)
        db_connection.commit()
        
    
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

    last_updated_date = RI_data["Total Cases (may count people more than once)"][45]

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
        if 'County' not in col and "Last Updated" not in col:
            RI_data[col] = RI_data[col].astype('int')
    
    RI_data = RI_data.groupby(by='County', as_index=False).agg({'Total Cases (may count people more than once)':'sum',
                                     'Rate of COVID-19 cases per 100,000 population':'mean',
                                     'Total hospitalizations':'sum',
                                     'Rate of hospitalizations per 100,000 population':'mean',
                                     'Total deaths':'sum',
                                     'Rate of deaths per 100,000 population':'mean',
                                     'Total number of people who have completed primary vaccine series':'sum',
                                     'Rate of people who have completed primary vaccine series per 100,000 population':'mean'})

    RI_data['fips'] = RI_data['County'].map(rhode_island_fips)

    # Reorder the columns
    cols = RI_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    RI_data = RI_data[cols]

    RI_data["Last Updated"] = last_updated_date


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

        json_serialized = json.dumps(county_json['features'][i])
        
        query = f''' INSERT INTO Counties VALUES ("{records[i][0]}",
        {state_ids['Rhode Island']},
        "{records[i][1]}",
        %s,
        {int(records[i][2])},
        {int(records[i][3])},
        {int(records[i][4])},
        {int(records[i][5])},
        {int(records[i][6])},
        {int(records[i][7])},
        {int(records[i][8])},
        {int(records[i][9])},
        "{records[i][10]}"); '''

        # Execute query and commit to database
        cur.execute(query, (json_serialized,)) 
        
        db_connection.commit()

    # Closes database connection and closes cursor
    cur.close()
    db_connection.close()

    print("Municipality data inserted.")

# This function cleans data for the 'Monthly_cases' table
# RATE DATA
def clean_infection_rate_data():
    
    # Reads csv
    monthly_case_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Case Rates by Municipality.csv')
    
    last_updated_date = monthly_case_data["Unnamed: 1"][1]

    # Drop unnecessary rows
    monthly_case_data.drop(labels=[0, 1, 2, 3, 4, 6], axis=0, inplace=True)

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
    monthly_case_data = monthly_case_data.replace('*', 3)
    
    # Drop Municipality column
    monthly_case_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in monthly_case_data.columns:
        if 'County' not in col:
            monthly_case_data[col] = monthly_case_data[col].astype('int')

    # Group by County name
    monthly_case_data = monthly_case_data.groupby(by='County', as_index=False).mean()
    
    monthly_case_data['fips'] = monthly_case_data['County'].map(rhode_island_fips)
    
    # Reorder the columns
    cols = monthly_case_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_case_data = monthly_case_data[cols]
    
    monthly_case_data = monthly_case_data.T
    
    monthly_case_data["Last Updated"] = last_updated_date
    
    return monthly_case_data


# This function cleans data for the 'Monthly_cases' table
# NUM DATA
def clean_infection_num_data():
    
    # Reads csv
    monthly_case_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Case Trends by Municipality.csv')
    
    last_updated_date = monthly_case_data["Unnamed: 1"][1]

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
    
    monthly_case_data["Last Updated"] = last_updated_date
    
    return monthly_case_data

# This function cleans data for the 'Monthly_Vax_Nums' table
# RATE DATA
def clean_vaccination_rate_data():
    
    # Reads csv
    vax_data = pd.read_csv('COVID-19 Rhode Island Data - Municipal Vaccination Rate Trends - Complete Vax.tsv', sep='\t')
    
    last_updated_date = vax_data["Unnamed: 1"][1]

    # Drop unnecessary rows
    vax_data.drop(labels=[0, 1, 2, 3, 4, 6], axis=0, inplace=True)

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
    vax_data = vax_data.groupby(by='County', as_index=False).mean()
    
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
    
    vax_data["Last Updated"] = last_updated_date
    
    return vax_data

# This function cleans data for the 'Monthly_Vax_Nums' table
# NUM DATA
def clean_vaccination_num_data():
    
    # Reads csv
    vax_data = pd.read_csv('COVID-19 Rhode Island Data - Municipal Vaccination Trends - Complete Vax.tsv', sep='\t')
    
    last_updated_date = vax_data["Unnamed: 1"][1]

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
    vax_data = vax_data.replace('<5', 3)

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
    
    vax_data["Last Updated"] = last_updated_date
    
    return vax_data

# This function cleans data for the 'Monthly_Deaths' table
# NUM DATA
def clean_death_num_data():

    # Reads csv
    monthly_death_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Fatality Trends by Municipality.csv')
    
    last_updated_date = monthly_death_data["Unnamed: 1"][1]

    # Drop unnecessary rows
    monthly_death_data.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    monthly_death_data = monthly_death_data.T

    # Rename the columns so the dates are the column names
    monthly_death_data.columns = monthly_death_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    monthly_death_data = monthly_death_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    monthly_death_data['Month of Death'] = monthly_death_data['Month of Death'].apply(lambda x: x.title())

    monthly_death_data.rename(columns={'Month of Death': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    monthly_death_data = monthly_death_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = monthly_death_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_death_data = monthly_death_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    monthly_death_data = monthly_death_data.replace('<5', 3)

    # Drop Municipality column
    monthly_death_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in monthly_death_data.columns:
        if 'County' not in col and "Last Updated" not in col:
            monthly_death_data[col] = monthly_death_data[col].astype('int')

    # Group by County name
    monthly_death_data = monthly_death_data.groupby(by='County', as_index=False).sum()

    monthly_death_data['fips'] = monthly_death_data['County'].map(rhode_island_fips)

    # Reorder the columns
    cols = monthly_death_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_death_data = monthly_death_data[cols]

    monthly_death_data = monthly_death_data.T
    
    monthly_death_data["Last Updated"] = last_updated_date


    return monthly_death_data

# This function cleans data for the 'Monthly_Deaths' table
# RATE DATA
def clean_death_rate_data():
    
    # Reads csv
    monthly_death_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Mortality Rates by Municipality.tsv', sep='\t')
    
    last_updated_date = monthly_death_data["Unnamed: 1"][1]

    # Drop unnecessary rows
    monthly_death_data.drop(labels=[0, 1, 2, 3, 4, 6], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    monthly_death_data = monthly_death_data.T

    # Rename the columns so the dates are the column names
    monthly_death_data.columns = monthly_death_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    monthly_death_data = monthly_death_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    monthly_death_data['Month of Death'] = monthly_death_data['Month of Death'].apply(lambda x: x.title())

    monthly_death_data.rename(columns={'Month of Death': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    monthly_death_data = monthly_death_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = monthly_death_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_death_data = monthly_death_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    monthly_death_data = monthly_death_data.replace('*', 3)

    # Drop Municipality column
    monthly_death_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in monthly_death_data.columns:
        if 'County' not in col and "Last Updated" not in col:
            monthly_death_data[col] = monthly_death_data[col].astype('int')

    # Group by County name
    monthly_death_data = monthly_death_data.groupby(by='County', as_index=False).mean()

    monthly_death_data['fips'] = monthly_death_data['County'].map(rhode_island_fips)

    # Reorder the columns
    cols = monthly_death_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_death_data = monthly_death_data[cols]

    monthly_death_data = monthly_death_data.T
    
    monthly_death_data["Last Updated"] = last_updated_date


    return monthly_death_data

# This function cleans and inserts the data for the 'Monthly_Hospital' table
# NUM DATA
def clean_hospit_num_data():

    # Reads csv
    monthly_hospit_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Hospitalization Trends by Municipality.csv')
    
    last_updated_date = monthly_hospit_data["Unnamed: 1"][1]

    # Drop unnecessary rows
    monthly_hospit_data.drop(labels=[0, 1, 2, 3, 4], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    monthly_hospit_data = monthly_hospit_data.T

    # Rename the columns so the dates are the column names
    monthly_hospit_data.columns = monthly_hospit_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    monthly_hospit_data = monthly_hospit_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    monthly_hospit_data['Month of Admission'] = monthly_hospit_data['Month of Admission'].apply(lambda x: x.title())

    monthly_hospit_data.rename(columns={'Month of Admission': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    monthly_hospit_data = monthly_hospit_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = monthly_hospit_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_hospit_data = monthly_hospit_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    monthly_hospit_data = monthly_hospit_data.replace('<5', 3)

    # Drop Municipality column
    monthly_hospit_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in monthly_hospit_data.columns:
        if 'County' not in col and "Last Updated" not in col:
            monthly_hospit_data[col] = monthly_hospit_data[col].astype('int')

    # Group by County name
    monthly_hospit_data = monthly_hospit_data.groupby(by='County', as_index=False).sum()

    monthly_hospit_data['fips'] = monthly_hospit_data['County'].map(rhode_island_fips)

    # Reorder the columns
    cols = monthly_hospit_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_hospit_data = monthly_hospit_data[cols]

    monthly_hospit_data = monthly_hospit_data.T
    
    monthly_hospit_data["Last Updated"] = last_updated_date


    return monthly_hospit_data

# This function cleans and inserts the data for the 'Monthly_Hospital' table
# RATE DATA
def clean_hospit_rate_data():
    
    # Reads csv
    monthly_hospit_data = pd.read_csv('COVID-19 Rhode Island Data - Monthly Hospitalization Rates by Municipality.tsv', sep='\t')
    
    last_updated_date = monthly_hospit_data["Unnamed: 1"][1]

    # Drop unnecessary rows
    monthly_hospit_data.drop(labels=[0, 1, 2, 3, 4, 6], axis=0, inplace=True)

    # Transpose dataframe so the locations are rows, not columns
    monthly_hospit_data = monthly_hospit_data.T

    # Rename the columns so the dates are the column names
    monthly_hospit_data.columns = monthly_hospit_data.iloc[0]

    # Remove the row of data that contains dates (since they are now column names)
    monthly_hospit_data = monthly_hospit_data.iloc[1: , :]

    # Make Municipality Names In Title Case
    monthly_hospit_data['Month of Admission'] = monthly_hospit_data['Month of Admission'].apply(lambda x: x.title())

    monthly_hospit_data.rename(columns={'Month of Admission': 'Municipality of residence'}, inplace=True)

    # Creates a dataframe that only contains municipalities with their associated counties
    counties = pd.DataFrame(list(zip(counties_municipalities.rhode_island_counties, 
                                     counties_municipalities.rhode_island_municipalities)),
                            columns=['County', 'Municipality of residence'])

    # Merge dataframes 
    monthly_hospit_data = monthly_hospit_data.merge(counties, on='Municipality of residence', how='right')

    # Reorder columns
    cols = monthly_hospit_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_hospit_data = monthly_hospit_data[cols]

    # Changes values of '<5' with 3
    # Values of '<5' could be 1, 2, 3, 4, 5.  So assume the average number.
    monthly_hospit_data = monthly_hospit_data.replace('*', 3)

    # Drop Municipality column
    monthly_hospit_data.drop(columns=["Municipality of residence"], axis=1, inplace=True)

    # Convert all of the numerical columns to ints
    for col in monthly_hospit_data.columns:
        if 'County' not in col and "Last Updated" not in col:
            monthly_hospit_data[col] = monthly_hospit_data[col].astype('int')

    # Group by County name
    monthly_hospit_data = monthly_hospit_data.groupby(by='County', as_index=False).mean()

    monthly_hospit_data['fips'] = monthly_hospit_data['County'].map(rhode_island_fips)

    # Reorder the columns
    cols = monthly_hospit_data.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    monthly_hospit_data = monthly_hospit_data[cols]

    monthly_hospit_data = monthly_hospit_data.T
    
    monthly_hospit_data["Last Updated"] = last_updated_date


    return monthly_hospit_data

def main():
    add_states()
    clean_municipality_data()

    df_rate = clean_infection_rate_data()
    df_num = clean_infection_num_data()


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


    for i in range(len(df_rate.columns) - 1):
        fips = df_rate[i][0]
        for j in range(2, len(df_rate) - 1):
            month, year = df_rate.index[j].split(" ")

            query = f''' INSERT INTO Monthly_Cases VALUES ({int(fips)}, {int(month_to_num[month])}, {int(year)}, {int(df_num[i][j])}, {int(df_rate[i][j])}, %s);'''
            cur.execute(query, (str(df_rate['Last Updated'][0]), ))
            db_connection.commit()

    cur.close()
    db_connection.close()


    df_vax_rate = clean_vaccination_rate_data()
    df_vax_num = clean_vaccination_num_data()

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

    for i in range(len(df_vax_rate.columns) - 1):
            fips = df_vax_rate[i][0]
            for j in range(2, len(df_vax_rate)):
                month, year = df_vax_rate.index[j].split(" ")

                query = f''' INSERT INTO Monthly_Vax_Nums VALUES ({int(fips)}, {int(month_to_num[month])}, {int(year)}, {int(df_vax_num[i][j])}, {int(df_vax_rate[i][j])}, %s);'''
                cur.execute(query, (str(df_vax_rate['Last Updated'][0]), ))
                db_connection.commit()
    cur.close()
    db_connection.close()

    df_death_rate = clean_death_rate_data()
    df_death_num = clean_death_num_data()

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

    for i in range(len(df_death_rate.columns) - 1):
            fips = df_death_rate[i][0]
            for j in range(2, len(df_death_rate) - 1):
                month, year = df_death_rate.index[j].split(" ")

                query = f''' INSERT INTO Monthly_Deaths VALUES ({int(fips)}, {int(month_to_num[month])}, {int(year)}, {int(df_death_num[i][j])}, {int(df_death_rate[i][j])}, %s);'''
                cur.execute(query, (str(df_death_num['Last Updated'][0]), ))
                db_connection.commit()
    cur.close()
    db_connection.close()

    df_hospit_rate = clean_hospit_rate_data()
    df_hospit_num = clean_hospit_num_data()

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

    for i in range(len(df_hospit_rate.columns) - 1):
            fips = df_hospit_rate[i][0]
            for j in range(2, len(df_hospit_rate) - 1):
                month, year = df_hospit_rate.index[j].split(" ")

                query = f''' INSERT INTO Monthly_Hospital VALUES ({int(fips)}, {int(month_to_num[month])}, {int(year)}, {int(df_hospit_num[i][j])}, {int(df_hospit_rate[i][j])}, %s);'''
                cur.execute(query, (str(df_hospit_num['Last Updated'][0]), ))
                db_connection.commit()
    cur.close()
    db_connection.close()



if __name__ == "__main__":
    main()