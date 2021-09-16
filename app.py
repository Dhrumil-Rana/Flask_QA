from flask import Flask

#creating the app
app = Flask(__name__)


@app.route("/")
def home():
    return "This is the homepage"
