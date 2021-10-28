from flask import Flask, jsonify, g
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
def county_data(stat):
    # get the data for all counties
    cur = get_db().cursor()
    cur.execute(f'SELECT fips, {stat} FROM counties')
    result = cur.fetchall()

    # change the format to dictionary instead of tuples
    dictionary = dict(result)

    cur.close()

    return jsonify(dictionary)
