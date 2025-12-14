import boto3, botocore, zipfile, os, time
from pathlib import Path

# general variables
region = 'us-east-1'
bucket_name = 'resource-bucket-hk99'

# lambda variables
lambda_file_path = Path(r"E:/Scripts/projects/s3-data-validation/lambda/lambda.py")
lambda_file_name = 'lambda/lambda.zip'
zip_name = lambda_file_path.parent / 'lambda.zip'
lambda_key = 'lambda/lambda.zip'

# cfn variables
stack_name = 'stack-1'
cfn_file_path = Path(r"E:/Scripts/projects/s3-data-validation/resources.yml")
cfn_name = 'resources.yml'
cfn_key = f"cloudformation/{cfn_name}"
main_bucket_name = 'main-bucket-fa54'
error_bucket_name = 'error-bucket-fa54'
account_id = str(271443544393)

# client
s3 = boto3.client('s3', region_name=region)
cfn = boto3.client('cloudformation', region_name=region)

# create bucket
def create_bucket_with_versioning():
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={"Status": "Enabled"}
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
    s3.upload_file(lambda_file_name, bucket_name, lambda_key)
    print(f"Uploaded {lambda_file_name} to s3://{bucket_name}/{lambda_key}")

def upload_cfn_to_s3():
    s3.upload_file(cfn_name, bucket_name, cfn_key)
    print(f"Uploaded {cfn_name} to s3://{bucket_name}/{cfn_key}")

def create_cfn_stack():
    response = cfn.create_stack(
    StackName=stack_name,
    TemplateURL=f"https://{bucket_name}.s3.{region}.amazonaws.com/cloudformation/{cfn_name}",
    Capabilities=[
        'CAPABILITY_NAMED_IAM'
    ],
    Parameters=[
        {
            'ParameterKey': 'MainBucketName',
            'ParameterValue': main_bucket_name,
        },
        {
            'ParameterKey': 'ErrorBucketName',
            'ParameterValue': error_bucket_name,
        },
        {
            'ParameterKey': 'AccountId',
            'ParameterValue': account_id,
        },
    ],
)

if __name__ == '__main__':
    create_bucket_with_versioning()
    zip_lambda_file()
    upload_zip_to_s3()
    upload_cfn_to_s3()
    create_cfn_stack()