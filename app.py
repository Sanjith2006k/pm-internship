from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from ai.matcher import match_student
from functools import wraps
from datetime import datetime, timedelta
import smtplib, random, string, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Email config – set MAIL_USERNAME / MAIL_PASSWORD as environment variables
app.config['MAIL_SERVER']   = 'smtp.gmail.com'
app.config['MAIL_PORT']     = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')


def send_otp_email(to_email, otp):
    """Send a 6-digit OTP to the given address via Gmail SMTP."""
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    if not username or not password:
        print("MAIL_USERNAME / MAIL_PASSWORD not set – OTP:", otp)
        return True          # dev fallback: skip send, OTP printed to console

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'InternAI – Admin Password Change OTP'
    msg['From']    = username
    msg['To']      = to_email

    html = f"""
    <html><body>
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;padding:32px;">
      <h2 style="color:#001a40;margin-bottom:4px;">Password Change Verification</h2>
      <p style="color:#555;font-size:14px;">You requested to change your InternAI admin password.</p>
      <div style="background:#eff6ff;border:2px solid #1e7ce8;border-radius:10px;
                  padding:24px;text-align:center;margin:24px 0;">
        <p style="margin:0 0 6px;font-size:13px;color:#555;">Your One-Time Password</p>
        <h1 style="margin:0;color:#1e7ce8;letter-spacing:10px;font-size:38px;font-weight:800;">
          {otp}
        </h1>
        <p style="margin:10px 0 0;font-size:12px;color:#888;">Valid for 10 minutes</p>
      </div>
      <p style="color:#888;font-size:12px;">If you didn't request this, you can safely ignore this email.</p>
    </div>
    </body></html>
    """
    msg.attach(MIMEText(html, 'html'))
    try:
        server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(username, password)
        server.sendmail(username, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False

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
        if not current_user.is_authenticated or current_user.role != 'admin':
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

class StudentPortfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, index=True, nullable=False)
    linkedin_url = db.Column(db.String(300))
    github_url = db.Column(db.String(300))
    resume_path = db.Column(db.String(400))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StudentCertificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    certificate_name = db.Column(db.String(200), nullable=False)
    issuing_organization = db.Column(db.String(200), nullable=False)
    issue_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    certificate_file_path = db.Column(db.String(400))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudentInternshipExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(200))
    stipend = db.Column(db.String(100))
    skills_used = db.Column(db.Text)
    work_description = db.Column(db.Text)
    proof_file_path = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    status = db.Column(db.String(50), default='approved')  # approved by default once org is verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_notes = db.Column(db.Text)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)   # StudentProfile.id
    internship_id = db.Column(db.Integer)
    status = db.Column(db.String(50), default='pending')  # pending, approved, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

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
                if org and org.verification_status == 'not_submitted':
                    return redirect(url_for('submit_verification'))
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

@app.route('/student', methods=['GET', 'POST'])
@login_required
@role_required('student')
def student_dashboard():
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    portfolio = StudentPortfolio.query.filter_by(user_id=current_user.id).first()
    certificates = StudentCertificate.query.filter_by(user_id=current_user.id).order_by(StudentCertificate.created_at.desc()).all()
    internship_experiences = StudentInternshipExperience.query.filter_by(user_id=current_user.id).order_by(StudentInternshipExperience.created_at.desc()).all()
    available_internships = Internship.query.filter_by(status='approved').all()
    applications = Application.query.filter_by(student_id=profile.id).all() if profile else []
    applied_ids = {a.internship_id for a in applications}
    orgs = {o.id: o for o in Organization.query.all()}
    # Enrich applications with internship info
    enriched_applications = []
    for app_obj in applications:
        intern = Internship.query.get(app_obj.internship_id)
        org = orgs.get(intern.organization_id) if intern else None
        enriched_applications.append({'application': app_obj, 'internship': intern, 'org': org})
    return render_template(
        'dashboard_student.html',
        profile=profile,
        portfolio=portfolio,
        certificates=certificates,
        internship_experiences=internship_experiences,
        user=current_user,
        available_internships=available_internships,
        enriched_applications=enriched_applications,
        applied_ids=applied_ids,
        orgs=orgs,
        total_available=len(available_internships),
        total_applied=len(applications),
    )

@app.route('/student/apply/<int:internship_id>', methods=['POST'])
@login_required
@role_required('student')
def apply_internship(internship_id):
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        return jsonify({'status': 'error', 'message': 'Profile not found'})
    existing = Application.query.filter_by(student_id=profile.id, internship_id=internship_id).first()
    if existing:
        return jsonify({'status': 'error', 'message': 'Already applied'})
    application = Application(student_id=profile.id, internship_id=internship_id)
    db.session.add(application)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Application submitted successfully!'})

@app.route('/student/withdraw/<int:application_id>', methods=['POST'])
@login_required
@role_required('student')
def withdraw_application(application_id):
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    app_obj = Application.query.filter_by(id=application_id, student_id=profile.id).first()
    if not app_obj:
        return jsonify({'status': 'error', 'message': 'Application not found'})
    if app_obj.status != 'pending':
        return jsonify({'status': 'error', 'message': 'Only pending applications can be withdrawn'})
    db.session.delete(app_obj)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Application withdrawn'})

@app.route('/student/profile', methods=['POST'])
@login_required
@role_required('student')
def update_student_profile():
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    portfolio = StudentPortfolio.query.filter_by(user_id=current_user.id).first()
    if not portfolio:
        portfolio = StudentPortfolio(user_id=current_user.id)
        db.session.add(portfolio)

    current_user.name = request.form.get('name', current_user.name).strip()
    profile.skills = request.form.get('skills', '').strip()

    portfolio.linkedin_url = request.form.get('linkedin_url', '').strip() or None
    portfolio.github_url = request.form.get('github_url', '').strip() or None

    resume_file = request.files.get('resume_file')
    if resume_file and resume_file.filename:
        if _is_allowed_upload(resume_file.filename, {'pdf', 'doc', 'docx'}):
            portfolio.resume_path = _save_student_file(resume_file, current_user.id, 'resume')

    db.session.commit()
    return redirect(url_for('student_dashboard') + '?section=profile&saved=1')

@app.route('/student/certificate', methods=['POST'])
@login_required
@role_required('student')
def add_student_certificate():
    certificate_name = request.form.get('certificate_name', '').strip()
    issuing_organization = request.form.get('issuing_organization', '').strip()
    if not certificate_name or not issuing_organization:
        return redirect(url_for('student_dashboard') + '?section=add-certificate&error=certificate_required')

    issue_date = _parse_date(request.form.get('issue_date'))
    expiry_date = _parse_date(request.form.get('expiry_date'))

    cert_file_path = None
    certificate_file = request.files.get('certificate_file')
    if certificate_file and certificate_file.filename:
        if _is_allowed_upload(certificate_file.filename, {'pdf', 'jpg', 'jpeg', 'png', 'webp'}):
            cert_file_path = _save_student_file(certificate_file, current_user.id, 'certificates')

    cert = StudentCertificate(
        user_id=current_user.id,
        certificate_name=certificate_name,
        issuing_organization=issuing_organization,
        issue_date=issue_date,
        expiry_date=expiry_date,
        certificate_file_path=cert_file_path,
        description=request.form.get('description', '').strip() or None
    )
    db.session.add(cert)
    db.session.commit()
    return redirect(url_for('student_dashboard') + '?section=add-certificate&saved=1')

@app.route('/student/internship-experience', methods=['POST'])
@login_required
@role_required('student')
def add_student_internship_experience():
    company_name = request.form.get('company_name', '').strip()
    role = request.form.get('role', '').strip()
    if not company_name or not role:
        return redirect(url_for('student_dashboard') + '?section=add-internship&error=internship_required')

    start_date = _parse_date(request.form.get('start_date'))
    end_date = _parse_date(request.form.get('end_date'))

    proof_file_path = None
    proof_file = request.files.get('proof_file')
    if proof_file and proof_file.filename:
        if _is_allowed_upload(proof_file.filename, {'pdf', 'jpg', 'jpeg', 'png', 'webp'}):
            proof_file_path = _save_student_file(proof_file, current_user.id, 'internships')

    exp = StudentInternshipExperience(
        user_id=current_user.id,
        company_name=company_name,
        role=role,
        start_date=start_date,
        end_date=end_date,
        location=request.form.get('location', '').strip() or None,
        stipend=request.form.get('stipend', '').strip() or None,
        skills_used=request.form.get('skills_used', '').strip() or None,
        work_description=request.form.get('work_description', '').strip() or None,
        proof_file_path=proof_file_path
    )
    db.session.add(exp)
    db.session.commit()
    return redirect(url_for('student_dashboard') + '?section=add-internship&saved=1')


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _is_allowed_upload(filename, allowed_extensions):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_extensions


def _save_student_file(file_obj, user_id, folder_name):
    safe_name = secure_filename(file_obj.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    saved_name = f'{timestamp}_{safe_name}'
    relative_dir = os.path.join('uploads', 'students', str(user_id), folder_name)
    absolute_dir = os.path.join(app.static_folder, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)
    file_obj.save(os.path.join(absolute_dir, saved_name))
    return f'static/{relative_dir}/{saved_name}'

@app.route('/student/change-password', methods=['POST'])
@login_required
@role_required('student')
def student_change_password():
    current_pw = request.form.get('current_password', '')
    new_pw = request.form.get('new_password', '')
    if current_user.password != current_pw:
        return redirect(url_for('student_dashboard') + '?section=settings&error=wrong_password')
    if len(new_pw) < 6:
        return redirect(url_for('student_dashboard') + '?section=settings&error=short_password')
    current_user.password = new_pw
    db.session.commit()
    return redirect(url_for('student_dashboard') + '?section=settings&saved=1')

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
    all_users = User.query.order_by(User.id.desc()).limit(10).all()
    all_internships = Internship.query.order_by(Internship.created_at.desc()).all()
    total_students = StudentProfile.query.count()
    total_orgs = Organization.query.count()
    verified_orgs = Organization.query.filter_by(is_verified=True).count()
    pending_orgs = Organization.query.filter_by(verification_status='pending').count()
    total_internships = Internship.query.count()

    recent_internships = []
    for i in all_internships[:8]:
        org = Organization.query.filter_by(id=i.organization_id).first() if i.organization_id else None
        recent_internships.append({'internship': i, 'org': org})

    pending_org_list = Organization.query.filter_by(verification_status='pending').all()

    stats = {
        'total_students': total_students,
        'total_orgs': total_orgs,
        'verified_orgs': verified_orgs,
        'pending_orgs': pending_orgs,
        'total_internships': total_internships,
    }
    return render_template('dashboard_admin.html', stats=stats, recent_users=all_users, recent_internships=recent_internships, pending_org_list=pending_org_list)

@app.route('/admin/internships')
@login_required
@admin_required
def admin_internships():
    all_internships = Internship.query.all()
    internships = [
        {'internship': i, 'org': Organization.query.filter_by(id=i.organization_id).first() if i.organization_id else None}
        for i in all_internships
    ]
    stats = {
        'total_internships': len(all_internships),
    }
    return render_template('admin_internships.html', internships=internships, stats=stats)

@app.route('/admin/organizations')
@login_required
@admin_required
def admin_organizations():
    pending_orgs = Organization.query.filter_by(verification_status='pending').all()
    verified_orgs_list = Organization.query.filter_by(verification_status='approved').all()
    total_orgs = Organization.query.count()
    verified_orgs = len(verified_orgs_list)
    return render_template('admin_verify_organizations.html', organizations=pending_orgs, verified_orgs_list=verified_orgs_list, total_orgs=total_orgs, verified_orgs=verified_orgs)

@app.route('/admin/organization/<int:org_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_organization(org_id):
    org = Organization.query.get_or_404(org_id)
    action = request.form.get('action')
    notes = request.form.get('notes', '')
    if action == 'approve':
        org.is_verified = True
        org.verification_status = 'approved'
    elif action == 'reject':
        org.is_verified = False
        org.verification_status = 'rejected'
    org.verification_notes = notes
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Organization {action}d'})

@app.route('/admin/students')
@login_required
@admin_required
def admin_students():
    all_profiles = StudentProfile.query.all()
    students = []
    for profile in all_profiles:
        user = User.query.get(profile.user_id)
        if user:
            students.append({'user': user, 'profile': profile})
    return render_template('admin_students.html', students=students)

@app.route('/admin/reports')
@login_required
@admin_required
def admin_reports():
    total_students = StudentProfile.query.count()
    total_orgs = Organization.query.count()
    verified_orgs = Organization.query.filter_by(is_verified=True).count()
    pending_orgs = Organization.query.filter_by(verification_status='pending').count()
    rejected_orgs = Organization.query.filter_by(verification_status='rejected').count()
    total_internships = Internship.query.count()
    allocated_students = StudentProfile.query.filter(StudentProfile.allocated_internship != None).count()
    students_with_skills = StudentProfile.query.filter(StudentProfile.skills != None, StudentProfile.skills != '').count()

    stats = {
        'total_students': total_students,
        'total_orgs': total_orgs,
        'verified_orgs': verified_orgs,
        'pending_orgs': pending_orgs,
        'rejected_orgs': rejected_orgs,
        'total_internships': total_internships,
        'allocated_students': allocated_students,
        'students_with_skills': students_with_skills,
    }
    return render_template('admin_reports.html', stats=stats, monthly_data=[])

@app.route('/admin/notifications')
@login_required
@admin_required
def admin_notifications():
    notifications = []

    recent_orgs = Organization.query.order_by(Organization.created_at.desc()).limit(5).all()
    for org in recent_orgs:
        notifications.append({
            'icon': 'ORG',
            'title': f'New organization registered: {org.company_name}',
            'message': f'Status: {org.verification_status}',
            'color': '#fbbf24' if org.verification_status == 'pending' else '#22c55e',
            'time': org.created_at.strftime('%d %b %Y') if org.created_at else ''
        })

    recent_internships = Internship.query.order_by(Internship.created_at.desc()).limit(5).all()
    for internship in recent_internships:
        notifications.append({
            'icon': 'INT',
            'title': f'New internship posted: {internship.title}',
            'message': 'Active internship posting',
            'color': '#22c55e',
            'time': internship.created_at.strftime('%d %b %Y') if internship.created_at else ''
        })

    recent_students = User.query.filter_by(role='student').order_by(User.id.desc()).limit(5).all()
    for student in recent_students:
        notifications.append({
            'icon': 'STU',
            'title': f'New student registered: {student.name}',
            'message': student.email,
            'color': '#8b5cf6',
            'time': ''
        })

    return render_template('admin_notifications.html', notifications=notifications)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_settings():
    success = None
    error   = None
    step    = request.args.get('step')   # None | 'otp' | 'newpass'

    if request.method == 'POST':
        action = request.form.get('action')

        # ── Profile update (unchanged) ──────────────────────────────────────
        if action == 'profile':
            current_user.name  = request.form.get('name',  current_user.name)
            current_user.email = request.form.get('email', current_user.email)
            db.session.commit()
            success = 'profile'

        # ── Step 1: send OTP to admin email ──────────────────────────────────
        elif action == 'send_otp':
            otp = ''.join(random.choices(string.digits, k=6))
            session['admin_otp']         = otp
            session['admin_otp_expires'] = (datetime.now() + timedelta(minutes=10)).isoformat()
            session['admin_otp_verified'] = False
            if send_otp_email(current_user.email, otp):
                return redirect(url_for('admin_settings') + '?step=otp&sent=1')
            else:
                error = 'email_failed'

        # ── Step 2: verify OTP ───────────────────────────────────────────────
        elif action == 'verify_otp':
            entered     = request.form.get('otp', '').strip()
            stored_otp  = session.get('admin_otp')
            expires_str = session.get('admin_otp_expires')

            if not stored_otp or not expires_str:
                error = 'no_otp'
            elif datetime.now() > datetime.fromisoformat(expires_str):
                error = 'otp_expired'
                session.pop('admin_otp', None)
            elif entered != stored_otp:
                error = 'wrong_otp'
                step  = 'otp'
            else:
                session['admin_otp_verified'] = True
                session.pop('admin_otp', None)
                session.pop('admin_otp_expires', None)
                return redirect(url_for('admin_settings') + '?step=newpass')

        # ── Step 3: change password (only after OTP verified) ────────────────
        elif action == 'password':
            if not session.get('admin_otp_verified'):
                error = 'not_verified'
            elif request.form.get('new_password') != request.form.get('confirm_password'):
                error = 'password_mismatch'
                step  = 'newpass'
            elif len(request.form.get('new_password', '')) < 6:
                error = 'password_short'
                step  = 'newpass'
            else:
                current_user.password = request.form.get('new_password')
                db.session.commit()
                session.pop('admin_otp_verified', None)
                success = 'password'

    return render_template('admin_settings.html', success=success, error=error, step=step)

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)