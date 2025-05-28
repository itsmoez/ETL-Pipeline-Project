import json
from utils import s3_utils
import logging
from utils.ETL import *


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def lambda_handler(event, context):

    file_path = "NOT_SET"

    LOGGER.info("lambda_handler: starting")

    try:

        LOGGER.info("lambda_handler: s3.get_file_info: starting")
        bucket_name, file_path = s3_utils.get_file_info(event)

        LOGGER.info(
            f"lambda_handler: event: file={file_path}, bucket_name={bucket_name}"
        )

        LOGGER.info(
            f"lambda_handler: s3.load_file: loading file_name={file_path} from bucket_name={bucket_name}"
        )

        body_text = s3_utils.load_file(bucket_name, file_path)

        raw_data = extract(body_text)

        branches, transactions, products, transaction_items = transform(raw_data)

        #function to create tables 

        load(branches, transactions, products, transaction_items)



        response_json = {
        'message':  print("ETL Complete") #prints the extracted and transformed data from the csv. 
        }
        return {
            'statusCode': 200,
            'body': json.dumps(response_json)
        }
        
    except Exception as err:
        LOGGER.error(f"lambda_handler: failure: error={err}, file={file_path}")
        raise err