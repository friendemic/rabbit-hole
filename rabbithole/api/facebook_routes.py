from app import app
from flask import request
import backend.schema
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
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    from_date = dateutil.parser.parse(from_date) if from_date is not None else None
    end_date = dateutil.parser.parse(end_date) if end_date is not None else None
    fb_accounts = fb_accounts.split(',') if fb_accounts is not None else None
    offset = 0 if offset is None else int(offset)
    limit = 100 if limit is None else int(limit)

    return dump_json(filter_items(conn, limit, offset, from_date, end_date, fb_accounts))


