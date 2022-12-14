from email.policy import default
from enum import unique
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/todo_app'
app.config['SECRET_KEY'] = 'nzyrw4uZOu8fcuaeruolumiouxizif'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    description = db.Column(db.Text)
    completed = db.Column(db.Integer, default=0)
    comments = db.Column(db.String(255))
    

    # def __init__(self, *args, **kwargs):
    #     super(Todo, self).__init__(*args, **kwargs)
    def __init__(self, task, completed, comments, description):
        self.task = task
        self.completd = completed
        self.description = description
        self.comments = comments
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))    
    email = db.Column(db.String(100), unique=True)  
    password = db.Column(db.String(100))
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        
    # def __init__(self, task, completed, comments, description):
    #     self.task = task
    #     self.completd = completed
    #     self.description = description
    #     self.comments = comments
db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User( 
                        first_name=first_name,
                        last_name=last_name,
                        surname=surname,
                        email=email,
                        password=password)
        
        db.session.add(new_user)
        db.session.commit()
        flash("New User Added Successfully!")
        # msg = 'New User Added Successfully!'
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f_email = request.form['email']
        f_password = request.form['password']
        
        user = User.query.filter(User.email ==f_email, User.password ==f_password).first()
        if user:
            # if f_email == user.email and f_password == user.password:
            return redirect(url_for('dashboard'))
            flash("Login successful")
        return redirect(url_for('login'))
        flash("Incorrect Login Credentials")
        
        return redirect(url_for("register"))
        flash("No account found with that email")
        
    return render_template("login.html")
    
    
    print("login route hit")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
        
@app.route('/todos')
def todos():
    todos = Todo.query.all()
    output_list = []
    for todo in todos:
        output_dict = {
            "task": todo.task,
            "completed" : todo.completed,
            "description" : todo.description,
            "comments" : todo.comments
        }
        
        output_list.append(output_dict)
        
        print(output_list)
    
    return render_template('index.html', todos=output_list)

@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        task = request.form.get('task')
        completed = request.form.get('completed')
        description = request.form.get('description')
        comments = request.form.get('comments')
        
        new_task = Todo(task=task, description=description, comments=comments, completed=completed)
        db.session.add(new_task)
        db.session.commit()
        # message = ("New Task Successfully Created!")
        
        return redirect('/')
    
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 