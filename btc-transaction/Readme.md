# BTC Transaction

This is Bitcoin transaction data collection project. The project collect Blockchain data from AWS using AWS SDK.

## Learning Objectives

* Downloading Blockchain data from AWS

## Usage

```
cd ~/python-training/btc-transaction
python3 -m venv .venv
source .venv/bin/activate
pip install -r requrements.txt
python main.py
```

if you would like to get specific month, you should add argument `YYYYMM` to app.py.
```
python main.py 200901
```

if you would like to get specific day, you should add argument `YYYYMMDD` to app.py.
```
python main.py 20240101
```

## Reference
* [Downloading files - Boto3 1.34.34 documentation (amazonaws.com)](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html)
* [AWS Public Blockchain Data](https://registry.opendata.aws/aws-public-blockchain/)
