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
    uID = db.Column(db.Integer, db.ForeignKey('accounts.userID'), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    rendered_image = db.Column(db.Text, nullable=True)
    comID = db.Column(db.Integer, db.ForeignKey('comments.commentID'), nullable=False)

    def __init__(self, uID, image, rendered_image, comID):
        self.uID = uID
        self.image = image
        self.rendered_image = rendered_image
        self.comID = comID


class comments(db.Model):
    __tablename__ = 'comments'
    commentID = db.Column(db.Integer, primary_key=True)
    commenterID = db.Column(db.Integer, db.ForeignKey('accounts.userID'), nullable=False)
    textComment = db.Column(db.VARCHAR(), nullable=False)
    postID = db.Column(db.Integer, db.ForeignKey(posts.postID), nullable=False)

    def __init__(self, commenterID, textComment, postID):
        self.commenterID = commenterID
        self.textComment = textComment
        self.postID = postID

class friends(db.Model):
    __tablename__ = 'friends'
    Number = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    friendID = db.Column(db.Integer, db.ForeignKey('accounts.userID'), nullable=False)

    def __init__(self, userID, friendID):
        self.userID = userID
        self.friendID = friendID

class message(db.Model):
    __tablename__ = 'message'
    msgID = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, nullable=False)
    receiverID = db.Column(db.Integer, nullable=False)
    msg = db.Column(db.VARCHAR, nullable=False)

    def __init__(self, senderID, receiverID, msg):
        self.senderID = senderID
        self.receiverID = receiverID
        self.msg = msg

@app.route('/')
def entry():
    return render_template("login.html")


@app.route('/login',methods=['POST', 'GET'])
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
    #getting userid then getting friends and filling friendlist
    user= db.session.query(accounts.userID).filter_by(username=session.get('name')).first()
    friendIDlist=db.session.query(friends.friendID).filter_by(userID=user)
    friendlist = []
    for friendID in friendIDlist:
        f = db.session.query(accounts.username).filter_by(userID=friendID).first()
        friendlist.append(f)
    # getting userid then getting friends and filling friendlist
    print(friendlist)
    return render_template("friends.html",friends=friendlist, title="Friends", name=session.get('name'), userlevel=session.get('userlevel') )
#return a list of all the friends

@app.route('/messanger/<friendname>', methods=['POST', 'GET'])
def messanger(friendname):
    sender = session.get('name')
    friendsID = db.session.query(accounts.userID).filter_by(username=friendname).first()  #receiver
    usersID = db.session.query(accounts.userID).filter_by(username=session.get('name')).first() #sender or current user

    sentmsgs = db.session.query(message.msgID,message.msg).filter_by(senderID=usersID,receiverID=friendsID).all() #msgs sent by the current user to friend
    receivedmsgs = db.session.query(message.msgID,message.msg).filter_by(senderID=friendsID,receiverID=usersID).all() #msgs sent by friend to current user

    if request.method == 'POST':
        msgToSend = request.form['sendmessage']
        messageSEND = message(msg=msgToSend, senderID=usersID, receiverID=friendsID)
        db.session.add(messageSEND)
        db.session.commit()
        return render_template("messanger.html", title="Messanger", msgsSent=sentmsgs, msgsReceived=receivedmsgs, friend=friendname, name = session.get('name'), userlevel = session.get('userlevel') )

    if request.method == 'GET':
        return render_template("messanger.html", title="Messanger", msgsSent=sentmsgs, msgsReceived=receivedmsgs, friend=friendname, name=session.get('name'), userlevel=session.get('userlevel') )


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
        return render_template("addaccount.html", title="Add Account", name=session.get('name'),userlevel=session.get('userlevel'))


# we still need to do block post and create user accounts
if __name__ == '__main__':
    app.run()