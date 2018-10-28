
from flask import Flask, request, redirect, render_template, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import pymysql


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:xnynzn987@localhost:3306/build_blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'afb9f6e868924eb4a14dba93aea625cc'

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(512))
    time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Post %r>' % self.title

#--------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(512))
    posts = db.relationship('Post', backref='owner')

    def __init__(self, username,  password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


#--------------------------------------------------
@app.before_request
def require_login():
    allowed_routes = [ 'login', 'signup' ,'posts', 'users']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#--------------------------------------------------
@app.route('/posts')
def posts():
    id = request.args.get('id')
    if id:
        posts = Post.query.filter_by(owner_id=int(id)).order_by('time_created desc').all()
    else:
        posts = Post.query.order_by('id desc').all()

    return render_template('main.html', posts=posts)

#--------------------------------------------------
@app.route('/')
def index():
    return  redirect(url_for('posts'))

#--------------------------------------------------
@app.route('/index')
def users():
    users = User.query.order_by('username').all()
    return render_template('index.html', users=users)

#--------------------------------------------------
@app.route('/newpost', methods=["GET","POST"])
def newpost():
    if request.method == "POST":
        title = request.form['title'].strip()
        article = request.form['article'].strip()

        owner = User.query.filter_by(username=session['username']).first()

        post = Post(title,article,owner)
        if len(title) > 0 and len(article) > 0:
            db.session.add(post)
            db.session.commit()
            return render_template("article.html", post = post)
        else:
            flash("Include a title and a body for the post","error")
            return render_template('newpost.html', post=post)
    return render_template('newpost.html')


#--------------------------------------------------
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":

        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        user = User.query.filter_by(username=username).first()

        if user and user.password == password: # the username is in the d/b
            session["username"]=username
            session['user_id']=user.id
            return redirect("/newpost")
        elif not user:  # not even the username in the d/b
            flash("User name not found. Sign up to create an account.","error")
            return redirect('/login')
        else: # username, but wrong p/w: render_template gives a way to pass back the [correct] username
            flash("Invalid password","error")
            return render_template('login.html',username=username)

    return render_template("login.html")

#--------------------------------------------------
@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    if 'user_id' in session:
        del session['user_id']

    return redirect("posts")

#--------------------------------------------------
@app.route('/signup', methods=["GET","POST"])
def signup():

    if request.method == "POST":
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        verify = request.form['verify'].strip()

        if not (len(username) > 2 and len(password) > 2):
            flash("Username and password must be more than two characters", "error")
            return render_template("/signup.html", username=username)

        if password == verify:

            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect("/newpost")
            else:
                flash("The user is already registered.",  "error")
                return render_template("/signup.html" )
        else:
            flash("Passwords must match", "error")
            return render_template("/signup.html", username=username)
    return render_template("/signup.html" )

#--------------------------------------------------
@app.route('/article/<int:id>', methods=["GET","POST"])
def article(id):
    post = Post.query.get(id)
    return render_template("article.html", post = post)


app.run()
