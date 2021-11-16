# python-training
Python Training Repository

## How to Use
Create virtual environment  
```
$ cd python-training
$ python3 -m venv .venv
```
  
Update & Install python libraries.  
```
$ pip install -U pip
$ pip install -U setuptools
$ pip install -r requirements.txt
```

#### COSMOS DB
if you would like to execute cosmos-db sample codes, change `cosmos-db/init.sh` and execute it.
```
$ vim init.sh
$ chmod +x init.sh
$ source init.sh
```
## Trouble Shooting
If you face `ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.` error in pip command, you should set below config.
```
$ export PIP_USER=false
```