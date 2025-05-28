import logging
from db_utils import *

# Logging setup for loading to DB
insert_logger = logging.getLogger('db_insert')
insert_handler = logging.FileHandler(r'C:\Users\GuledM(DE-LON16)\Documents\Group-Project\brews_brothers_DELON16\sprint_2\notes\db_insert.log')
insert_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
insert_handler.setFormatter(insert_formatter)
insert_logger.addHandler(insert_handler)
insert_logger.setLevel(logging.INFO)

# Load environment variables from .env file

conn,cursor=db_connection() #opening the connection to the database and return conn short for connection anf cursor for further use. 

def create_tables(sql_script_file_path): #prefix file path with r
    try:
        with open(sql_script_file_path, 'r') as sql_file:
            sql = sql_file.read()
            cursor.execute(sql)
            conn.commit()
            print("Tables created successfully.")
            insert_logger.info("All data tables created successfully.")
    except Exception as e:
        conn.rollback()
        insert_logger.error("Table creation failed: %s", e)
        return

def load_into_database(branches, transactions, products, transaction_items):
    
    # Create the tables before entering our transformed data.

    create_tables(r"C:\Users\GuledM(DE-LON16)\Documents\Group-Project\brews_brothers_DELON16\sprint_2\docker\v.2-SQL-script.sql")

    try:

        # Preparing our data for batch insertion
        branch_values = [(d["branch_id"], d["branch_name"]) for d in branches]

        transaction_values = [
            (t["transaction_id"], t["branch_id"], t["date"], t["time"], t["total"], t["trans_type"])
            for t in transactions
        ]

        product_values = [
            (p["product_id"], p["product_name"], p["price"])
            for p in products
        ]

        item_values = [
            (i["items_id"], i["transaction_id"], i["product_id"], i["price"])
            for i in transaction_items
        ]


        branch_query = '''
        INSERT INTO branches (branch_id, branch_name)
        VALUES (%s, %s)
        ON CONFLICT (branch_id) DO NOTHING;
        '''
        cursor.executemany(branch_query, branch_values)

        transaction_query = '''
        INSERT INTO transactions (transaction_id, branch_id, date, time, total, trans_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO NOTHING;
        '''
        cursor.executemany(transaction_query, transaction_values)

        product_query = '''
        INSERT INTO products (product_id, product_name, price)
        VALUES (%s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING;
        '''
        cursor.executemany(product_query, product_values)

        items_query = '''
        INSERT INTO transaction_items (items_id, transaction_id, product_id, price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (items_id) DO NOTHING;
        '''
        cursor.executemany(items_query, item_values)

        conn.commit()
        insert_logger.info("All data inserted successfully.")

    except Exception as e:
        conn.rollback()
        insert_logger.error("Insert failed: %s", e)
    
    
    
    
    
    

