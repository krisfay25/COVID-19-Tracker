from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def test():
    #Establish parameters for connection to database
    config = {
    'user': '', # USE YOUR USERNAME, NEVER PUSH THIS
    'password': '', # USE YOUR PASSWORD, NEVER PUSH THIS
    'host': 'localhost',
    'port': 3306,
    'database': 'RI_DATA',
    'raise_on_warnings': True                    
    }

    #Establish connection to database
    db_connection = mysql.connector.connect(**config)

    #Establishes a cursor
    cur = db_connection.cursor()
    
    query = "SELECT * FROM Municipality"
        
    # Execute query and commit to database
    cur.execute(query)
    result = cur.fetchall()
    print("result:")
    print(result)
    #db_connection.commit()
    
    # Closes database connection and closes cursor
    cur.close()
    db_connection.close()

test()