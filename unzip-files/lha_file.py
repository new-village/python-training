""" unzip-files/lha_file.py
Download & unlha files of japanese horse race data from JRDB

"""
import logging
import logging.config
from io import BytesIO, StringIO
from lhafile import Lhafile

import pandas as pd
import requests


class JrdbDataHandler:
    def __init__(self):
        self.ses = requests.Session()
        self.url = 'http://www.jrdb.com/data/Jrdb/'

    def download(self, file):
        try:
            # Get request to japanpost
            url = self.url + file
            res = self.ses.get(url)
            logger.info('Try to get %s' % (url))
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
        unzip = Lhafile(BytesIO(content))

        # Get file name
        fn = [f.filename for f in unzip.infolist()]

        if len(fn) >= 1:
            logger.info('Try to Uncompressing %s' % (fn[0]))
            # Unzip file name from zip file
            csv = unzip.read(fn[0])
        else:
            # Unexpected zipffile structure error
            logger.error('Unexpected Zipfile Structure. There is no TXT or many CSVs.')
            raise SystemExit()

        return csv.decode('ms932')

    def to_dataframe(self, csv):
        try:
            # Read csv file to pandas dataframe
            df = pd.read_csv(StringIO(csv), header=None)
            logger.info('Try to convert csv to dataframe. rows:%s/columns:%s' % df.shape)
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
    handler = JrdbDataHandler()
    csv = handler.download('JRDB040911.lzh')

    # Convert CSV to Dataframe with Header
    df = handler.to_dataframe(csv)
    print(df.head())
