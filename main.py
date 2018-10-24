
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

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Post %r>' % self.title

@app.route('/posts')
def index():
    posts = Post.query.order_by('id desc').all()
    return render_template('main.html', posts=posts)


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


@app.route('/article/<int:id>', methods=["GET","POST"])
def article(id):
    post = Post.query.get(id)
    return render_template("article.html", post = post)

app.run()
