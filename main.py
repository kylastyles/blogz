from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import flask_sqlalchemy

app=Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:admin' # TODO finish link
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'gddsie934nr9f9rj23jefi'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
#    draft = db.Column(db.Boolean)
#    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body) #owner)
        self.title = title
        self.body = body
#        self.owner = owner

# @app.before_request
# def require login():
#     allowed_routes = ['login', 'register']
#     if request.endpoint not in allowed_routes and 'email' not in session:
#         return redirect('login')

# @app.route('/register', methods=['POST', 'GET'])
# def register():
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
# def logout():
#     del session['email']
#     return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():

    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']

        new_task = request.form['task']
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed=False, owner=owner).all()
    completed_tasks = Task.query.filter_by(completed=True, owner=owner).all()

    return render_template('index.html', title='Build-A-Blog', tasks=tasks, completed_tasks=completed_tasks)

# @app.route('/delete-task', methods=['POST'])
# def delete_task():
#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


if __name__ == "__main__":
    app.run()      