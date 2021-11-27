""" azure-cosmos-db/main.py
Azure COSMOS DB への接続とレコード取得用スクリプト

注意：
事前に環境変数（init.sh）を設定する必要があります。

参考：
https://pypi.org/project/azure-cosmos/
https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples#item-examples
"""
from azure.cosmos import CosmosClient, exceptions, PartitionKey
import os
import datetime

import logging
import logging.config


class cosmos():
    def __init__(self, container_name):
        # USER DEFINE VARIABLES: Container Name
        database_name = 'python-training'

        # Create the client
        try:
            url = os.environ['ACCOUNT_URI']
            key = os.environ['ACCOUNT_KEY']
            client = CosmosClient(url, credential=key)
        except KeyError as e:
            logger.error('There is no expected environment variables.')
            raise SystemExit(e)

        # Create or Get Database
        try:
            self.database = client.create_database(database_name)
            logger.info('Create database is successfully finished: ' + database_name)
        except exceptions.CosmosResourceExistsError:
            self.database = client.get_database_client(database_name)
            logger.info(database_name + ' is already exists.')
            pass

        # Create or Get Container
        try:
            self.container = self.database.create_container(id=container_name, partition_key=PartitionKey(path='/_id'))
            logger.info('Create Container is successfully finished: ' + container_name)
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client(container_name)
            logger.info(container_name + ' is already exists.')
        except exceptions.CosmosHttpResponseError as e:
            logger.error('Connection error')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

    def select_all(self):
        # Get all records
        items = list(self.container.read_all_items())
        # Reduct system columns
        for i in items:
            [i.pop(key, 'x') for key in ['_rid', '_self', '_etag', '_attachments', '_ts']]
        return items

    def upsert(self, items):
        try:
            if isinstance(items, dict):
                res = [self.container.upsert_item(items)]
                logger.info('Upsert {0} items is successfully finished'.format(len(res)))
            elif isinstance(items, list):
                res = [self.container.upsert_item(i) for i in items]
                logger.info('Upsert {0} items is successfully finished'.format(len(res)))
        except Exception as e:
            logger.error('There is data integrity issue')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

        return res


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # call main function
    db = cosmos('sample')

    # insert records
    # items = {'id': 'aaa', 'create_dttm': datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%fZ')}
    items = [{'id': str(num), 'create_dttm': datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%fZ')} for num in range(10)]
    db.upsert(items)

    # get all records
    records = db.select_all()
    logger.info(str(records))
