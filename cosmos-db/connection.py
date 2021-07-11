""" connection.py
Azure COSMOS DB への接続とレコード取得用スクリプト

注意：
事前に環境変数（init.sh）を設定する必要があります。

参考：
https://pypi.org/project/azure-cosmos/
https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-python-samples#item-examples
"""
from azure.cosmos import CosmosClient
import os

# Create the client
url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
# Get Database
database_name = os.environ['COSMOS_DB']
database = client.get_database_client(database_name)
# Get Container
container_name = os.environ['COSMOS_CTNR']
container = database.get_container_client(container_name)

# Get top 10 records
item_list = list(container.read_all_items(max_item_count=10))
# 件数の出力
print('Found {0} items'.format(item_list.__len__()))
# 取得したレコードのIDフィールドを出力
for doc in item_list:
    print('Item Id: {0}'.format(doc.get('id')))
