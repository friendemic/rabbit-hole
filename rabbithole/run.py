from api.app import app
from api import facebook_routes

@app.route("/")
def home():
    return "whatever"

if __name__ == "__main__":
    app.run(debug=True)
