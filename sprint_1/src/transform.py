import csv
import uuid

# Function to generate a GUID.
def generate_guid():
    return str(uuid.uuid4())

# This function processes the CSV file and returns normalized tables.
def transform(file_path):
    # Initialize data structures representing your normalized tables.
    branches = []           # Table for branches
    transactions = []       # Table for transactions : purchases made
    products = []           # Table for unique products/items
    transaction_items = []  # Table linking transactions and products : each individual drink in each transaction

    # Lookup dictionaries to avoid duplicates.
    seen_branches = {}
    seen_products = {}

    # Open and read the CSV file.
    with open(file_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Process the branch.
            branch_name = row['branch_name']
            if branch_name not in seen_branches:
                branch_id = generate_guid()
                seen_branches[branch_name] = branch_id
                branches.append({
                    "branch_id": branch_id,
                    "branch_name": branch_name
                })
            else:
                branch_id = seen_branches[branch_name]

            # Process the transaction.
            transaction_id = generate_guid()
            # Combine date and time into a single datetime string.
            transactions.append({
                "transaction_id": transaction_id,
                "branch_id": branch_id,
                "datetime": f"{row['date']} {row['time']}",
                "total": row["total"],
                "trans_type": row["trans_type"]
            })

            # Process the order field.
            order_string = row["order"]
            # Split the order string by ", " to get a list of individual product strings.
            order_items = order_string.split(", ")
            for item in order_items:
                # Split each product string using " - " as the delimiter.
                parts = item.split(" - ")

                # Extract the details. Assume two formats:
                # Format with flavor: "Drink Type - Flavor - Price" → 3 parts.
                # Format without flavor: "Drink Type - Price" → 2 parts.
                if len(parts) == 3:
                    drink_type = parts[0].strip()
                    flavour = parts[1].strip()
                    try:
                        price = float(parts[2].strip())
                    except ValueError:
                        # Skip this product if the price can’t be parsed.
                        continue
                elif len(parts) == 2:
                    drink_type = parts[0].strip()
                    flavour = None
                    try:
                        price = float(parts[1].strip())
                    except ValueError:
                        continue
                else:
                    # Skip if the format doesn't match what we expect.
                    continue

                # Use a unique key for the product based on drink type and flavour.
                product_key = f"{drink_type}_{flavour}"
                if product_key not in seen_products:
                    product_id = generate_guid()
                    seen_products[product_key] = product_id
                    products.append({
                        "product_id": product_id,
                        "drink_type": drink_type,
                        "flavour": flavour,
                        "price": price  # Price stored here is assumed to be the product price.
                    })
                else:
                    product_id = seen_products[product_key]

                # Link the product to the current transaction.
                transaction_items.append({
                    "transaction_id": transaction_id,
                    "product_id": product_id,
                    "price": price
                })
                
    return branches, transactions, products, transaction_items

# Main execution to process the file.
if __name__ == "__main__":
    file_path = "C:/Users/MohammedA(DE-LON16)/Documents/generations-sessions/week_8_sprint/Formatted Clean Data/formatted_leeds_no_names.csv"
    branches, transactions, products, transaction_items = transform(file_path)


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
# Transactions table =  TRANSACT_ID:         BRANCH_ID             DATETIME          TOTAL            TRANS_TYPE
# Trans_items table=    transaction_id     product_id'             price
# Products table =      product_id         drink_type               flavour           price
# Branches table =      branch_id          branch_name
