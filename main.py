from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:admin@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'gddsie934nr9f9rj23jefi'

db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120),unique=True)
#     password = db.Column(db.String(120))
#     blogs = db.relationship('Blog', backref='owner')

#     def __init__(self, email, password):
#         self.email = email
#         self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
#    draft = db.Column(db.Boolean)
    # owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body


# @app.before_request
# def require login():
'''Initially created for get-it-done. Unedited.'''
#     allowed_routes = ['login', 'register']
#     if request.endpoint not in allowed_routes and 'email' not in session:
#         return redirect('login')

# @app.route('/register', methods=['POST', 'GET'])
# def register():
'''Initially created for get-it-done. Unedited.'''
#     if request.method == 'POST':
#         email = request.form['email']
#         password1 = request.form['password']
#         password2 = request.form['verify']

#         if verify(email, password1, password2) == False:
#             return render_template('register.html')

#         existing_user = User.query.filter_by(email=email).first()
#         if not existing_user:
#             new_user = User(email, password1)
#             db.session.add(new_user)
#             db.session.commit()
#             session['email'] = email
#             return redirect('/')
#         else:
#             flash('Email is already registered', 'error')
    
#     return render_template('register.html')

# def verify(email, password1, password2):
'''Initially created for user-signup. Unedited. No regex.'''
#     if email == "":
#         flash('Please register with your email address', 'error')
#         return False
#     elif "@" not in email or "." not in email or " " in email or len(email) < 7:
#         flash('Please enter a valid email', 'error')
#         return False
#     elif password1 == "":
#         flash('Please enter a password', 'error')
#         return False
#     elif " " in password1:
#         flash('No spaces allowed in password field', 'error')
#         return False
#     elif len(password1) < 3 or len(password1) > 20:
#         flash('Password must be between 3-20 characters', 'error')
#         return False
#     elif password2 == "":
#         flash('Please verify your password', 'error')
#         return False
#     elif password1 != password2:
#         flash('Passwords must match', 'error')
#         return False
#     else:
#         return True

# @app.route('/login', methods=['POST', 'GET'])
'''Initially created for get-it-done. Unedited.'''
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()

#         if user and user.password == password:
#             session['email'] = email
#             flash('Logged in', 'info')
#             return redirect('/')
#         else:
#             flash('User password incorrect, or user does not exist.', 'error')
#     return render_template('login.html')

# @app.route('/logout')
'''Initially created for get-it-done. Unedited.'''
# def logout():
#     del session['email']
#     return redirect('/')

@app.route('/')
def index():
    '''New for build-a-blog. Displays previous blog posts.'''

    # owner = User.query.filter_by(email=session['email']).first()
    blogs = Blog.query.all()

    return render_template('index.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    '''New for build-a-blog. Displays newpost.html and delivers form data to index.html'''
    if request.method == 'POST':
        title = request.form['blog-title']
        body = request.form['blog-body']

        if title == "":
            flash('Please enter a title', 'error')
            return render_template('newpost.html', body=body)
        elif body == "":
            flash("Don't forget to write your blog post!", 'error')
            return render_template('newpost.html', title=title)

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.flush()
        db.session.commit()
        return redirect('/')

    return render_template('newpost.html')

# @app.route('/delete-task', methods=['POST'])
# def delete_task():
'''Initially created for get-it-done. Unedited.'''
#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


if __name__ == "__main__":
    app.run()      