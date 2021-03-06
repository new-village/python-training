""" crawler.py
This script download data from defined url
"""

import json
import requests
import logging

logger = logging.getLogger('uvicorn')


class collection():
    def __init__(self, url):
        try:
            # Request to URL
            res = requests.get(url)
        except Exception as e:
            # Exception error handling
            logger.error('request is failure: Name, server or service is not known')

        # Response Status Confirmation
        if res.status_code in [200]:
            # Normal
            self.content = res.content.decode()
            logger.info('request to ' + url + ' has been successful')
        else:
            # Abnormal
            logger.error('request to ' + url + ' has been failure:' + str(self.res.status_code))
            logger.error(self.res.content.decode())

    def to_dict(self):
        return json.loads(self.content)
