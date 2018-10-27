
from flask import Flask, request, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
import cgi
import pymysql


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:xnynzn987@localhost:3306/build_blog'
app.config['SQLALCHEMY_ECHO'] = True

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

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def __repr__(self):
        return '<User %r>' % self.username


#--------------------------------------------------
@app.route('/posts')
def posts():
    posts = Post.query.order_by('id desc').all()
    return render_template('main.html', posts=posts)


#--------------------------------------------------
@app.route('/newpost', methods=["GET","POST"])
def newpost():
#   SHOULD not not not DO THIS; I'm just making up for the absence
# of a Post object in the GET
    if request.method == "POST":
        title = request.form['title'].strip()
        article = request.form['article'].strip()
        post = Post(title,article)
        if len(title) > 0 and len(article) > 0:
            db.session.add(post)
            db.session.commit()
            return render_template("article.html", post = post)
        else:
            return render_template('newpost.html', post=post, error=True)
    title=''
    article=''
    dummy_post = Post(title,article)
    return render_template('newpost.html', post=dummy_post, error = False)

#--------------------------------------------------
@app.route('/', methods=["GET","POST"])
def index():
    return  render_template("index.html")


#--------------------------------------------------
@app.route('/login', methods=["GET","POST"])
def login():
    # if valid: put username in session and return /newpost
    # if NOT username: return to /login with error message #1
    # if NOT password: return to /login with error message #2

    return render_template("login.html")

#--------------------------------------------------
@app.route('/logout', methods=["POST"])
def logout():
    return redirect("posts.html")


#--------------------------------------------------
@app.route('/signup', methods=["GET","POST"])
def signup():
    return render_template("signup.html")

#--------------------------------------------------
@app.route('/article/<int:id>', methods=["GET","POST"])
def article(id):
    post = Post.query.get(id)
    return render_template("article.html", post = post)

app.run()
