# Azure Blob Storage Sample
This is the sample code of Azure Blob Storage by Python.

## How to USE
1. Copy `init.sh` with name `local.sh`.  
This is for security reasons, avoid to upload user defined information to git services.

```bash:
$ cd azure-blob-storage
$ cp init.sh local.sh
```

2. Set `Storage Account Name` and `Key` to `local.sh`.  
`Storage Account Name` and `Key` can be confirmed in Azure Storage Account Page. Details can see [this document](https://docs.microsoft.com/ja-jp/azure/storage/blobs/storage-quickstart-blobs-python#copy-your-credentials-from-the-azure-portal).
```bash:
$ cd azure-blob-storage
$ vim local.sh
$ source local.sh
```

3. Install related libraries
```bash:
$ cd azure-blob-storage
$ pip install azure-storage
```

4. Execute script
```bash:
$ python main.py 
```
