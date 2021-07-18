""" package.py
パッケージ化の練習スクリプト
"""
import os
from azure.cosmos import CosmosClient, exceptions, PartitionKey


class dataloader():
    def __init__(self):
        # Create the client
        url = os.environ['ACCOUNT_URI']
        key = os.environ['ACCOUNT_KEY']
        client = CosmosClient(url, credential=key)

        # Create or Get Database
        try:
            self.database = client.create_database('real-estate')
        except exceptions.CosmosResourceExistsError:
            self.database = client.get_database_client('real-estate')

        # Create or Get Container
        try:
            self.container = self.database.create_container(id='trades', partition_key=PartitionKey(path='/_id'))
        except exceptions.CosmosResourceExistsError:
            self.container = self.database.get_container_client('trades')
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