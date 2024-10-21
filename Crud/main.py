import psycopg2
import pandas as pd
from flask import Flask, request, jsonify
import csv


app = Flask(__name__) 
 
def load_data(filename):
    myList = []
    with open(filename) as items:
        data = csv.reader(items, delimiter=',')
        next(data)
        for row in data:
            add_data_in_table(row)
           # myList.append(row)
        return myList

def add_data_in_table(row):
    print('--->>>', row[1])
    qInsert =""" INSERT INTO  movies ( name, type, description_1, description_2, description_3, description_4, description_5, description_6, description_7, description_8, description_9, description_10, created_year) VALUES
                   (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
    """
    cursor.execute( qInsert, (row[1], row[2],row[3], row[3],row[3], row[3], row[3],row[3],row[3],row[3],row[3], row[3],row[4]) )

@app.route("/getData")
def getData():
    open_connection()
    cursor.execute(""" SELECT * FROM movies""")
    resp =  cursor.fetchall()
    close_connection()
    return resp


@app.route("/test")
def test():
    open_connection()
    create_table()
    url = "https://raw.githubusercontent.com/amirtds/kaggle-netflix-tv-shows-and-movies/main/titles.csv"
    new_list = load_data('convertcsv.csv')
    close_connection()
    return "test"

def open_connection():
    #connect to DB and create a table
    global conn
    conn =  psycopg2.connect(host="localhost", dbname="electric", user="postgres", password="password", port=54321)
    global cursor 
    cursor = conn.cursor()

def close_connection():
    conn.commit()
    cursor.close()
    conn.close()

def create_table():
    cursor.execute(""" CREATE TABLE IF NOT EXISTS movies (
               id SERIAL PRIMARY KEY,
               name VARCHAR,
               type VARCHAR,
               description_1 VARCHAR,
               description_2 VARCHAR,
               description_3 VARCHAR,
               description_4 VARCHAR,
               description_5 VARCHAR,
               description_6 VARCHAR,
               description_7 VARCHAR,
               description_8 VARCHAR,
               description_9 VARCHAR,
               description_10 VARCHAR,
               created_year VARCHAR
               );
    """)


if __name__ == "__main__":
    app.run(debug=True)
    