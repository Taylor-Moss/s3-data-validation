import boto3
import csv
from datetime import datetime

def lambda_handler(event, context):

    # resource
    s3 = boto3.resource('s3')

    # get bucket name and the csv file name
    