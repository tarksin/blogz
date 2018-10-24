
from flask import Flask, request, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy
import cgi
import pymysql


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:xnynzn987@localhost:3306/build_blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# t_posts = [{'id':1, 'title':'Exploratory data analysis','body': 'Exploratory data analysis (EDA) is the first step in analyzing a dataset.'},
# {'id': 2, 'title':'Features and targets', 'body':'Targets are the dependent variable whose value is attempted to be derived by analysis of the features of the dataset.'},
# {'id':3, 'title':'Central tendency and statistical uncertainty','body':'These two concepts embody the differences between computer scientists and statisticians as they work with data.'}]

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(512))

    # watched = db.Column(db.Boolean)
    # rating = db.Column(db.String(10))
    #
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
        print('------------45 POST-----------')
        title = request.form['title'].strip()
        article = request.form['article'].strip()
        post = Post(title,article)
        if len(title) > 0 and len(article) > 0:
            print('------------49-----------')
            db.session.add(post)
            db.session.commit()
            print('------------53-----------')
            return render_template("article.html", post = post)
        else:
            print('------------55-----------')
            return render_template('newpost.html', post=post, error=True)

    print('------------58 GET-----------')
    title=''
    article=''
    dummy_post = Post(title,article)
    return render_template('newpost.html', post=dummy_post, error = False)


@app.route('/article/<int:id>', methods=["GET","POST"])
def article(id):
    post = Post.query.get(id)
    return render_template("article.html", post = post)



app.run()
