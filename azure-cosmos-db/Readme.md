# Azure Cosmos DB
This is the sample code of Azure Cosmos DB by Python.

## How to USE
1. Copy `init.sh` with name `local.sh`.  
This is for security reasons, avoid to upload user defined information to git services.

```bash:
$ cd azure-cosmos-db
$ cp init.sh local.sh
```

2. Set `URI` and `Primary Key` to `local.sh`.  
`URI` and `Primary Key` can be confirmed in Azure Cosmos DB Account Page. Details can see [this document](https://docs.microsoft.com/ja-jp/azure/cosmos-db/secure-access-to-data?tabs=using-primary-key).
```bash:
$ cd azure-cosmos-db
$ vim local.sh
$ source local.sh
```

3. Install related libraries
```bash:
$ cd azure-cosmos-db
$ pip install azure-cosmos
```

4. Execute script
```bash:
$ python main.py 
```
