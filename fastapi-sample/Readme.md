# Rest API
This is a sample REST API back-end application executed on Azure Container Instance.  
  
## How to use
#### Execute application on local
1. Set environment variables by local.sh
```bash:
$ cd fastapi-sample
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
$ cd fastapi-sample
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Build Docker image & test run on local docker environment  
if your execution is finished successful, you can see new records in cosmos-db.
```
$ cd fastapi-sample
$ docker build -t fastapi-sample .
$ docker run --rm -e ${ACCOUNT_URI} -e ${ACCOUNT_KEY} -it fastapi-sample
```

3. Push Image to Azure Container Registry
You can see pushed contaier image on Azure Container Registry > Repository after below commands.
```
$ docker login -u ${USERNAME} -p ${PASSWORD} ${REGISTRY}.azurecr.io
$ docker tag fastapi-sample ${REGISTRY}.azurecr.io/fastapi-sample
$ docker push ${REGISTRY}.azurecr.io/fastapi-sample
```

4. Deploy Web Application
Select Repository > fastapi-sample > latest and select `deploy webapps`  
You can see deployed application on `App Service` page.

5. Set Environment Variables
Select `App Service` > Configuration > New Application Setting.  
Then you have to set ACCOUNT_URI/ACCOUNT_KEY environment variables and Save configuration.
  
  
#### Call API
To call the REST API by CURL, execute below command:
```
$ curl http://127.0.0.1:8000/
$ curl http://127.0.0.1:8000/api/13106/2018
```