import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from api.app import app as application
from api import facebook_routes

application.debug = True

if __name__ == "__main__":
    app.run(debug=True)
