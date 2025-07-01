from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from .models import Accounts, Posts, Comments, Friends, Messages
from . import db
import bcrypt
import requests
import json
from functools import wraps
import base64
from werkzeug.utils import secure_filename
from .utils import allowed_file
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm

app = Blueprint('app', __name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('app.login'))
    return wrap

@app.route('/')
def entry():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    session.pop('userlevel', None)
    return redirect(url_for('app.login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        form = RegistrationForm()
        if 'logged_in' in session:
            if session['logged_in']:
                return redirect(url_for('app.home'))
        return render_template("register.html", title="Register Page", form=form)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'steamid' in request.form:
        form = RegistrationForm(request.form)
        if not form.validate():
            return render_template('register.html', info='Invalid form data')
        allusers = db.session.query(Accounts.username).all()
        newuserName = form.username.data.strip()
        for usernames in allusers:
            if newuserName == usernames[0]:
                return render_template('register.html', info='Username already exists', form=form)
        passIN = form.password.data
        newsteamID = form.steamid.data
        newpassword = bcrypt.hashpw(passIN.encode('utf-8'), bcrypt.gensalt())
        user = Accounts(username=newuserName, password=newpassword.decode('utf-8'), role='U', steamid=newsteamID)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html",form=form, title="Login Page")
    else:
        return redirect(url_for('app.register'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if not form.validate():
            return render_template('login.html', form=form, info='Invalid form data')
        nameIN = form.username.data
        passwordIN = form.password.data
        user = Accounts.query.filter_by(username=nameIN).first()
        if user:
            # Check if the user exists and verify the password
            hashed_password = user.password
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
            if isinstance(passwordIN, str):
                passwordIN = passwordIN.encode('utf-8')
            if bcrypt.checkpw(passwordIN, hashed_password):
                getAllItems = requests.get('https://steamcommunity.com/market/search/render/?appid=730&norender=1&count=5')
                allItems = getAllItems.content
                allItems = json.loads(allItems)
                # get top 5 csgo market items and set for session
                allItems = allItems['results']
                #print(allItems)
                session['top5Items'] = json.loads(json.dumps(allItems, default=str))
                print(f' Top 5 Items in the game: {session["top5Items"]}')
                if user.role == 'U':
                    session['logged_in'] = True
                    session['name'] = nameIN
                    session['userlevel'] = "user"
                    return redirect(url_for('app.home'))
                elif user.role == 'A':
                    session['logged_in'] = True
                    session['name'] = nameIN
                    session['userlevel'] = 'admin'
                    print('The user is an admin, redirecting to home page')
                    return redirect(url_for('app.home'))
                else:
                    print('The user is neither a user nor an admin.')
            else:
                return render_template('login.html',form=form, info='Password incorrect.')
        else:
            return render_template('login.html', form=form, info='Account with that username does not exist.')
    if request.method == 'GET':
        form = LoginForm()
        if 'logged_in' in session:
            if session['logged_in']:
                return redirect(url_for('app.home'))
        return render_template('login.html', form=form)

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    print("User is logged in")
    avatarDictionary = {}
    allUsers = Accounts.query.all()
    print(allUsers)
    for u in allUsers:
        getUserInfo = requests.get("https://backpack.tf/api/users/info/v1?steamids=" + u.steamid + "&key=6183f13deea7b76faf43ee48")
        getUserInfo = getUserInfo.content
        getUserInfo = json.loads(getUserInfo)
        getUserInfo = getUserInfo['users'][u.steamid]['avatar']
        avatarDictionary[u.userid] = getUserInfo
    #print(avatarDictionary)
    if request.method == 'GET':
        print("User is logged in")
        post = Posts.query.all()
        commentlist = Comments.query.all()
        user = Accounts.query.all()
        #print(f'Nav market items: {session.get("top5Items")}')
        return render_template('home.html', name=session.get('name'), userlevel=session.get('userlevel'), posts=post, comments=commentlist, users=user, navMarketItems=session.get('top5Items'), myDict=avatarDictionary)

    if request.method == 'POST':
        if 'block' in request.form:
            blockpostID = request.form['postID']
            blockpost = Posts.query.filter_by(postID=blockpostID).first()
            blockpost.blocked = 'true'
            db.session.commit()

        if 'comment' in request.form:
            userid = db.session.query(Accounts.userid).filter_by(username=session.get('name')).first()
            commenttext = request.form['comment_input']
            postID = request.form['postID']
            commentSEND = Comments(textComment=commenttext, commenterID=userid, postID=postID)
            db.session.add(commentSEND)
            db.session.commit()
        return redirect('app.home')

@app.route('/CreatePost', methods=['POST', 'GET'])
@login_required
def create_post():
    def render_picture(data):
        return base64.b64encode(data).decode('ascii')

    if request.method == 'POST':
        account = Accounts.query.filter_by(username=session.get('name')).first()
        userid = account.userid
        blocked = "false"

        if 'usertext' not in request.form or not request.form['usertext']:
            flash('Post requires text')
            return redirect(request.url)

        usertext = request.form['usertext']

        image = request.files.get('img')
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            mimetype = image.mimetype
            image_data = image.read()
            rendered_data = render_picture(image_data)
            post = Posts(userid=userid, image=rendered_data, description=usertext,
                         filename=filename, mimetype=mimetype, blocked=blocked)
        else:
            post = Posts(userid=userid, image=None, filename=None, mimetype=None,
                         description=usertext, blocked=blocked)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('app.home'))

    if request.method == 'GET':
        return render_template("createpost.html",
                              title="Create Post",
                              name=session.get('name'),
                              userlevel=session.get('userlevel'),
                              navMarketItems=session.get('top5Items'))