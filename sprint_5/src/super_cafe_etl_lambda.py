import json
from utils import s3_utils, sql_utils, db_utils
from utils import s3_utils
import logging
from utils.ETL import *
import os

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SSM_ENV_VAR_NAME = 'SSM_PARAMETER_NAME'


def lambda_handler(event, context):

    file_path = "NOT_SET"

    LOGGER.info("lambda_handler: starting")

    try:
        ssm_param_name = os.environ.get(SSM_ENV_VAR_NAME, 'NOT_SET')
        LOGGER.info(f'lambda_handler: ssm_param_name={ssm_param_name} from ssm_env_var_name={SSM_ENV_VAR_NAME}')

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

        LOGGER.warning(f'lambda_handler: transformed_data={branches, transactions, products, transaction_items}')

        redshift_details = db_utils.get_ssm_param(ssm_param_name)
        conn, cur = db_utils.open_sql_database_connection_and_cursor(redshift_details)

        sql_utils.create_db_tables(conn, cur)
        load_into_database(branches, transactions, products, transaction_items)
        cur.close()
        conn.close()

        LOGGER.info(f'lambda_handler: done, file={file_path}')

    except Exception as err:
        LOGGER.error(f'lambda_handler: failure: error={err}, file={file_path}')
        raise err