""" api.py
This script download weather information in Tokyo from the Japan Meteorological Agency API
"""
import json
import requests
import logging
import logging.config


def collector():
    try:
        # Request jma api
        url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json'
        res = requests.get(url)
    except Exception as e:
        # Exception error handling
        logger.error('request is failure: Name, server or service is not known')
        logger.error('Trace', exc_info=True)
        raise SystemExit(e)

    # Response Status Confirmation
    if res.status_code in [200]:
        # Normal
        content = json.loads(res.content.decode())
        logger.info('request to ' + url + ' has been successful')
    else:
        # Abnormal
        logger.error('request to ' + url + ' has been failure:' + str(res.status_code))
        logger.error(res.content.decode())
        raise SystemExit()

    return content


if __name__ == "__main__":
    # Load logger config & Set Logger
    logging.config.fileConfig('./config/logging.ini')
    logger = logging.getLogger()

    # Download ZIP File Strings
    res = collector()
    print(json.dumps(res, indent=2, ensure_ascii=False))
