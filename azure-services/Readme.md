# azure-services
This project have azure service scripts.

## cosmos-db.py on local
1. Set environment variables  
```bash:
$ cd azure-services
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Run Python script  
```bash:
$ pip install --upgrade pip
$ pip install --upgrade setuptools
$ pip install azure-cosmos
$ pip install pandas
$ python cosmos-db.py
```
  
## Azure Container Registry
1. Set environment variables  
```bash:
$ cd azure-services
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Build Docker image & test run on local docker environment  
if your execution is finished successful, you can see new records in cosmos-db.
```
$ cd azure-services
$ docker build -t batch .
$ docker run --rm -e ACCOUNT_URI -e ACCOUNT_KEY -it batch
```

3. Push Image to Azure Container Registry
You have to change {xxx} to your environment.
```
$ docker login -u {USERNAME} -p {PASSWORD} {REGISTRY}.azurecr.io
$ docker tag batch {REGISTRY}.azurecr.io/batch
$ docker push {REGISTRY}.azurecr.io/batch
```

4. Launch Container by Azure Container Instance
Don't fogot to set ACCOUNT_URI/ACCOUNT_KEY environment variables in launch wizard.

## Reference
[Reference (Japanese)](https://tech-lab.sios.jp/archives/19859)

