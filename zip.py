import boto3, botocore, zipfile, os
from pathlib import Path

# variables
bucket_name = 'LambdaBucketName'
lambda_file_path = Path(r"E:/Scripts/projects/s3-data-validation/lambda/lambda.py")
zip_name = lambda_file_path.parent / 'lambda.zip'
s3_key = f"lambda/{zip_name}"

# client
s3 = boto3.client('s3')

# zip the .py file
def zip_lambda_file():
    if not lambda_file_path.exists():
        raise FileNotFoundError(f"{lambda_file_path} does not exist.")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(
            lambda_file_path,
            arcname=lambda_file_path.name
        )

    print(f"Zipped {lambda_file_path} into {zip_name}")

# s3 upload
def upload_zip_to_s3():
    s3.upload_file(zip_name, bucket_name, s3_key)
    print(f"Uploaded {zip_name} to s3://{bucket_name}/{s3_key}")

if __name__ == '__main__':
    zip_lambda_file()
    upload_zip_to_s3()