import csv

headers = ['date_time', 'branch_name', 'customer_name', 'items', 'total', 'trans_type', 'card_number']
    
def extract_func(file_path):
    with open(file_path,'r') as file:
        Reader=csv.DictReader(file,headers, delimiter=',') # Adding column names and changing delimiter to ','
        raw_data=[rows for rows in Reader]
        for lines in raw_data:
            # print(lines)
            return raw_data
    

