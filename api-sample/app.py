""" app.py
"""
import logging
from concurrent import futures
from datetime import datetime

import uvicorn
from fastapi import BackgroundTasks, FastAPI

from internal import collection, connection, execute

app = FastAPI()
logger = logging.getLogger('uvicorn')


@app.get('/')
def list_trades():
    data = connection().select_all()
    return data


@app.get('/count')
def count_trades():
    cnt = connection().count()
    return {'count': cnt}


@ app.get('/{city_id}/{year}')
async def async_task(city_id: str, year: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(collect_data, city_id, year)
    return {'message': f'The request has been accepted. Accepted Time: {datetime.utcnow()}'}


def collect_data(city_id: str, year: str):
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

    logger.info(f'The request has been successfully completed. {datetime.utcnow()}')


def sanitization(_data):
    result = []
    with futures.ProcessPoolExecutor(max_workers=8) as executor:
        for rec in _data:
            result.append(executor.submit(execute, rec).result())

    return result


if __name__ == '__main__':
    uvicorn.run(app)
