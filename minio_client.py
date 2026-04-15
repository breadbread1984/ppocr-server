#!/usr/bin/python3

from typing import List, Optional
from os.path import basename
import json
from urllib.parse import urlparse
from minio import Minio
from minio.error import S3Error

class MinioClient(object):
  def __init__(self, configs):
    self.client = Minio(
      endpoint = configs.minio_host,
      access_key = configs.minio_user,
      secret_key = configs.minio_password,
      secure = False
    )
    self.configs = configs
  def create_bucket(self, bucket):
    if self.client.bucket_exists(bucket_name = bucket): return False
    self.client.make_bucket(bucket_name = bucket)
    policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {"AWS": ["*"]},
          "Action": ["s3:GetObject"],
          "Resource": [f"arn:aws:s3:::{bucket}/*"]
        },
        {
          "Effect": "Allow",
          "Principal": {"AWS": ["*"]},
          "Action": ["s3:ListBucket"],
          "Resource": [f"arn:aws:s3:::{bucket}"]
        }
      ]
    }
    try:
      self.client.set_bucket_policy(bucket_name = bucket, policy = json.dumps(policy))
    except S3Error as e:
      raise
    return True
  def list_objects(self, bucket):
    if not self.client.bucket_exists(bucket_name = bucket): return None
    objects = self.client.list_objects(bucket_name = bucket, recursive = True)
    return [obj.object_name for obj in objects]
  def clear_bucket(self, bucket):
    if not self.client.bucket_exists(bucket_name = bucket): return False
    for obj in self.client.list_objects(bucket_name = bucket, recursive = True):
      self.client.remove_object(bucket_name = bucket, object_name = obj.object_name)
    return True
  def remove_bucket(self, bucket):
    if not self.client.bucket_exists(bucket_name = bucket): return False
    self.clear_bucket(bucket = bucket)
    self.client.remove_bucket(bucket_name = bucket)
    return True
  def download_impl(self, bucket, filename, output_path):
    self.client.fget_object(bucket_name = bucket, object_name = filename, file_path = output_path)
  def download(self, url, output_path):
    parsed_url = urlparse(url)
    elems = parsed_url.path.split('/')
    bucket = elems[-2]
    filename = elems[-1]
    self.download_impl(bucket, filename, output_path)
  def upload(self, bucket, input_path, object_name = None):
    if not self.client.bucket_exists(bucket_name = bucket):
      self.client.make_bucket(bucket_name = bucket)
    self.client.fput_object(
      bucket_name = bucket,
      object_name = basename(input_path) if object_name is None else object_name,
      file_path = input_path
    )
    return f"http://{self.configs.minio_host}/{bucket}/{basename(input_path) if object_name is None else object_name}"
  def remove(self, url):
    parsed_url = urlparse(url)
    elems = parsed_url.path.split('//')
    bucket = elems[-2]
    filename = elems[-1]
    self.remove_impl(bucket, filename)
  def remove_impl(self, bucket, filename):
    self.client.remove_object(bucket_name = bucket, object_name = filename)

