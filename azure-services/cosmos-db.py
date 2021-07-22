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
import datetime

import logging
import logging.config


class cosmos():
    def __init__(self):
        # Create the client
        url = os.environ['ACCOUNT_URI']
        key = os.environ['ACCOUNT_KEY']
        client = CosmosClient(url, credential=key)

        # Create or Get Database
        try:
            self.database = client.create_database('cosmos_db')
        except exceptions.CosmosResourceExistsError:
            self.database = client.get_database_client('cosmos_db')

        # Create or Get Container
        try:
            self.container = self.database.create_container(id='sample', partition_key=PartitionKey(path='/_id'))
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client('sample')
        except exceptions.CosmosHttpResponseError:
            raise

    def count(self):
        count = list(self.container.read_all_items()).__len__()
        return count

    def select_all(self):
        items = list(self.container.read_all_items())
        return items

    def upsert(self, items):
        for i in items:
            self.container.upsert_item(i)


if __name__ == "__main__":
    # load logging configuration
    logging.config.fileConfig('./config/logging.ini')
    logger = logging.getLogger()

    # call main function
    db = cosmos()

    # 件数の出力
    print('Found {0} items'.format(db.count()))

    # 取得したレコードのIDフィールドを出力
    for doc in db.select_all():
        print(doc)

    # 新規レコードの追加
    now = datetime.datetime.now()
    rec = {
        'id': str(int(db.select_all()[db.count() - 1].get('id')) + 1),
        'create_dttm': now.strftime('%Y/%m/%dT%H:%M:%S.%fZ')
    }
    db.upsert(rec)
