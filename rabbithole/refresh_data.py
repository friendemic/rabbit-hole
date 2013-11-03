from backend.config import facebook as facebook_config
from backend.facebook.facebook import FacebookUtil, FacebookFeedApi
from backend.schema import update_schema, content_facebook
from backend.facebook.feed_db import insert_update_items
from backend.db import engine, conn

util = FacebookUtil(facebook_config['account_number'],
                    facebook_config['access_token'])

feed = FacebookFeedApi(util, facebook_config['feed_fields'])

update_schema(engine)

for page in feed.feed(100):
    insert_update_items(conn, page)
