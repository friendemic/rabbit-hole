import config
from facebook.facebook import FacebookUtil, FacebookFeedApi
from schema import update_schema, content_facebook
from facebook.feed_db import insert_update_items
from db import engine, conn

util = FacebookUtil(config.facebook['account_number'],
                    config.facebook['access_token'])

feed = FacebookFeedApi(util, config.facebook['feed_fields'])

update_schema(engine)

for page in feed.feed(100):
    insert_update_items(conn, page)
