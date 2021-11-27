# python-training
This is my python training repository. The project stored minimum application for each flameworks and services. If you want to know app details, please read each app's `Readme.md`.

## Applications
| Application Name         | Summary |
| ------------------------ | ------- |
| azure-blob-storage       | The Application manipulate files or data with Azure BLOB Storage                   |
| azure-container-registry | The Application makes python docker container and push to Azure Container Registry |
| azure-cosmos-db          | Insert records to Cosmos DB and get all records from DB                            |
| fastapi-sample           | Data Collection and Generate REST API Service by FastAPI framework           |
| import-understanding     | Understanding for python import mechanism.                                   |
| requests                 | Understanding for requests library and stream unzip.                         |


## Trouble Shooting
If you face `ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.` error in pip command, you should set below config.
```
$ export PIP_USER=false
```

## Note
This project has been created on [gitpod](https://www.gitpod.io/).