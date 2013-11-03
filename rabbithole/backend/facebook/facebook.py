import requests
import urlparse
import dateutil.parser
import json
from ..config import facebook as facebook_config


class FacebookUtil:

    """Class for low-level access to the Facebook graph api"""

    base_url = 'https://graph.facebook.com'

    def __init__(self, account_number, access_token):
        self.account_number = account_number
        self.access_token = access_token

    def get_url(self, path):
        return urlparse.urljoin(self.base_url, path)

    def get_user_url(self, path):
        return self.get_url("%s/%s" % (self.account_number, path))

    def get_default_params(self):
        return {'access_token': self.access_token}

    def get(self, url, addl_params={}, headers={}):
        params = self.get_default_params()
        params.update(addl_params)

        print "making request to %s, with params %s" % (url, params)

        response = requests.get(url, params=params)

        print "request done"

        if(response.status_code >= 400):
            print "error, %s" % response.text
            return None

        return response.json()


class FacebookFeedApi:

    """Simplified access to the Feed api

       util is a FacebookUtil

       fields are formatted for use in the JsonParser, see that class for
       format documentation

       page_size is the size of the page to request from the facebook feed api
    """

    def __init__(self, util, fields, page_size=100):
        self.util = util
        self.fields = fields
        self.page_size = page_size

    def get_base_url(self):
        return self.util.get_user_url("feed")

    def feed(self, page_size=None):

        """Pages through the feed, yielding each page
        to the caller.

        i.e., you can do something like:
            for page in feed:
                do_stuff_with_page()
        """

        if(page_size is None):
            page_size = self.page_size

        url = self.get_base_url()

        while url is not None:
            response_data = self.util.get(url, {'limit': page_size})

            paging = response_data.get("paging")
            url = None if paging is None else paging.get("next")

            yield self.parse_feed(response_data.get('data'))

    def parse_feed(self, feed_json):

        """Instantiates a JsonParser with the fields defined for this
        object, and parses all the items in the provided dict
        """

        parser = JsonParser(self.fields)
        return [parser.parse(item) for item in feed_json]


class JsonParser:

    """Responsible for parsing an arbitrary array of dicts, based on
    some definition.

    Field definitions:
        {
            # Just grab the field 'id' out of the dict, and put it in the
            # field named 'id'
            'id': None,

            # Traverse into the 'from' collection in the dict, grab
            # the 'id' element from it, and assign it to the field named
            # 'fb_account'
            'fb_account': {
                'descent': ['from', 'id']
            },

            # Count the number of elements in the 'comments' collection
            'comments': {
                'action': 'len'
            },

            # Grab the field named 'status_type' out of the dict, and put it
            # in the field named 'status'
            'status': {
                'field_name': 'status_type'
            },

            # Sorta hackish, but determines whether the current item was posted
            # by the facebook account accessing the api. Puts boolean True or
            # False in the field named 'self', compares directly to the config.
            'self': {
                'action': 'is_self'
            },

            # Also a bit hackish, gets the full JSON for the current item, and
            # puts it in the field 'data'
            'data': {
                'action': 'full_item_text',
            }
        }
    """

    def __init__(self, fields):
        self.fields = fields

    def resolve(self, item, field_name, field_def=None):
        if field_def is None:
            return item.get(field_name)

        else:
            return self.resolve_complex(item, field_name, field_def)

    def resolve_complex(self, item, field_name, field_def):
        """Gets data from the item (either through 'descent', 'field_name',
        or presumed field name), performs any defined actions, and potentially
        handles it based on the 'type' element (only 'datetime' implemented for
        now)
        """

        if 'descent' in field_def:
            resolved_item = self.resolve_descent(item,
                                                 field_def['descent'])
        else:
            if 'field_name' in field_def:
                resolved_item = item.get(field_def['field_name'])
            else:
                resolved_item = item.get(field_name)

        if 'action' in field_def:
            resolved_item = self.resolve_action(item,
                                                resolved_item,
                                                field_def['action'])

        if field_def.get('type') == 'datetime':
            try:
                resolved_item = dateutil.parser.parse(resolved_item)
            except ValueError as ex:
                resolved_item = None

        return resolved_item

    def resolve_descent(self, item, descent):
        resolved = item

        for component in descent:
            resolved = resolved.get(component)

            if resolved is None:
                return None

        return resolved

    def resolve_action(self, item, resolved_item, action):

        if action is 'len':
            return 0 if resolved_item is None else len(resolved_item)
        if action is 'is_self':
            return self.resolve_descent(item, ['from', 'id']) == facebook_config['account_number']
        if action is 'full_item_text':
            return json.dumps(item)

        return None

    def parse(self, item):
        parsed_item = {}
        for field in self.fields.keys():
            field_def = self.fields.get(field)
            parsed_item[field] = self.resolve(item, field, field_def)

        return parsed_item
