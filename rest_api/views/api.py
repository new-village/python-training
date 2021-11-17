""" api.py
"""
from flask import Blueprint, jsonify
from models import collection, execute, connection
from concurrent import futures
from flask import current_app

api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/<string:city>/<string:year>")
def get(city, year):
    """ Collect and parse race calendar and return JSON
    """
    # TODO: データベースから結果取得
    return jsonify({'city': city, 'year': year}), 200


@api.post("/<string:city>/<string:year>")
def post(city, year):
    """ Collect and parse race calendar and return JSON
    """
    # requests.get でデータ取得
    url = 'https://www.land.mlit.go.jp/webland/api/TradeListSearch?from=' + year + '1&to=' + year + '4&city=' + city
    res = collection(url).to_dict()

    # 取得データのsanitization（加工）
    if res.get('data'):
        data = sanitization(res['data'])
    else:
        # Exception error handling
        current_app.logger.error('Invalid response from ' + url)
        data = {'message': 'Invalid response from ' + url}

    # データベースにデータ投入
    conn = connection()
    conn.upsert(data)

    return jsonify(data), 201


def sanitization(_data):
    result = []
    with futures.ProcessPoolExecutor(max_workers=8) as executor:
        for rec in _data:
            result.append(executor.submit(execute, rec).result())

    return result
