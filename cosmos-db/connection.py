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

import logging
from logging.config import fileConfig

def connection(_container, _partition):
    # Create the client
    url = os.environ['ACCOUNT_URI']
    key = os.environ['ACCOUNT_KEY']
    client = CosmosClient(url, credential=key)

    # Create or Get Database
    try:
        database = client.create_database(os.environ['COSMOS_DB'])
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(os.environ['COSMOS_DB'])

    # Create or Get Container
    try:
        container = database.create_container(id=_container, partition_key=PartitionKey(path=_partition))
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(_container)
    except exceptions.CosmosHttpResponseError:
        raise    

    return container

def main():
    container = connection('items', '/_id')
    # Get top 10 records
    item_list = list(container.read_all_items(max_item_count=10))
    # 件数の出力
    print('Found {0} items'.format(item_list.__len__()))
    # 取得したレコードのIDフィールドを出力
    for doc in item_list:
        print('Item Id: {0}'.format(doc.get('id')))

if __name__ == "__main__":
    # load logging configuration
    cd = os.path.dirname(os.path.abspath(__file__))
    logging.config.fileConfig(cd + '/config/logging.ini')
    logger = logging.getLogger(__name__)

    # call main function
    main()
