""" package.py
パッケージ化の練習スクリプト
"""
import os
import json
import requests
import logging
import sanitizer
from logging.config import fileConfig
from concurrent import futures


def sanitization(_data):
    result = []
    with futures.ProcessPoolExecutor(max_workers=8) as executor:
        for rec in _data:
            result.append(executor.submit(sanitizer.execute, rec).result())

    return result


if __name__ == "__main__":
    # loggerの設定の設定
    cd = os.path.dirname(os.path.abspath(__file__))
    logging.config.fileConfig(cd + '/config/logging.ini')
    logger = logging.getLogger(__name__)

    # requests.get でデータ取得
    url = 'https://www.land.mlit.go.jp/webland/api/TradeListSearch?from=20201&to=20201&city=13106'
    res = requests.get(url)
    res = json.loads(res.content.decode())

    # 取得データのsanitization（加工）
    data = sanitization(res['data'])

    # データベースにデータ投入
    print(data)
