""" app.py
"""
import uvicorn
import logging
from concurrent import futures
from fastapi import FastAPI
from pydantic import BaseModel
from internal import collection, execute, connection

app = FastAPI()
logger = logging.getLogger('uvicorn')

@app.get('/')
def search_trades():
    return {'details': 'This site is api of real estate collection based on mlti.'}


@app.get('/{city_id}/{year}')
def get_estate_trades(city_id: str, year: str):
    # requests.get でデータ取得
    url = 'https://www.land.mlit.go.jp/webland/api/TradeListSearch?from=' + year + '1&to=' + year + '4&city=' + city_id
    res = collection(url).to_dict()

    # 取得データのsanitization（加工）
    if res.get('data'):
        data = sanitization(res['data'])
    else:
        # Exception error handling
        logger.error('Invalid response from ' + url)
        data = {'message': 'Invalid response from ' + url}

    # データベースにデータ投入
    conn = connection()
    conn.upsert(data)

    return data


def sanitization(_data):
    result = []
    with futures.ProcessPoolExecutor(max_workers=8) as executor:
        for rec in _data:
            result.append(executor.submit(execute, rec).result())

    return result


if __name__ == '__main__':
    uvicorn.run(app)