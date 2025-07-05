from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
import os
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "fallback_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# ---------------- Models ---------------- #

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    tag = db.Column(db.String(50))
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# ---------------- Login Loader ---------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- Routes ---------------- #

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = User(username=request.form['username'], password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registered! Now log in.")
            return redirect(url_for('login'))
        except:
            flash("Username already exists.")
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        title = request.form['title']
        tag = request.form['tag']
        task = Task(title=title, tag=tag, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('dashboard'))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", tasks=tasks)

@app.route('/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.is_done = not task.is_done
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pomodoro')
@login_required
def pomodoro():
    return render_template("pomodoro.html")

@app.route('/stats')
@login_required
def stats():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    total = len(all_tasks)
    completed = len([t for t in all_tasks if t.is_done])
    pending = total - completed
    percent_done = (completed / total * 100) if total else 0

    return render_template("stats.html", total=total, completed=completed, pending=pending, percent_done=percent_done)

# ---------------- Launch ---------------- #

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=10000)
