# Rest API
This is a sample REST API back-end application executed on Azure Container Instance.  
  
## How to use
#### Execute application on local
1. Set environment variables by local.sh
```bash:
$ cd rest_api
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Run Python script  
```bash:
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install --upgrade setuptools
$ pip install -r requirements.txt
$ python app.py
```
  
#### Execute application on Azure Container Registry
1. Set environment variables  
```bash:
$ cd rest_api
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Build Docker image & test run on local docker environment  
if your execution is finished successful, you can see new records in cosmos-db.
```
$ cd rest_api
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
  
#### Call API
To call the REST API by CURL, execute below command:
```
$ curl http://127.0.0.1:5000/
$ curl http://127.0.0.1:5000/api/13106/2018
```