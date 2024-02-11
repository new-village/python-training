# Hello PySpark

This is my first PySpark project.

## Learning Objectives

* Install Jupyer and PySpark
* Load the Parquet file into Spark
* Transform the blockchain data for analysis

## Usage

```
cd ~/python-training/hello-pyspark
python3 -m venv .venv
source .venv/bin/activate
pip install -r requrements.txt
ipython kernel install --user --name=.venv --display-name=.venv
```

if you automate to convert file, you can execute batch job below

```shell:
python main.py
```

## Reference
* [Getting Started — PySpark 3.5.0 documentation](https://spark.apache.org/docs/latest/api/python/getting_started/install.html#using-pypi)
* [WSL + vscode 環境でJupyter Notebookを使えるまでの設定](https://qiita.com/gen4pen/items/1252282faa2db22386be)