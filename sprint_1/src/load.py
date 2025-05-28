import logging
from db_utils import *

# Logging setup for loading to DB
insert_logger = logging.getLogger('db_insert')
insert_handler = logging.FileHandler('db_insert.log')
insert_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
insert_handler.setFormatter(insert_formatter)
insert_logger.addHandler(insert_handler)
insert_logger.setLevel(logging.INFO)

# Load environment variables from .env file

conn,cursor=db_connection() #opening the connection to the database and return conn short for connection anf cursor for further use. 



def load_into_database(branches, transactions, products, transaction_items):
    # Convert dicts to tuples
    branch_values = [(d["branch_id"], d["branch_name"]) for d in branches]

    transaction_values = [
        (t["transaction_id"], t["branch_id"], t["date"], t["time"], t["total"], t["transaction_type"])
        for t in transactions
    ]

    product_values = [
        (p["product_id"], p["drink_type"], p["flavour"], p["price"])
        for p in products
    ]

    item_values = [
        (i["transaction_id"], i["product_id"], i["quantity"], i["price"])
        for i in transaction_items
    ]

    try:
        branch_query = '''
        INSERT INTO branches (branch_id, branch_name)
        VALUES (%s, %s)
        ON CONFLICT (branch_id) DO NOTHING;
        '''
        cursor.executemany(branch_query, branch_values)

        transaction_query = '''
        INSERT INTO transactions (transaction_id, branch_id, date, time, total, transaction_type)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO NOTHING;
        '''
        cursor.executemany(transaction_query, transaction_values)


        items_query = '''
        INSERT INTO transaction_items (transaction_id, product_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (transaction_id, product_id) DO NOTHING;
        '''
        cursor.executemany(items_query, item_values)

        conn.commit()
        insert_logger.info("All data inserted successfully.")

    except Exception as e:
        conn.rollback()
        insert_logger.error("Insert failed: %s", e)
    
    
    

