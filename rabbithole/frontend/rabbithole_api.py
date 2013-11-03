import requests
import config
import urlparse
from backend.util import denull_dict, date_format

class RabbitholeApi:

    def __init__(self, url):
        self.url = url

    def get_url(self, path):
        return urlparse.urljoin(self.url, path)

    def get(self, url, addl_params={}, headers={}):
        params = self.get_default_params()
        params.update(addl_params)

        response = requests.get(url, params=params)

        if(response.status_code >= 400):
            print "error, %s" % response.text
            return None

        return response.json()

    def get_default_params(self):
        return {}

    def fb_feed(self, limit=None, offset=None, from_date=None, end_date=None, fb_accounts=None):
        url = self.get_url('fb_feed')
        params = {
            'limit': limit,
            'offset': offset,
            'from_date': date_format(from_date),
            'end_date': date_format(end_date),
            'fb_accounts': fb_accounts
        }

        params = denull_dict(params)

        return self.get(url, params)
