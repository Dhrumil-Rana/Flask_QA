from flask import Flask, render_template

# creating the app
app = Flask(__name__, template_folder='template/static')


@app.route("/", methods=['GET'])
def sign_in():
    return flask.render_template("login.html")


@app.route("/signin", methods=['GET'])
def content():
    return "This is the signin page"


if name == "__main__":
    app.run()