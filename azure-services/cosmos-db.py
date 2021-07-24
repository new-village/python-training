""" cosmos-db.py
Azure COSMOS DB への接続とレコード取得用スクリプト

注意：
事前に環境変数（init.sh）を設定する必要があります。

参考：
https://pypi.org/project/azure-cosmos/
https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples#item-examples
"""
from azure.cosmos import CosmosClient, exceptions, PartitionKey
import os
import pandas as pd
import datetime

import logging
import logging.config


class cosmos():
    def __init__(self):
        # Set logger
        logger = logging.getLogger()

        # Create the client
        url = os.environ['ACCOUNT_URI']
        key = os.environ['ACCOUNT_KEY']
        client = CosmosClient(url, credential=key)

        # Create or Get Database
        try:
            self.database = client.create_database('cosmos_db')
            logger.debug('Create cosmos_db database')
        except exceptions.CosmosResourceExistsError:
            self.database = client.get_database_client('cosmos_db')
            logger.debug('Connect database to cosmos_db')

        # Create or Get Container
        try:
            self.container = self.database.create_container(id='sample', partition_key=PartitionKey(path='/_id'))
            logger.debug('Create sample table')
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client('sample')
            logger.debug('Connect table to sample')
        except exceptions.CosmosHttpResponseError as e:
            logger.error('Connection error')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

    def count(self):
        count = list(self.container.read_all_items()).__len__()
        return count

    def select_all(self):
        self.items = list(self.container.read_all_items())
        return self

    @property
    def dataframe(self):
        try:
            df = pd.DataFrame(self.items)
            df = df.set_index('id', drop=True)
            logger.info('Try to convert ' + str(len(self.items)) + ' records to Pandas Dataframe')
        except Exception as e:
            # Unexpected zipffile structure error
            logger.error('Unexpected item structure: ' + str(len(self.items)) + ' records')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

        return df

    def upsert(self, items):
        try:
            if isinstance(items, dict):
                res = [self.container.upsert_item(items)]
                logger.debug('Upsert {0} items'.format(len(res)))
            elif isinstance(items, list):
                res = [self.container.upsert_item(i) for i in items]
                logger.debug('Upsert {0} items'.format(len(res)))
        except Exception as e:
            logger.error('There is data integrity issue')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

        return res


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.config.fileConfig('./config/logging.ini')
    logger = logging.getLogger()

    # call main function
    db = cosmos()
    # 取得レコードの出力
    print(db.select_all().dataframe)

    # 新規レコードの追加
    now = datetime.datetime.now()
    rec = {
        'id': str(db.count() + 1),
        'create_dttm': now.strftime('%Y/%m/%dT%H:%M:%S.%fZ'),
        'created_by': 'cosmos-db.py'
    }
    db.upsert(rec)
