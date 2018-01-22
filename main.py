from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:admin@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'gddsie934nr9f9rj23jefi'

db = SQLAlchemy(app)

# <-------------------------- CLASSES ------------------------------>

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return self.name

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return self.title

# <---------------------- HELPER FUNCTIONS -------------------------->

def verify(name, password1, password2):
    '''Initially created for user-signup. Edited to remove email parameters.'''
    if name == "":
        flash('Please enter a username', 'error')
        return False
    elif name < 3:
        flash('Name may not be less than three characters.', 'error')
    elif password1 == "":
        flash('Please enter a password', 'error')
        return False
    elif " " in password1:
        flash('No spaces allowed in password field', 'error')
        return False
    elif len(password1) < 3 or len(password1) > 20:
        flash('Password must be between 3-20 characters', 'error')
        return False
    elif password2 == "":
        flash('Please verify your password', 'error')
        return False
    elif password1 != password2:
        flash('Passwords must match', 'error')
        return False
    else:
        return True

# <--------------------------- ROUTES ------------------------------->
@app.before_request
def require_login():
    '''Initially created for get-it-done. Edited for Blogz.'''
    allowed_routes = ['index', 'blog', 'login', 'signup']
    if request.endpoint not in allowed_routes and not session:
        return redirect('/login')

@app.route('/')
def index():
    '''NEW for Blogz. Lists all users.'''
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    '''Initially created for get-it-done. Unedited.'''
    if request.method == 'POST':
        name = request.form['name']
        password1 = request.form['password']
        password2 = request.form['verify']

        if verify(name, password1, password2) == False:
            return render_template('signup.html', name=name)

        existing_user = User.query.filter_by(name=name).first()
        if not existing_user:
            new_user = User(name, password1)
            db.session.add(new_user)
            db.session.commit()
            session['name'] = name
            return redirect('/newpost')
        else:
            flash('Name is already registered', 'error')
    
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    '''Initially created for get-it-done. Unedited.'''
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()

        if user and user.password == password:
            session['name'] = name
            flash('Logged in', 'info')
            return redirect('/newpost')
        else:
             flash('User password incorrect, or user does not exist.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
     del session['name']
     return redirect('/blog')

@app.route('/blog')
def blog():
    '''Created for build-a-blog. Displays previous blog posts.'''

    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    '''Created for build-a-blog. Displays newpost.html and delivers form data to index.html'''
    if not session:
        return redirect('login')

    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']
        owner_name = User.query.filter_by(name=session['name']).first()

        if title == "":
            flash('Please enter a title', 'error')
            return render_template('newpost.html', body=body)
        elif body == "":
            flash("Don't forget to write your blog post!", 'error')
            return render_template('newpost.html', title=title)

        new_blog = Blog(title, body, owner_name)
        db.session.add(new_blog)
        db.session.flush()
        db.session.commit()

        num = new_blog.id
        return redirect('/blogpost?id={0}&owner={1}'.format(num, owner_name))

    return render_template('newpost.html')


@app.route('/blogpost', methods=['POST', 'GET'])
def blogpost():
    '''Created for build-a-blog. Displays individual blog entries as selected by blog.id.'''
    num = request.args.get('id')
    owner = request.args.get('owner')
    blog = Blog.query.filter_by(id=num).first()

    return render_template('blogpost.html', blog=blog)

@app.route('/singleUser')
def singleUser():
    '''NEW for Blogz. Shows all posts from one user.'''
    id = request.args.get('id')
    users_posts = Blog.query.filter_by(owner_id=id).all()
    owner = User.query.filter_by(id=id).first()
    return render_template('singleUser.html', users_posts=users_posts, owner=owner)



if __name__ == "__main__":
    app.run()      