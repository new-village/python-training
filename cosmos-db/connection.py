""" connection.py
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
from logging.config import fileConfig

class cosmos():
    def __init__(self, _container, _partition):
        # Create the client
        url = os.environ['ACCOUNT_URI']
        key = os.environ['ACCOUNT_KEY']
        client = CosmosClient(url, credential=key)

        # Create or Get Database
        try:
            self.database = client.create_database(os.environ['COSMOS_DB'])
        except exceptions.CosmosResourceExistsError:
            self.database = client.get_database_client(os.environ['COSMOS_DB'])

        # Create or Get Container
        try:
            self.container = self.database.create_container(id=_container, partition_key=PartitionKey(path=_partition))
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client(_container)
        except exceptions.CosmosHttpResponseError:
            raise

    def count(self):
        count = list(self.container.read_all_items()).__len__()
        return count

    def select_all(self):
        items = list(self.container.read_all_items())
        return items
    
    def upsert(self, item):
        res = self.container.upsert_item(item)
        return res


def main():
    items = cosmos('items', '/_id')

    # 件数の出力
    print('Found {0} items'.format(items.count()))
    
    # 取得したレコードのIDフィールドを出力   
    for doc in items.select_all():
        print(doc)

    # 新規レコードの追加
    now = datetime.datetime.now()
    rec = {
        'id': str(int(items.select_all()[items.count() - 1].get('id')) + 1),
        'create_dttm': now.strftime('%Y/%m/%dT%H:%M:%S.%fZ')
        }
    items.upsert(rec)


if __name__ == "__main__":
    # load logging configuration
    cd = os.path.dirname(os.path.abspath(__file__))
    logging.config.fileConfig(cd + '/config/logging.ini')
    logger = logging.getLogger(__name__)

    # call main function
    main()
