from flask import Flask, render_template

# creating the app
app = Flask(__name__, template_folder='templates')


@app.route("/", methods=['GET'])
def sign_in():
    return render_template("login.html")


@app.route("/signin", methods=['GET'])
def content():
    return "This is the signin page"


if __name__ == "__main__":
    app.run()