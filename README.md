# Project Name
s3-data-validation

## Overview
Creates a Lambda function that will trigger when a new CSV file is uploaded to an S3 bucket. It will validate the file and if discrepancies are found, it will then send to an error bucket.

Example:
> This project automates the creation and management of AWS S3 buckets using CloudFormation and Lambda, with built-in validation and error handling.

---

## Features
- data validation
- automation with lambda
- s3 event notifications
- cloudformation resource deployment

---

## Technologies Used
- Language(s): Python
- Frameworks / SDKs: boto3
- Cloud / Services: AWS (S3, CloudFormation, Lambda)
- Tools: Git, GitHub, VS Code

## Instructions
In zip.py
- line 6 change resource bucket name
- line 19 change main bucket name
- line 20 change error bucket name
- line 21 change aws account id

In resources.yml
- line 57 change resource bucket name to match it in the zip.py file