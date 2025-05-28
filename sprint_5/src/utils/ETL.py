import csv
import logging
import uuid
from datetime import datetime
import hashlib
from utils.db_utils import *
# Logging setup for loading to DB

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


headers = ['date_time', 'branch_name', 'customer_name', 'items', 'total', 'trans_type', 'card_number']


def extract(body_text):
    LOGGER.info('extract: starting')
    Reader=csv.DictReader(body_text, fieldnames= headers ,delimiter=',')
    raw_data=[rows for rows in Reader]
    LOGGER.info(f'extract: done: rows={len(raw_data)}')
    for lines in raw_data:
        return raw_data
    
    


# Function to generate a GUID.
def generate_guid(*args):
    hash_input = '|'.join(str(arg).strip().lower() for arg in args) #Normalising our inputs 
    hash_digest = hashlib.md5(hash_input.encode()).hexdigest()
    return str(uuid.UUID(hash_digest[:32]))

def filling_missing_values(raw_data):
    LOGGER.info(f'filling_in_missing_values: starting')

    for row in raw_data:
        for key, value in row.items():
            if value == '':
                row[key] = 'N/A'
    LOGGER.info(f'filling_in_missing_values: done')
    return raw_data
    

def remove_sensitive_data(raw_data):
    LOGGER.info(f'remove_sensitive_information: processing rows={len(raw_data)}')
    for row in raw_data:
        #remove sensitive data
            del row['customer_name']
            del row['card_number']
    LOGGER.info(f'remove_sensitive_information: done, processed rows={len(raw_data)}')        
    return raw_data

def split_datetime(raw_data):
    LOGGER.info(f'split_datetime: starting')

    for row in raw_data:
        raw_date_time = row.get('date_time', '').strip()
        if raw_date_time:
            try:
                dt_obj = datetime.strptime(raw_date_time, '%d/%m/%Y %H:%M')
                row['date'] = dt_obj.date()  # datetime.date object
                row['time'] = dt_obj.time()
            except ValueError:
                row['date'] = 'n/a'
                row['time'] = 'n/a'
        else:
            row['date'] = 'n/a'
            row['time'] = 'n/a'
        # remove original combined field
        del row['date_time']
    LOGGER.info(f'split_datetime: done')
    return raw_data


# This function processes the CSV file and returns normalized tables.
def process_data(raw_data):
    # Initialize data structures representing your normalized tables.
    branches = []           # Table for branches
    transactions = []       # Table for transactions : purchases made
    products = []           # Table for unique products/items
    transaction_items = []  # Table linking transactions and products : each individual drink in each transaction

    # Lookup dictionaries to avoid duplicates.
    seen_branches = {}
    seen_products = {}

    # Open and read the CSV file.

    for row in raw_data:


        # Process the branch.
        branch_name = row['branch_name']
        if branch_name not in seen_branches:
            branch_id = generate_guid(branch_name)
            seen_branches[branch_name] = branch_id
            branches.append({
                "branch_id": branch_id,
                "branch_name": branch_name
            })
        else:
            branch_id = seen_branches[branch_name]
        # Process the transaction.
        transaction_id = generate_guid(
            branch_id, row['date'], row['time'], row['total'], row['trans_type']
        )
        # keep date and time seperate.
        transactions.append({
            "transaction_id": transaction_id,
            "branch_id": branch_id,
            "date": row['date'],
            "time": row['time'],
            "total": row['total'],
            "trans_type": row['trans_type']
        })
        # Process the order field.
        
        order_string = row['items'].title()
        # Split the order string by ", " to get a list of individual product strings.
        order_items = order_string.split(", ")

        for idx, item in enumerate(order_items):
            # Using Indexing so that if we have multiple products that are the same we can add the index to generate a unique id for it. 
            # Parse product name and price
            parts = item.rsplit(" - ", 1)  # split from the right to keep product name + flavour together
            if len(parts) != 2:
                continue
            product_name = parts[0].strip()
            try:
                price = float(parts[1].strip())
            except ValueError:
                continue
            
            product_key = product_name
            if product_key not in seen_products:
                product_id = generate_guid(product_name, price)
                seen_products[product_key] = product_id
                products.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "price": price
                })
            else:
                product_id = seen_products[product_key]

            # Generate a deterministic item_id using the index
            items_id = generate_guid(transaction_id, product_id, price, idx)

            transaction_items.append({
                "items_id": items_id,
                "transaction_id": transaction_id,
                "product_id": product_id,
                "price": price
            })
    LOGGER.info(f'Splitting_into_seperate_dictionaries: done')

    print(branches)
    print(transactions)
    print(products)
    print(transaction_items)
    return branches, transactions, products, transaction_items


def load_into_database(branches, transactions, products, transaction_items):
    


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
        LOGGER.info("All data inserted successfully.")

    except Exception as e:
        conn.rollback()
        LOGGER.error("Insert failed: %s", e)

def transform(raw_data):
    LOGGER.info('transform: starting')
    raw_data = filling_missing_values(raw_data)
    raw_data = remove_sensitive_data(raw_data)
    raw_data = split_datetime(raw_data)
    
    LOGGER.info(f'transform: done: rows={len(raw_data)}')
    return process_data(raw_data)


    