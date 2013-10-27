from app import app
from flask import request
from backend.util import dump_json
from backend.facebook.feed_db import filter_items
from backend.db import conn
from datetime import datetime
import dateutil.parser

@app.route("/fb_feed")
def fb_feed():
    from_date = request.args.get('from_date')
    end_date = request.args.get('end_date')
    fb_accounts = request.args.get('fb_accounts')

    if from_date is not None:
        from_date = dateutil.parser.parse(from_date)

    if end_date is not None:
        end_date = dateutil.parser.parse(end_date)

    if fb_accounts is not None:
        fb_accounts = fb_accounts.split(',')

    return "<pre>" + dump_json(filter_items(conn, from_date, end_date, fb_accounts)) + "</pre>"


