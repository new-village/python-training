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
$ source local.sh
$ docker build -t batch .
$ docker run -e ACCOUNT_URI -e ACCOUNT_KEY -it -rm batch
```



## Reference
[Reference (Japanese)](https://tech-lab.sios.jp/archives/19859)

