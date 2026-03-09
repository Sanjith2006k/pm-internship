from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from ai.matcher import match_student
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Role-based access control decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role != role:
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Admin authentication check
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.email != 'admin@gmail.com':
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

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

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    company_name = db.Column(db.String(200))
    gst_number = db.Column(db.String(100))
    domain_email = db.Column(db.String(100))
    linkedin_profile = db.Column(db.String(300))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    verification_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer)  # Use organization_id to match existing DB
    title = db.Column(db.String(200))
    skills_required = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(200), default='Remote')
    duration = db.Column(db.String(100), default='3 months')
    stipend = db.Column(db.String(100))
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_notes = db.Column(db.Text)

# ---------------- LOGIN MANAGER ---------------- #

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template('base.html')


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
        elif user.role == 'organization':
            org = Organization(
                user_id=user.id,
                company_name=request.form.get('company_name', user.name),
                verification_status='not_submitted'
            )
            db.session.add(org)
            db.session.commit()

        # Redirect to login with success message
        return redirect(url_for('login', registered='success'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check hardcoded admin credentials
        if email == 'admin@gmail.com' and password == 'admin123':
            # Create or get admin user
            admin_user = User.query.filter_by(email='admin@gmail.com').first()
            if not admin_user:
                admin_user = User(name='Admin', email='admin@gmail.com', password='admin123', role='admin')
                db.session.add(admin_user)
                db.session.commit()
            login_user(admin_user)
            return redirect(url_for('admin_dashboard'))
        
        # Check regular user
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'organization':
                org = Organization.query.filter_by(user_id=user.id).first()
                # If organization hasn't submitted verification details yet, redirect to submission page
                if org and org.verification_status == 'not_submitted':
                    return redirect(url_for('submit_verification'))
                return redirect(url_for('org_dashboard'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ---------------- STUDENT ---------------- #

@app.route('/student', methods=['GET','POST'])
@login_required
@role_required('student')
def student_dashboard():
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        profile.skills = request.form['skills']
        db.session.commit()

    return render_template('dashboard_student.html', profile=profile)

# ---------------- ORGANIZATION ---------------- #

@app.route('/org/submit-verification', methods=['GET', 'POST'])
@login_required
@role_required('organization')
def submit_verification():
    org = Organization.query.filter_by(user_id=current_user.id).first()
    
    # If already submitted, redirect to dashboard
    if org and org.verification_status != 'not_submitted':
        return redirect(url_for('org_dashboard'))
    
    if request.method == 'POST':
        if org:
            org.gst_number = request.form.get('gst_number')
            org.domain_email = request.form.get('domain_email')
            org.linkedin_profile = request.form.get('linkedin_profile')
            org.industry = request.form.get('industry')
            org.location = request.form.get('location')
            org.description = request.form.get('description')
            org.verification_status = 'pending'
            db.session.commit()
        
        return redirect(url_for('org_dashboard'))
    
    return render_template('org_submit_verification.html', org=org)

@app.route('/organization', methods=['GET','POST'])
@login_required
@role_required('organization')
def org_dashboard():
    org = Organization.query.filter_by(user_id=current_user.id).first()
    
    # If verification not submitted yet, redirect
    if not org or org.verification_status == 'not_submitted':
        return redirect(url_for('submit_verification'))
    
    if request.method == 'POST':
        # Check if organization is verified before posting internship
        if not org or not org.is_verified:
            return jsonify({'status': 'error', 'message': 'Your organization must be verified by admin before posting internships'}), 403
        
        internship = Internship(
            organization_id=org.id if org else current_user.id,
            title=request.form.get('title'),
            skills_required=request.form.get('skills_required'),
            capacity=int(request.form.get('capacity', 1)),
            location=request.form.get('location', 'Remote'),
            duration=request.form.get('duration', '3 months'),
            stipend=request.form.get('stipend')
        )
        db.session.add(internship)
        db.session.commit()

    internships = Internship.query.filter_by(organization_id=org.id if org else current_user.id).all()
    
    stats = {
        'total_applications': 0,
        'shortlisted': 0,
        'selected': 0,
        'avg_match': 0
    }
    
    return render_template('dashboard_org.html', internships=internships, stats=stats, org=org)

@app.route('/org/create-internship', methods=['GET', 'POST'])
@login_required
@role_required('organization')
def create_internship():
    org = Organization.query.filter_by(user_id=current_user.id).first()
    
    # Check if organization is verified
    if not org or not org.is_verified:
        error = "Your organization is pending verification. Our admin team will review your details shortly."
        return render_template('create_internship.html', error=error, org=org)
    
    if request.method == 'POST':
        internship = Internship(
            organization_id=org.id,
            title=request.form.get('title'),
            skills_required=request.form.get('skills_required'),
            capacity=int(request.form.get('capacity', 1)),
            location=request.form.get('location', 'Remote'),
            duration=request.form.get('duration', '3 months'),
            stipend=request.form.get('stipend')
        )
        db.session.add(internship)
        db.session.commit()
        return redirect(url_for('org_dashboard'))
    
    return render_template('create_internship.html', org=org)

@app.route('/org/internship/<int:internship_id>/applications')
@login_required
@role_required('organization')
def org_applications(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    org = Organization.query.filter_by(user_id=current_user.id).first()
    if internship.organization_id != (org.id if org else None):
        return redirect(url_for('org_dashboard'))
    return render_template('view_applications.html', internship=internship)

@app.route('/org/internship/<int:internship_id>/matched-candidates')
@login_required
@role_required('organization')
def org_matched_candidates(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    org = Organization.query.filter_by(user_id=current_user.id).first()
    if internship.organization_id != (org.id if org else None):
        return redirect(url_for('org_dashboard'))
    return render_template('matched_candidates.html', internship=internship)

@app.route('/org/candidate/<int:candidate_id>')
@login_required
@role_required('organization')
def org_candidate_profile(candidate_id):
    candidate = StudentProfile.query.get_or_404(candidate_id)
    return render_template('candidate_profile.html', candidate=candidate)

# ---------------- ADMIN ---------------- #

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    students = StudentProfile.query.all()
    internships = Internship.query.all()
    pending_internships = [
        {
            'internship': i, 
            'org': Organization.query.filter_by(id=i.organization_id).first() if i.organization_id else None
        } 
        for i in internships if i.status == 'pending'
    ]
    
    stats = {
        'total_pending': len([i for i in internships if i.status == 'pending']),
        'total_approved': len([i for i in internships if i.status == 'approved']),
        'total_rejected': len([i for i in internships if i.status == 'rejected'])
    }
    
    return render_template('dashboard_admin.html', students=students, internships=internships, stats=stats, pending_internships=pending_internships)

@app.route('/admin/internship/<int:internship_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_internship(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    notes = request.form.get('notes', '')
    internship.status = 'approved'
    internship.admin_notes = notes
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Internship approved'})

@app.route('/admin/internship/<int:internship_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_internship(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    notes = request.form.get('notes', '')
    internship.status = 'rejected'
    internship.admin_notes = notes
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Internship rejected'})

@app.route('/admin/organization/<int:org_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_organization(org_id):
    org = Organization.query.get_or_404(org_id)
    action = request.form.get('action')  # approve or reject
    notes = request.form.get('notes', '')
    
    if action == 'approve':
        org.is_verified = True
        org.verification_status = 'approved'
    elif action == 'reject':
        org.verification_status = 'rejected'
    org.verification_notes = notes
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Organization {action}d'})

@app.route('/admin/organizations')
@login_required
@admin_required
def admin_organizations():
    pending_orgs = Organization.query.filter_by(verification_status='pending').all()
    return render_template('admin_verify_organizations.html', organizations=pending_orgs)

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)