""" loader.py
"""
import os
import boto3
from logging import getLogger
from botocore.config import Config
from botocore import UNSIGNED

logger = getLogger(__name__)

class S3Blockchain:
    def __init__(self):
        self.s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        self.bucket_name = 'aws-public-blockchain'

    def _list_objects(self, prefix):
        return self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix).get('Contents', [])

    def download_btc_transactions(self, date):
        prefix = f'v1.0/btc/transactions/date={date}/'
        file_path = f'./data/date={date}/'
        contents = self._list_objects(prefix)

        if contents:
            for content in contents:
                file_name = content['Key'].split('/')[-1]
                os.makedirs(file_path, exist_ok=True)
                self.s3.download_file(self.bucket_name, content['Key'], os.path.join(file_path, file_name))
                logger.info(f'[SUCCESS] Downloaded {file_name} to {file_path}')
        else:
            logger.warning(f'[FAILURE] {prefix} is not Found')
