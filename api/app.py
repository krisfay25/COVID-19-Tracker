from flask import Flask, json, jsonify, g
from flask_cors import CORS
import mysql.connector

# Initialize flask app
app = Flask(__name__)
CORS(app)

# Establish parameters for connection to database
config = {
    'user': '', # USE YOUR USERNAME, NEVER PUSH THIS
    'password': '', # USE YOUR PASSWORD, NEVER PUSH THIS
    'host': 'localhost',
    'port': 3306,
    'database': 'RI_DATA',
    'raise_on_warnings': True                     
}

# The columns of each table
county_headers = ['fips', 'state_id', 'county_name', 'total_cases', 'total_hospital', 'total_deaths', 'total_vaccinated', 'case_rate_per_100k', 'hospital_rate_per_100k', 'death_rate_per_100k', 'vaccinated_rate_per_100k', 'last_updated_timestamp']
monthly_headers = {
    'monthly_cases': ['fips', 'infection_month', 'infection_year', 'num_cases', 'rate_cases', 'last_updated'],
    'monthly_deaths': ['fips', 'death_month', 'death_year', 'num_deaths', 'rate_deaths', 'last_updated'],
    'monthly_vax_nums': ['fips', 'vaxxed_month', 'vaxxed_year', 'num_vaxxed', 'rate_vaxxed', 'last_updated'],
    'monthly_hospital': ['fips', 'hospit_month', 'hospit_year', 'num_hospit', 'rate_hospit', 'last_updated']
}
# the columns to return for the all monthly data query
# the query is very particular so we are not generating it in python
all_monthly_headers = ['fips', 'infection_month', 'infection_year', 'num_cases', 'rate_cases', 'num_deaths', 'rate_deaths', 'num_hospit', 'rate_hospit', 'num_vaxxed', 'rate_vaxxed']

# Connect to the database when needed
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(**config)
    return db

# Close database after request
@app.teardown_request
def close_database(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# A stat for all counties, in a list
# example: /all/county_name
@app.route('/all/<stat>', methods=['GET'])
def all_data(stat):
    # error if the stat is not found
    if stat not in county_headers and stat != 'geo_json_data':
        return f'Stat {stat} not in database', 400

    cur = get_db().cursor()

    # geo json must be parsed and returned as a list
    if stat == 'geo_json_data':
        cur.execute(f'SELECT geo_json_data FROM Counties')
        results = cur.fetchall()
        features = [json.loads(result[0]) for result in results]
        cur.close()
        return jsonify(features)

    # get the data for all counties
    cur.execute(f'SELECT fips, {stat} FROM Counties')
    result = cur.fetchall()

    # change the format to list of dictionaries instead of tuples
    dictionary = [{ "fips": entry[0], "value": entry[1] } for entry in result]

    cur.close()

    return jsonify(dictionary)

# Stats for a county keyed by stat
# example: /county/44001
@app.route('/county/<fips>', methods=['GET'])
def county_main_data(fips):
    cur = get_db().cursor()

    cur.execute(f'SELECT {",".join(county_headers)} FROM Counties WHERE fips={fips}')
    result = cur.fetchall()

    # error if the fips code returned nothing
    if not result:
        cur.close()
        return f'County with fips code {fips} not in database', 400

    # zip the headers with each stat, to make the headers the keys
    dictionary = dict(zip(county_headers, result[0]))

    cur.close()

    return jsonify(dictionary)

# Monthly data for a county from a table (cases, deaths, hospital, vax_nums)
# example: /county/44001/monthly/cases
@app.route('/county/<fips>/monthly/<table>', methods=['GET'])
def county_monthly_data(fips, table):
    # error if there's no monthly table for that stat
    headers = monthly_headers.get(f'monthly_{table}')
    if not headers:
        return f'Table {table} does not exist', 400
    
    cur = get_db().cursor()

    # get the data from the specified table for the county
    cur.execute(f'SELECT {",".join(headers)} FROM Monthly_{table} WHERE fips="{fips}"')
    result = cur.fetchall()

    # error if the fips code returned nothing
    if not result:
        cur.close()
        return f'County with fips code {fips} not in database', 400

    # zip the headers with each month, to make the headers the keys
    dictionary = [dict(zip(headers, month)) for month in result]

    cur.close()

    return jsonify(dictionary)

# All monthly data for a county
# example: /county/44001/monthly
@app.route('/county/<fips>/monthly', methods=['GET'])
def county_all_monthly_data(fips):
    cur = get_db().cursor()

    headers = all_monthly_headers

    # get the data from all tables for the county
    cur.execute(f'''
SELECT Monthly_cases.fips AS "fips", infection_month AS "Month", infection_year AS "Year", num_cases, rate_cases, num_deaths, rate_deaths, num_hospit, rate_hospit, num_vaxxed, rate_vaxxed,  

Monthly_cases.last_updated AS "Case/Hospit/Deaths Last Updated", Monthly_Vax_Nums.last_updated AS "Vax Last Updated" 

FROM Monthly_Cases 

INNER JOIN Monthly_Deaths

	ON Monthly_Cases.fips = Monthly_Deaths.fips AND Monthly_Cases.infection_month = Monthly_Deaths.death_month AND Monthly_Cases.infection_year = Monthly_Deaths.death_year

INNER JOIN Monthly_Hospital

	ON Monthly_Deaths.fips = Monthly_Hospital.fips AND Monthly_Deaths.death_month = Monthly_Hospital.hospit_month AND Monthly_Deaths.death_year = Monthly_Hospital.hospit_year 

LEFT JOIN Monthly_Vax_Nums 

	ON Monthly_Vax_Nums.fips = Monthly_Hospital.fips AND Monthly_Vax_Nums.vaxxed_month = Monthly_Hospital.hospit_month AND Monthly_Vax_Nums.vaxxed_year = Monthly_Hospital.hospit_year

    WHERE Monthly_cases.fips = 44001
    ''')
    result = cur.fetchall()

    # error if the fips code returned nothing
    if not result:
        cur.close()
        return f'County with fips code {fips} not in database', 400

    # zip the headers with each month, to make the headers the keys
    dictionary = [dict(zip(headers, month)) for month in result]

    cur.close()

    return jsonify(dictionary)
