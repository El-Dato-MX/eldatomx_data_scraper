import os
import mysql.connector

def connect_to_database():
    # Connect to the database
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )
    cursor = conn.cursor()
    return conn, cursor