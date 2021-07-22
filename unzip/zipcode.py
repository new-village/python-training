""" zipcode.py
郵便局の郵便番号データダウンロードサイトから東京都の郵便番号をダウンロードして解凍するスクリプト
"""
import os
import requests
import json
import pandas as pd
import logging
from zipfile import ZipFile
from io import BytesIO
from logging.config import fileConfig


def download(url):
    try:
        # endpoint への get request
        res = requests.get(url)
        logger.info('Try to get ' + url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        # 例外エラーの場合はスクリプトを停止
        logger.error('Request is failure: Name, server or service not known')
        logger.error('Trace', exc_info=True)
        raise SystemExit(e)

    # Response Status Confirmation
    if res.status_code not in [200]:
        # HTTP Response is not 200 (Normal)
        logger.error('Request to ' + endpoint + ' has been failure: ' + str(res.status_code))
        logger.error(res.content.decode())
        raise SystemExit()    

    return res.content


def zip_to_df(content):
    # Unzip HTTP response file
    zipfiles = ZipFile(BytesIO(content))

    # Get File Name
    fn = [f for f in zipfiles.namelist() if '.csv' in f.lower()]
    if len(fn) == 1:
        # ZIPファイルから特定のCSVファイルを取得
        csv = zipfiles.open(fn[0])
        # CSVの読み込みとヘッダー情報の付与
        df = pd.read_csv(csv, encoding='shift-jis')
        df.columns=["gov_cd", "old_postal_cd", "postal_cd", "state_kana", "city_kana", "address", "state", "city", "address", "flg1", "flg2", "flg3", "flg4", "flg5", "flg6"]

        logger.info('Try to convert ' + fn[0] + ' to Pandas Dataframe')
    else:
        # Unexpected Zipfile Structure Error
        logger.error('Unexpected Zipfile Structure. There is no CSV or many CSVs.')
        raise SystemExit()

    return df


if __name__ == "__main__":
    # Load logger config & Set Logger
    cd = os.path.dirname(os.path.abspath(__file__))
    logging.config.fileConfig(cd + '/config/logging.ini')
    logger = logging.getLogger()

    # Download ZIP File Strings
    url = 'https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/13tokyo.zip'
    zip_strings = download(url)

    # Extract CSV file from ZIP File Strings
    df = zip_to_df(zip_strings)
    print(df)