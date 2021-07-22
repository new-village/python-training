""" zipcode.py
This script download postal code list of Tokyo from Japan Post
"""
import os
import json
import pandas as pd
import logging
import requests

from io import BytesIO
from zipfile import ZipFile
from logging.config import fileConfig


class ziplist:
    def __init__(self):
        self.ses = requests.Session()
        self.url = 'https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/'

    def download(self, file):
        try:
            # endpoint への get request
            url = self.url + file.lower()
            res = self.ses.get(url)
            logger.info('Try to get ' + url)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            # 例外エラーの場合はスクリプトを停止
            logger.error(
                'Request is failure: Name, server or service not known')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

        # Response Status Confirmation
        if res.status_code not in [200]:
            # HTTP Response is not 200 (Normal)
            logger.error('Request to ' + url +
                         ' has been failure: ' + str(res.status_code))
            raise SystemExit()

        self.res = res.content
        return self

    @property
    def dataframe(self):
        # Unzip HTTP response file
        zipfiles = ZipFile(BytesIO(self.res))

        # Get File Name
        fn = [f for f in zipfiles.namelist() if '.csv' in f.lower()]
        if len(fn) == 1:
            # ZIPファイルから特定のCSVファイルを取得
            csv = zipfiles.open(fn[0])
            # CSVの読み込みとヘッダー情報の付与
            df = pd.read_csv(csv, encoding='shift-jis')
            df.columns = ["gov_cd", "old_postal_cd", "postal_cd", "state_kana", "city_kana",
                          "address", "state", "city", "address", "flg1", "flg2", "flg3", "flg4", "flg5", "flg6"]

            logger.info('Try to convert ' + fn[0] + ' to Pandas Dataframe')
        else:
            # Unexpected Zipfile Structure Error
            logger.error(
                'Unexpected Zipfile Structure. There is no CSV or many CSVs.')
            raise SystemExit()

        return df


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.config.fileConfig('./config/logging.ini')
    logger = logging.getLogger()

    # Download ZIP File Strings
    zipf = ziplist().download('13TOKYO.ZIP').dataframe
    print(zipf)
