import boto3
import csv
from datetime import datetime

def lambda_handler(event, context):

    # resource
    s3 = boto3.resource('s3')

    # get bucket name and the csv file name from the 'event' input
    main_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # define the name of the error bucket to copy into
    error_bucket = 'error-bucket-name'
    error_bucket = error_bucket.lower()

    # download the csv file from s3, read the content, decode from bytes to string, and split the content by lines
    object = s3.Object(main_bucket, key)
    data = object.get()['Body'].read().decode('utf-8').splitlines()

    # create an error variable default to False
    error = False

    # define valid product lines and valid currencies
    valid_product_line = ['Bakery','Meat', 'Dairy']
    valid_currencies = ['USD', 'CAD', 'MXN']

    # read the csv content line by line using pythons csv reader
    for row in csv.reader(data[1:], delimiter=','):
        # for each row extract the product line, currency, bill amount, and date from the specific columns
        date = row[6]
        product_line = row[4]
        currency = row[7]

        # check if the product line is valid and if it isnt, set error flag to true and print an error message
        if product_line not in valid_product_line:
            error = True
            print(f"Error in record {row[0]}: incorrect product line: {product_line}.")
            continue

        # check if the currency is valid, if not set error flag to true and print an error message
        if currency not in valid_currencies:
            error = True
            print(f"Error in record {row[0]}: incorrect currency: {currency}.")
            continue

        # check if the date is in the correct format ('%Y-%m-%d') - if not set error flag to true and print an error message
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            error = True
            print(f"Error in record {row[0]}: incorrect date format: {date}.")
            continue

    # after checking all rows, if an error is found, copy the csv file to the error bucket and delete it from the original bucket
    if error:
        copy_source = {
            'Bucket': main_bucket,
            'Key': key
        }
        try:    
            s3.meta.client.copy(copy_source, error_bucket, key)
            print(f"Moved error file to: {error_bucket}.")
            s3.Object(main_bucket, key).delete()
            print(f"Deleted original file from {main_bucket}.")
        except Exception as e:
            print(f"Error while moving file: {str(e)}.")
    else:
        return {
            'statusCode': 200,
            'body': 'No errors found in csv file.'
        }