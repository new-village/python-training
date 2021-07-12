""" weather.py
気象庁のAPIから東京都の天気予報を取得するスクリプト
"""
import os
import sys
import json
import requests

import logging
from logging.config import fileConfig

cd = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(cd + '/config/logging.ini')

def main():
    # loggerの設定の設定
    logger = logging.getLogger('GET')

    try:
        # 気象庁のAPIにリクエスト
        url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json'
        res = requests.get(url)
    except Exception as e:
        # リクエストのエラー
        logger.error('request is failure: Name, server or service is not known')
        logger.error(e)
        logger.error('Trace', exc_info=True)
        sys.exit(2)
    else:
        # レスポンスコードのエラーチェック
        if res.status_code in [200]:
            # 正常系
            content = json.loads(res.content.decode())
            print(content)
            logger.info('request to ' + url + ' has been successful')
        else:
            # 異常系
            logger.error('request to ' + url + ' has been failure:' + str(res.status_code))
            logger.error(res.content.decode())
            sys.exit(2)

if __name__ == "__main__":
    main()
