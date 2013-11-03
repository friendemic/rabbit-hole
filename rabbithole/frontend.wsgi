from frontend.app import app
from frontend.routes import *

if __name__ == "__main__":
    app.run(debug=True, port=5001)
