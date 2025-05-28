from db_utils import *
from extract import extract_func
from transform import transform
from load import load_into_database


raw_data = extract_func(r"C:\Users\GuledM(DE-LON16)\Documents\Group-Project\brews_brothers_DELON16\sprint_2\data\leeds_09-05-2023_09-00-00_done.csv")
branches, transactions, products, transaction_items = transform(raw_data)

# print(branches)
# print(transactions)
# print(products)
# print(transaction_items)


load_into_database(branches, transactions, products, transaction_items)

