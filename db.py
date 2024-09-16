# app/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="Image_processing",
        user="postgres",
        password="ayushi@0987",
        port = "5000"
    )
    return conn
