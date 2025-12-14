import boto3
import csv
from datetime import datetime
import urllib.parse

def lambda_handler(event, context):

    # resource
    s3 = boto3.resource('s3')

    # get bucket name and the csv file name from the 'event' input
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # define the name of the error bucket to copy into
    error_bucket = 'ErrorBucketName'
    error_bucket = error_bucket.lower()

    # download the csv file from s3, read the content, decode from bytes to string, and split the content by lines
    obj = s3.get_object(
        Bucket=bucket_name,
        Key=key
    )

    body = obj['Body'].read()

    print(body)

    # initialize an error flag to false - we will set this flag to true when we find an error
    error_found = False

    # define valid product lines and valid currencies
    valid_product_line = 'meat'
    valid_currency = ['USD', 'CAD', 'MXN']

    # read the csv content line by line using pythons csv reader - ignore the header line (data[1:])
    

        # for each row extract the product line, currency, bill amount, and date from the specific columns

        # check if the product line is valid and if it isnt, set error flag to true and print an error message

        # check if the currency is valid, if not set error flag to true and print an error message

        # check if the bill amount is negative, if so set error flag to true and print an error message

        # check if the date is in the correct format ('%Y-%m-%d') - if not set error flag to true and print an error message

    # after checking all rows, if an error is found, copy the csv file to the error bucket and delete it from the original bucket
    
        # handle any exception that may occur while moving the file and print the message

    # if no errors were found, return a success message with the status code of 200 and a body message indicating that no errors were found


    return {
        'statusCode': 200,
        'body': print('Success')
    }