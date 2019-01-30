"""
Utilities for handling data that's submitted for the shops.

Adapted s3 uploads from http://zabana.me/notes/upload-files-amazon-s3-flask.html
"""
import os.path
from uuid import uuid4

from flask import current_app

from coffeeshop.server import photos, s3


def save_photo(file):
    """
    Generic entry point for saving a photo

    If the current application is a production or testing app then assume that
    you're always going to upload to S3. Otherwise, if your app is a
    development app assume you're always going to use Flask-Uploads

    :param file: File to upload from form
    :return: path to file
    :rtype: str
    """
    if current_app.config['FLASK_ENV'] in ('production', 'testing'):
        return upload_file_to_s3(file)

    # otherwise assume development
    return upload_file_to_disk(file)


def upload_file_to_disk(file):
    """
    Use flask_uploads to save the file to disk

    :param file: File to be uploaded
    :return: Path to file
    :rtype: str
    """
    return photos.url(
        photos.save(file)
    )


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

    except Exception as error:
        current_app.logger.exception(error)
        raise

    base_url = current_app.config['S3_LOCATION']

    return f'{base_url}/{bucket_name}/{bucket_path}'


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
