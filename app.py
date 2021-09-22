from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import pickle

app = Flask(__name__)

ENV = 'prod'
#this is for localhost
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dhrumil1998@@@localhost/gameApp'
# this one is for the heruko
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wkmpqniejsynrs:cb8e4d066de141ba34aec6df0e1bc47e2d5741383d1e541a9ffb4d9a230c347a@ec2-18-209-143-227.compute-1.amazonaws.com:5432/d52kv5vd4tka5f'
#this is general
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class accounts(db.Model):
    __tablename__ = 'accounts'
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(), unique=True)
    password = db.Column(db.VARCHAR(), unique=False)
    role = db.Column(db.CHAR(1))

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/login',methods=['POST','GET'])
def login():
    nameIN=request.form['username']
    passwordIN=request.form['password']


    #check if username is in the accounts database
    user = accounts.query.filter_by(username=nameIN).first()
    if user:
        if user.password == passwordIN:
            if user.role == 'U':
                return render_template('home.html',name = nameIN, userlevel='user')
            else:
                return render_template('home.html', name=nameIN, userlevel='admin')
        else:
            return render_template('login.html',info='Password incorrect.')
    else:
         return render_template('login.html', info='Account with that username does not exist.')

if __name__ == '__main__':
    app.run()