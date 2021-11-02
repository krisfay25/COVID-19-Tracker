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
counties_headers = ['fips', 'state_id', 'county_name', 'total_cases', 'total_hospital', 'total_deaths', 'total_vaccinated', 'last_updated_timestamp']
monthly_case_headers = ['fips', 'infection_month', 'infection_year', 'num_cases', 'rate_cases']
monthly_vax_headers = ['fips', 'vaxxed_month', 'vaxxed_year', 'num_vaxxed', 'rate_vaxxed']

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

# Stats keyed by county fips
@app.route('/all/<stat>', methods=['GET'])
def all_data(stat):
    # error if the stat is not found
    if stat not in counties_headers and stat != 'geo_json_data':
        return f'Stat {stat} not in database', 400

    cur = get_db().cursor()

    # special case for geo json as the json must be parsed and returned in a list format
    if stat == 'geo_json_data':
        cur.execute(f'SELECT geo_json_data FROM Counties')
        results = cur.fetchall()
        features = [json.loads(result[0]) for result in results]
        cur.close()
        return jsonify(features)

    # get the data for all counties
    cur.execute(f'SELECT fips, {stat} FROM Counties')
    result = cur.fetchall()

    # change the format to dictionary instead of tuples to be jsonified
    dictionary = [{ "fips": entry[0], "value": entry[1] } for entry in result]

    cur.close()

    return jsonify(dictionary)

# Stats for a county keyed by stat
@app.route('/county/<fips>', methods=['GET'])
def county_data(fips):
    cur = get_db().cursor()

    cur.execute(f'SELECT {",".join(counties_headers)} FROM Counties WHERE fips={fips}')
    result = cur.fetchall()

    # error if the fips code returned nothing
    if not result:
        cur.close()
        return f'County with fips code {fips} not in database', 400

    # zip the headers with each stat, to make the headers the keys
    dictionary = dict(zip(counties_headers, result[0]))

    cur.close()

    return jsonify(dictionary)

# Cases for a county in a list (monthly)
@app.route('/county/<fips>/cases', methods=['GET'])
def county_cases(fips):
    cur = get_db().cursor()

    # get all stats for the county
    cur.execute(f'SELECT {",".join(monthly_case_headers)} FROM Monthly_Cases WHERE fips="{fips}"')
    result = cur.fetchall()

    # error if the fips code returned nothing
    if not result:
        cur.close()
        return f'County with fips code {fips} not in database', 400

    # zip the headers with each month, to make the headers the keys
    dictionary = [dict(zip(monthly_case_headers, month)) for month in result]

    cur.close()

    return jsonify(dictionary)

# Vax data for a county in a list (monthly)
@app.route('/county/<fips>/vaccination', methods=['GET'])
def county_vax(fips):
    cur = get_db().cursor()

    # get all stats for the county
    cur.execute(f'SELECT {",".join(monthly_vax_headers)} FROM Monthly_Vax_Nums WHERE fips="{fips}"')
    result = cur.fetchall()

    # error if the fips code returned nothing
    if not result:
        cur.close()
        return f'County with fips code {fips} not in database', 400

    # zip the headers with each month, to make the headers the keys
    dictionary = [dict(zip(monthly_vax_headers, month)) for month in result]

    cur.close()

    return jsonify(dictionary)
