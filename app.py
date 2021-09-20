# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask,request,render_template
import pickle

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("login.html")
userdatabase={'test':'123'}
admindatabase={'admin':'admin'}

@app.route('/login_form',methods=['POST','GET'])
def login():
    nameIN=request.form['username']
    passwordIN=request.form['password']
    if nameIN in userdatabase:
        if userdatabase[nameIN] != passwordIN:
            return render_template('login.html', info='Password incorrect.')
        else:
            return render_template('home.html', userlevel='user')
    elif nameIN in admindatabase:
        if admindatabase[nameIN]!=passwordIN:
            return render_template('login.html',info='Password incorrect.')
        else:
            return render_template('home.html',userlevel='admin')
    else:
         return render_template('login.html', info='Username does not exist.')

if __name__ == '__main__':
    app.run()