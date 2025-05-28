import psycopg2 as psycopg
import os
from dotenv import load_dotenv
import logging

# Logging setup for DB connection 
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

load_dotenv(dotenv_path=r"C:\Users\GuledM(DE-LON16)\Documents\Group-Project\brews_brothers_DELON16\sprint_2\docker\.env") #link path to .env
host_name = os.environ.get("POSTGRES_HOST")
port = os.environ.get("PORT")
database_name = os.environ.get("POSTGRES_DB")
user_name = os.environ.get("POSTGRES_USER")
user_password = os.environ.get("POSTGRES_PASSWORD")

def db_connection():
    print('Opening connection...')
    try: #tries to connect and if it fails it returns an error message which is logged. 
        conn=psycopg.connect(f"""
            host={host_name}
            port={port}
            dbname={database_name}
            user={user_name}
            password={user_password}
            """)
        print("Connection established!")
        LOGGER.info("Connected to database successfully.") #logging successful connections 
        cursor=conn.cursor()
        print("Cursor opened...")
        LOGGER.info("Cursor to database opened successfully.") #logging successful connections 
        cursor.execute("SET datestyle = 'ISO, DMY';")
        LOGGER.info("Date set to DD/MM/YYYY")
        return conn,cursor

    except Exception as ex:
        print('Failed to:', ex)
        LOGGER.error("Database connection failed: %s", ex) #logging unsuccessful connections
        raise


def close_db_connection(cursor, conn):
    if cursor:
        cursor.close()
    print("Cursor closed.")
    LOGGER.info("Connection to database closed successfully.")
    if conn:
        conn.close()
    print("Database connection closed.")
    LOGGER.error("Cursor to database closed successfully.") #logging successful connections 

