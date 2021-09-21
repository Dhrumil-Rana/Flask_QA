from flask import Flask,request,render_template
import pickle

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("login.html")

#temp "databases" until actual datbase connection is implemented
userdatabase={'test':'123'}
admindatabase={'admin':'admin'}
#or instead of checking 2 different sets of username and passwords, we can check one set and then check which access level the username belongs to

@app.route('/login',methods=['POST','GET'])
def login():
    nameIN=request.form['username']
    passwordIN=request.form['password']

    #check if username is in the user database
    if nameIN in userdatabase:
        if userdatabase[nameIN] != passwordIN:
            return render_template('login.html', info='Password incorrect.')
        else:
            return render_template('home.html',name = nameIN, userlevel='user')
    #check if username is in admin database
    elif nameIN in admindatabase:
        if admindatabase[nameIN]!=passwordIN:
            return render_template('login.html',info='Password incorrect.')
        else:
            return render_template('home.html',name = nameIN, userlevel='admin')

    #username does not exist in any database
    else:
         return render_template('login.html', info='Username does not exist.')

if __name__ == '__main__':
    app.run()