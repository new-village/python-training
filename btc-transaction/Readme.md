# Hello PySpark

This is my first PySpark project. The project collect Blockchain data from AWS, then load data to spark.

## Learning Objectives

* Understanding PySpark
* Downloading Blockchain data from AWS

## Usage

```
cd ~/python-training/hello-pyspark
python3 -m venv .venv
source .venv/bin/activate
pip install -r requrements.txt
python app.py
```

if you would like to get specific year and month data, you should add argument `YYYYMM` to app.py.
```
python app.py 200901
```

## Reference
* [Downloading files - Boto3 1.34.34 documentation (amazonaws.com)](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html)