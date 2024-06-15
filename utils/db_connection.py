import os
import mysql.connector

def connect_to_database(environment='DEV'):
    # Connect to the database
    conn = mysql.connector.connect(
            host=os.getenv(f'{environment}_DB_HOST'),
            user=os.getenv(f'{environment}_DB_USER'),
            password=os.getenv(f'{environment}_DB_PASSWORD'),
            database=os.getenv(f'{environment}_DB_DATABASE')
    )
    cursor = conn.cursor()
    return conn, cursor