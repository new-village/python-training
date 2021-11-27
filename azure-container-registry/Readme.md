# Azure Container registry
This is the sample code of Azure Container Registry.

## How to USE
1. Copy `init.sh` with name `local.sh`.  
This is for security reasons, avoid to upload user defined information to git services.

```bash:
$ cd azure-container-registry
$ cp init.sh local.sh
```

2. Set `Registry Name`, `User Name` and `Password` to `local.sh`.  
`Registry Name`, `User Name` and `Password` can be confirmed in Azure Container Registry Page.
```bash:
$ cd azure-container-registry
$ vim local.sh
$ source local.sh
```

3. Build Docker image locally.
```bash:
$ cd azure-container-registry
$ docker build -t sample-batch .
```

4. Push Image to Azure Container Registry
```
$ docker login -u ${USERNAME} -p ${PASSWORD} ${REGISTRY}.azurecr.io
$ docker tag sample-batch ${REGISTRY}.azurecr.io/sample-batch
$ docker push ${REGISTRY}.azurecr.io/sample-batch
```

## Note
#### Local Container Execution
If you execute the script locally, put below command in your console.
```bash:
$ docker run --rm -e MESH=500 -it sample-batch
```

If you would like to execute batch on Azure, you can deploy container to `Azure Batch Service`.  
See details is [the document](https://dev.to/kenakamu/use-container-for-azure-batch-service-2mnn).

## Reference
[Reference (Japanese)](https://tech-lab.sios.jp/archives/19859)
