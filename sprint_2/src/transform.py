import csv
import uuid
import hashlib
from datetime import datetime

# Function to generate a GUID.
def generate_guid(*args):
    hash_input = '|'.join(str(arg).strip().lower() for arg in args) #Normalising our inputs 
    hash_digest = hashlib.md5(hash_input.encode()).hexdigest()
    return str(uuid.UUID(hash_digest[:32]))

def filling_missing_values(raw_data):

    for row in raw_data:
        for key, value in row.items():
            if value == '':
                row[key] = 'N/A'
    return raw_data
    

def remove_sensitive_data(raw_data):
    for row in raw_data:
        #remove sensitive data
            del row['customer_name']
            del row['card_number']
    return raw_data

def split_datetime(raw_data):

    for row in raw_data:
        raw_date_time = row.get('date_time', '').strip()
        if raw_date_time:
            try:
                # Attempt to parse with expected UK format: DD/MM/YYYY HH:MM
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

    return branches, transactions, products, transaction_items

def transform(raw_data):
    raw_data = filling_missing_values(raw_data)
    raw_data = remove_sensitive_data(raw_data)
    raw_data = split_datetime(raw_data)

    return process_data(raw_data)

# For the file paths, you must change the \ to / in the file path.   
#    "C:/Users/MohammedA(DE-LON16)/Documents/generations-sessions/week_8_sprint/Formatted Clean Data/formatted_data_chesterfield_no_names.csv"
#    "C:/Users/MohammedA(DE-LON16)/Documents/generations-sessions/week_8_sprint/Formatted Clean Data/formatted_data_uppingham_no_names.csv"


    # Print out some summary information.
#    print("Branches table count:", len(branches))
#    print("Transactions table count:", len(transactions)) #- basically counts how many orders, should line up with winstons clean csv
#    print("Products table count:", len(products))
#    print("Transaction Items table count:", len(transaction_items))

#print(products)

# What the tables look like
# Transactions table =  TRANSACT_ID:       BRANCH_ID             DATE              TIME          TOTAL            TRANS_TYPE
# Trans_items table=    ITEM_ID            transaction_id        product_id'       price
# Products table =      product_id         product_name          price
# Branches table =      branch_id          branch_name
