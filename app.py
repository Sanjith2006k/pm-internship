from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from ai.matcher import match_student

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ---------------- DATABASE MODELS ---------------- #

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # student, organization, admin

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    skills = db.Column(db.Text)
    allocated_internship = db.Column(db.String(200))
    match_score = db.Column(db.Float)

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    skills_required = db.Column(db.Text)
    capacity = db.Column(db.Integer)

# ---------------- LOGIN MANAGER ---------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            role=request.form['role']
        )
        db.session.add(user)
        db.session.commit()

        if user.role == 'student':
            profile = StudentProfile(user_id=user.id, skills="")
            db.session.add(profile)
            db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'organization':
                return redirect(url_for('org_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ---------------- STUDENT ---------------- #

@app.route('/student', methods=['GET','POST'])
@login_required
def student_dashboard():
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        profile.skills = request.form['skills']
        db.session.commit()

    return render_template('dashboard_student.html', profile=profile)

# ---------------- ORGANIZATION ---------------- #

@app.route('/organization', methods=['GET','POST'])
@login_required
def org_dashboard():
    if request.method == 'POST':
        internship = Internship(
            title=request.form['title'],
            skills_required=request.form['skills_required'],
            capacity=int(request.form['capacity'])
        )
        db.session.add(internship)
        db.session.commit()

    internships = Internship.query.all()
    return render_template('dashboard_org.html', internships=internships)

# ---------------- ADMIN ---------------- #

@app.route('/admin')
@login_required
def admin_dashboard():
    students = StudentProfile.query.all()
    internships = Internship.query.all()
    return render_template('dashboard_admin.html', students=students, internships=internships)

@app.route('/run_allocation')
@login_required
def run_allocation():
    students = StudentProfile.query.all()
    internships = Internship.query.all()

    for student in students:
        results = match_student(student.skills, internships)
        if results:
            best_match, score = results[0]
            student.allocated_internship = best_match.title
            student.match_score = score

    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)