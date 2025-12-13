import boto3, botocore, zipfile, os
from pathlib import Path

# variables
region = 'us-east-1'
bucket_name = 'lambda-bucket-0214'
lambda_file_path = Path(r"E:/Scripts/projects/s3-data-validation/lambda/lambda.py")
zip_name = lambda_file_path.parent / 'lambda.zip'
s3_key = f"lambda/{zip_name}"

# client
s3 = boto3.client('s3', region_name=region)

# create bucket
def create_bucket_with_versioning():
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region}
                         )
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists and is owned by you.")
    
        elif error_code == 'BucketAlreadyExists':
            raise RuntimeError(
                print(f"Bucket name '{bucket_name}' already exists and is owned by another AWS account.")
            )

        else:
            raise

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
    create_bucket_with_versioning()
    zip_lambda_file()
    upload_zip_to_s3()