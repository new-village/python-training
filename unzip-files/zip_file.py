""" unzip-files/zip.py
Download & unzip files of japanese zipcode list from Japan Post Bank

"""
import logging
import logging.config
from io import BytesIO, StringIO
from zipfile import ZipFile

import pandas as pd
import requests


class ZipCodeHandler:
    def __init__(self):
        self.ses = requests.Session()
        self.url = 'https://www.post.japanpost.jp/zipcode/dl/kogaki/zip/'

    def download(self, file):
        try:
            # Get request to japanpost
            url = self.url + file.lower()
            res = self.ses.get(url)
            logger.info('Try to get ' + url)
        except requests.exceptions.RequestException as e:
            # Exception error handling
            logger.error('Request is failure: Name, server or service not known')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

        # Response Status Confirmation
        if res.status_code not in [200]:
            # HTTP Response is not 200 (Normal)
            logger.error('Request to ' + url + ' has been failure: ' + str(res.status_code))
            raise SystemExit()

        return self._extract_csv(res.content)

    def _extract_csv(self, content):
        # Unzip HTTP response file
        zipfiles = ZipFile(BytesIO(content))

        # Get file name
        fn = [f for f in zipfiles.namelist() if '.csv' in f.lower()]
        if len(fn) == 1:
            logger.info('Try to unzip ' + fn[0])
            # Unzip file name from zip file
            zip_obj = zipfiles.open(fn[0])
            csv = zip_obj.read()
        else:
            # Unexpected zipffile structure error
            logger.error('Unexpected Zipfile Structure. There is no CSV or many CSVs.')
            raise SystemExit()

        return csv.decode('shift-jis')

    def to_dataframe(self, csv):
        try:
            # Read csv file to pandas dataframe
            df = pd.read_csv(StringIO(csv), header=None)
            df.columns = ["gov_cd", "old_postal_cd", "postal_cd", "state_kana", "city_kana",
                          "address", "state", "city", "address", "flg1", "flg2", "flg3", "flg4", "flg5", "flg6"]
            logger.info('Try to convert csv to dataframe: ' + str(df.shape))
        except Exception as e:
            # Exception error handling
            logger.error('Unexpected error has been occuered.')
            logger.error('Trace', exc_info=True)
            raise SystemExit(e)

        return df


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # Download zip file
    handler = ZipCodeHandler()
    csv = handler.download('13TOKYO.ZIP')

    # Convert CSV to Dataframe with Header
    df = handler.to_dataframe(csv)
    print(df.head())
