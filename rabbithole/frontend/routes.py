from app import app
from rabbithole_api import RabbitholeApi
import json
import backend.util
import dateutil.parser
from flask import render_template, request

@app.route("/")
def home():
    display_fields = [
        'picture', 'created_date', 'message', 'comments', 'fb_account', 'is_self'
    ];
    api = RabbitholeApi('http://localhost:5000')
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

    response = api.fb_feed(limit, offset, from_date, end_date, fb_accounts)

    return render_template('home/home.html', feed_items=response, fields=display_fields)
