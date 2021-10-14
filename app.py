from flask import Flask,request,render_template,session
from flask_sqlalchemy import SQLAlchemy
import pickle
import bcrypt

app = Flask(__name__)

ENV = 'prod'
select_database = 'almin'

#this is for localhost
if ENV == 'dev':
    app.debug = True
    if select_database == 'dhrumil':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dhrumil1998@@@localhost/gameApp'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:almin123@localhost/flaskwebsite490'
# this one is for the heruko
else:
    app.debug = False
    if select_database == 'dhrumil':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wkmpqniejsynrs:cb8e4d066de141ba34aec6df0e1bc47e2d5741383d1e541a9ffb4d9a230c347a@ec2-18-209-143-227.compute-1.amazonaws.com:5432/d52kv5vd4tka5f'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://onagbacopzfapd:985b15068892b63537c9a10a74d74d6579c45f677b4cba87594a09806e78e14d@ec2-52-23-87-65.compute-1.amazonaws.com:5432/d29sd9q7h5fs67'

#this is general
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='very secret key'
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

class posts(db.Model):
    __tablename__ = 'posts'
    postID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    description = db.Column(db.VARCHAR())
    image = db.Column(db.LargeBinary)

    def __init__(self, postID, userID, description, image):
        self.postID = postID
        self.userID = userID
        self.description = description
        self.image = image


@app.route('/')
def entry():
    return render_template("login.html")


@app.route('/login',methods=['POST','GET'])
def login():
    nameIN = request.form['username']
    passwordIN = request.form['password'].encode('utf-8')

    # check if username is in the accounts database
    user = accounts.query.filter_by(username=nameIN).first()
    if user:
        # compare password given to database hash
        if bcrypt.checkpw(passwordIN, user.password.encode('utf-8')):
            if user.role == 'U':
                session['name']=request.form['username']
                session['userlevel']="user"
                return render_template('home.html', name=nameIN, userlevel='user')
            else:
                session['name']=request.form['username']
                session['userlevel'] = 'admin'
                return render_template('home.html', name=nameIN, userlevel='admin')
        else:
            return render_template('login.html', info='Password incorrect.')
    else:
        return render_template('login.html', info='Account with that username does not exist.')


@app.route('/home', methods=['POST', 'GET'])
def post():
    return render_template('home.html',name=session.get('name'), userlevel=session.get('userlevel'))
# return a list of post and gian has to make a css file such that it will show in sequence


@app.route('/Friends', methods=['POST', 'GET'])
def friend():
    return "This is the Friends page"
#return a list of all the friends


@app.route('/CreatePost', methods=['POST', 'GET'])
def Post():
    if request.method == 'POST':
        return "sent"
    if request.method == 'GET':
        return render_template("createpost.html", title="Create Post",name=session.get('name'), userlevel=session.get('userlevel'))

# gian will add the post through a form post and we will take it and add it to our database
@app.route('/AddAccount', methods=['POST', 'GET'])
def addaccount():
    if request.method == 'POST':
        newuserName = request.form['username']
        passIN = request.form['password']
        newrole = request.form['role']
        newpassword = bcrypt.hashpw(passIN.encode('utf-8'), bcrypt.gensalt())
        user = accounts(username= newuserName, password=newpassword.decode('utf-8'), role=newrole)
        db.session.add(user)
        db.session.commit()
        return newpassword

    if request.method == 'GET':
        return render_template("addaccount.html", title="Create Post", name=session.get('name'),userlevel=session.get('userlevel'))


# we still need to do block post and create user accounts
if __name__ == '__main__':
    app.run()