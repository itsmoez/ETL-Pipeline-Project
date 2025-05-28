import boto3
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

s3_client = boto3.client('s3')



def get_file_info(event):
    LOGGER.info('get_file_info: starting') #first log to identify start if function
    first_record = event['Records'][0] #retrieves the event details
    bucket_name = first_record['s3']['bucket']['name'] #retrieves bucket that had been updated 
    file_name = first_record['s3']['object']['key'] #retrieves the file_name that has been added

    LOGGER.info(f'get_file_info: file={file_name}, bucket_name={bucket_name}') #adding log with the details of the file and bucket
    return bucket_name, file_name #return file name and bucket name for future use



def load_file(bucket_name, s3_key):
    LOGGER.info(f'load_file: loading s3_key={s3_key} from bucket_name={bucket_name}') #log to identify next step in process
    response = s3_client.get_object(Bucket=bucket_name, Key=s3_key) #retriving our files metadata and actual content
    body_text = response['Body'].read().decode('utf-8').split('\n') #from the metadata we retrieve the actual content specifically

    body_text = [line.strip() for line in body_text]


    LOGGER.info(f'load_file: done: s3_key={s3_key} result_chars={len(body_text)}') #logging the function has worked and how many rows we have 
    return body_text
