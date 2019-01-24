"""
Utilities for handling data that's submitted for the shops.

Adapted s3 uploads from http://zabana.me/notes/upload-files-amazon-s3-flask.html
"""
import os.path
from uuid import uuid4

import boto3, botocore
from flask import current_app

s3 = boto3.client("s3")


def upload_file_to_s3(file, bucket_name=None, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    if not bucket_name:
        bucket_name = current_app.config['S3_BUCKET']

    current_app.logger.info(bucket_name)
    bucket_path = path_in_bucket(file.filename)

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            bucket_path,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        current_app.logger.exception(e)
        raise

    return bucket_path


def secure_filename(filename):
    """
    Replace the start of a filename with a UUID and return it

    :param filename: Filename to be replaced
    :rtype: str
    """

    ext = os.path.splitext(filename)[-1]

    return str(uuid4()) + ext


def path_in_bucket(filename):
    """
    Join a filename with the key to the folder based on the environment

    :param filename: Filename to be replaced
    :rtype: str
    """
    folder = current_app.config['S3_KEY_BASE']
    env = current_app.config['FLASK_ENV']
    return f'{env}/{folder}/{filename}'
