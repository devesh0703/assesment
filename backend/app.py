from flask import Flask,jsonify
from flask import request
from flask_cors import CORS
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
CORS(app)
db_file="sqliteUserData.db"


def get_connection():
    conn=None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

@app.before_first_request
def create_connection():
    """ create a database connection to a SQLite database """
    print("CREATING NEW TABLE")
    conn = None
    try:
        conn=get_connection()
        cursor_obj = conn.cursor()
        # Drop the GEEK table if already exists.
        cursor_obj.execute("DROP TABLE IF EXISTS TRAVELDATA")
        
        # Creating table
        table = """ CREATE TABLE TRAVELDATA (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    First_Name CHAR(25) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    Country VARCHAR(50),
                    Total_traveler INT,
                    Budget REAL
                ); """
        
        cursor_obj.execute(table)
        return conn
    except Error as e:
        print(e)


@app.route("/add_travel",methods=["POST"])
def add_travel():
    data={}
    error={}
    if request.json:
        for el in request.json:
            if el['name'] == "Name" and el['value']!='':
                data['name']=el['value']
            elif el['name'] == "email" and el['value']!='':
                data['email']=el['value']
            elif el['name'] == "location" and el['value']!='':
                data['location'] = el['value']
            elif el['name'] == "total_travellers" and el['value']!='':
                data['total_travellers']=el['value']
            elif el['name'] == "price" and el['value']!='':
                data['price'] = el['value']
            else:
                error[el['name']]=f" {el['name']} is required Field it cannot be empty. "

    if not error:
        conn=get_connection()
        cursor_obj = conn.cursor()
        query=f"INSERT INTO TRAVELDATA (First_Name,Email,Country,Total_traveler,Budget) VALUES ('{data['name']}','{data['email']}','{data['location']}',{data['total_travellers']},{data['price']});"
        cursor_obj.execute(query)
        conn.commit()
        conn.close()
        return jsonify("success"),200
    else:
        return jsonify(error),400
    
@app.route("/get_travelData",methods=["GET"])
def get_data():
    print("GETTING ALL THE RECORDS")
    conn=get_connection()
    cursor_obj = conn.cursor()
    cursor_obj.execute("SELECT * FROM TRAVELDATA")
    col_name=[i[0] for i in cursor_obj.description]
    #print(col_name)
    rows = cursor_obj.fetchall()
  
    data={}
    for id,row in enumerate(rows):
        data[id]={}
        for idx,item in enumerate(row):
            data[id][col_name[idx]]=item
            
            
    return jsonify(data)

