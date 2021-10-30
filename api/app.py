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
    cur = get_db().cursor()

    # special case for geo json as the json must be parsed and returned in a list format
    if stat == 'geo_json_data':
        cur.execute(f'SELECT geo_json_data FROM counties')
        results = cur.fetchall()
        features = [json.loads(result[0]) for result in results]
        cur.close()
        return jsonify(features)

    # get the data for all counties
    cur.execute(f'SELECT fips, {stat} FROM counties')
    result = cur.fetchall()

    # change the format to dictionary instead of tuples
    dictionary = dict(result)

    cur.close()

    return jsonify(dictionary)

# Stats for a county keyed by stat
@app.route('/county/<fips>/cases', methods=['GET'])
def county_data(fips):
    cur = get_db().cursor()

    # get column headers
    cur.execute(f'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA="RI_DATA" AND TABLE_NAME="Monthly_cases"')
    result = cur.fetchall()
    headers = [name[0] for name in result]

    # get all stats for the county
    cur.execute(f'SELECT * FROM Monthly_cases WHERE fips="{fips}"')
    result = cur.fetchall()

    # zip the headers with each month, to make the headers the keys
    dictionary = [dict(zip(headers, month)) for month in result]

    cur.close()

    return jsonify(dictionary)
