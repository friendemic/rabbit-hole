# Rabbithole

Small proof-of-concept for rabbithole in Python.

## Installation

Uses a pip requirements.txt. So long as you have python-dev and libmysqlclient installed, `pip install -r requirements.txt` should work just fine. I'd suggest doing that in a virtualenv, though:

    cd /path/to/rabbit-hole
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

Installing the frontend / backend using Apache is slightly more complicated. Basically, do something like this:

    <VirtualHost *:5000>
        ServerName backend.friendemic.com

        WSGIDaemonProcess rabbithole_backend user=ubuntu group=ubuntu threads=5 \
            python-path=/home/ubuntu/src/rabbit-hole/venv/lib/python2.7/site-packages
        WSGIScriptAlias / /home/ubuntu/src/rabbit-hole/rabbithole/backend.wsgi

        <Directory /home/ubuntu/src/rabbit-hole/rabbithole>
            WSGIProcessGroup rabbithole_backend
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

There are backend.wsgi and frontend.wsgi for the different applications. Pay attention to the `python-path` element there, it has to point to the site-packages in your virtualenv.

And, of course, make sure you add `Listen 5000` (or whatever port you chose) to /etc/apache2/ports.conf. The frontend installation is pretty much the same, with a different process name and script alias (also, probably listening on 80)

## Running the backend:

First, edit the `backend/config.py`. Enter appropriate values for the database, your facebook account number, and a valid access\_token.

But, nothing production-ready in here yet (very basic stuff). To go to Facebook, page through all the feed items, and put them in the DB, just run `python rabbithole/refresh_data.py` (don't forget to activate your virtualenv, if you used one during installation).


## Running the frontend:

Edit `frontend/config.py` with the url and port you configured for the backend in Installation in the variable named `backend_url`. Use the apache installation outlined above, or do `python rabbithole/run_frontend.py`, it'll start up using Flask's built-in dev server (believe it listens on localhost:5000 by default)

Only endpoint is fb\_feed.

### fb\_feed

Example:

`fb_feed?from_date=2013-01-01&end_date=2013-10-26&fb_account=1234,2345,3456&limit=10&offset=10`

`from_date` and `end_date` are anything that can be parsed by dateutil.parser.parse.

`fb_account` is a comma-separated list of facebook account numbers

`limit` and `offset` are obvious.

