from . import db

class Accounts(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': 'Gamedb'}
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    steamid = db.Column(db.String(50), nullable=True)

    def __init__(self, username, password, role, steamid=None):
        self.username = username
        self.password = password
        self.role = role
        self.steamid = steamid

class Posts(db.Model):
    __tablename__ = 'posts'
    __table_args__ = {'schema': 'Gamedb'}
    postid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('Gamedb.accounts.userid'), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    description = db.Column(db.String(100), nullable=True)
    blocked = db.Column(db.String(50), nullable=True)
    mimetype = db.Column(db.String(50), nullable=True)
    filename = db.Column(db.String(50), nullable=True)

    def __init__(self, userid, image=None, description=None, blocked=None, mimetype=None, filename=None):
        self.userid = userid
        self.image = image
        self.description = description
        self.blocked = blocked
        self.mimetype = mimetype
        self.filename = filename

class Comments(db.Model):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'Gamedb'}
    commentid = db.Column(db.Integer, primary_key=True)
    commenterid = db.Column(db.Integer, db.ForeignKey('Gamedb.accounts.userid'), nullable=False)
    textcomment = db.Column(db.String(100), nullable=False)
    postid = db.Column(db.Integer, db.ForeignKey('Gamedb.posts.postid'), nullable=False)

    def __init__(self, commenterid, textcomment, postid):
        self.commenterid = commenterid
        self.textcomment = textcomment
        self.postid = postid

class Friends(db.Model):
    __tablename__ = 'friends'
    __table_args__ = {'schema': 'Gamedb'} 
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('Gamedb.accounts.userid'), nullable=False)
    friendid = db.Column(db.Integer, db.ForeignKey('Gamedb.accounts.userid'), nullable=False)

    def __init__(self, userid, friendid):
        self.userid = userid
        self.friendid = friendid

class Messages(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {'schema': 'Gamedb'}
    msgid = db.Column(db.Integer, primary_key=True)
    senderid = db.Column(db.Integer, db.ForeignKey('Gamedb.accounts.userid'), nullable=False)
    reciverid = db.Column(db.Integer, db.ForeignKey('Gamedb.accounts.userid'), nullable=False)
    msg = db.Column(db.String(100), nullable=False)

    def __init__(self, senderid, reciverid, msg):
        self.senderid = senderid
        self.reciverid = reciverid
        self.msg = msg