# Rabbithole

Small proof-of-concept for rabbithole in Python.

## Running the backend:

First, edit the `backend/config.py`. Enter appropriate values for the database, your facebook account number, and a valid access\_token.

But, nothing production-ready in here yet (very basic stuff). To go to Facebook, page through all the feed items, and put them in the DB, just run `python backend/test.py`.


## Running the frontend:

Same deal here, extremely basic. `python run.py`, it'll start up using Flask's built-in dev server (believe it listens on localhost:5000 by default)

Only endpoint is fb\_feed.

### fb\_feed

Example:

`fb_feed?from_date=2013-01-01&end_date=2013-10-26&fb_account=1234,2345,3456`

`from_date` and `end_date` are anything that can be parsed by dateutil.parser.parse.

`fb_account` is a comma-separated list of facebook account numbers

