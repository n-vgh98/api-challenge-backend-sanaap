import uuid
import boto3
from django.conf import settings
from botocore.exceptions import ClientError


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def upload_file_to_minio(file_obj, content_type):
    bucket_name = settings.AWS_PRIVATE_BUCKET_NAME

    s3 = get_s3_client()
    unique_name = f"{uuid.uuid4()}_{file_obj.name}"

    extra_args = {
        "ContentType": content_type,
        "ACL": "private"
    }

    try:
        s3.upload_fileobj(
            file_obj,
            bucket_name,
            unique_name,
            ExtraArgs=extra_args
        )
    except Exception as e:
        raise Exception(f"MinIO upload failed: {e}")
    file_url = get_file_url_from_minio(unique_name)
    return unique_name, file_url


def get_file_url_from_minio(filename, expires_in=2592000):
    bucket_name = settings.AWS_PRIVATE_BUCKET_NAME
    s3 = get_s3_client()
    try:
        return s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": filename},
            ExpiresIn=expires_in,
        )
    except Exception as e:
        raise Exception(f"MinIO signed URL error: {e}")


def delete_from_minio(filename):
    bucket_name = settings.AWS_PRIVATE_BUCKET_NAME
    s3 = get_s3_client()

    try:
        s3.head_object(Bucket=bucket_name, Key=filename)
        s3.delete_object(Bucket=bucket_name, Key=filename)
        return True

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise Exception(f"MinIO delete failed: {e}")
