import psycopg2 as psycopg
import os
from dotenv import load_dotenv
import logging

# Logging setup for DB connection 
connection_logger = logging.getLogger('db_connection') #log name
connection_handler = logging.FileHandler('db_connection.log') #where to store the log which is a file called db_connection.log
connection_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') #how to format of each log. i.e timestamp of log message, what the issue was and our message.
connection_handler.setFormatter(connection_formatter) #sets the format for each log message, timestamp, issue and our written message.
connection_logger.addHandler(connection_handler) #telling it where to store the logs.
connection_logger.setLevel(logging.INFO) #what thinggs to log under info.



load_dotenv()
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
        connection_logger.info("Connected to database successfully.") #logging successful connections 
        cursor=conn.cursor()
        print("Cursor opened...")
        connection_logger.info("Cursor to database opened successfully.") #logging successful connections 
        return conn,cursor

    except Exception as ex:
        print('Failed to:', ex)
        connection_logger.error("Database connection failed: %s", ex) #logging unsuccessful connections
        raise


def close_db_connection(cursor, conn):
    if cursor:
        cursor.close()
    print("Cursor closed.")
    connection_logger.info("Connection to database closed successfully.")
    if conn:
        conn.close()
    print("Database connection closed.")
    connection_logger.info("Cursor to database closed successfully.") #logging successful connections 

