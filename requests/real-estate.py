""" real-estate.py
国土交通省のAPIから東京都の不動産取引価格情報を取得するスクリプト
"""
import os
import sys
import json
import requests

import logging
from logging.config import fileConfig

cd = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(cd + '/config/logging.ini')

def get(_url):
    try:
        res = requests.get(_url)
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
    
    return content

if __name__ == "__main__":
    # loggerの設定の設定
    logger = logging.getLogger(__name__)

    # 東京都の2020年の取引データを取得
    url = 'https://www.land.mlit.go.jp/webland/api/TradeListSearch?from=20201&to=20204&area=13'
    res = get(url)
    for r in res['data']:
        print(r)
    