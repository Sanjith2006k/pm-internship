"""
Seed script – populates the InternAI database with realistic demo data.
Safe to re-run: existing rows (matched by email / unique field) are skipped.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from app import app, db
from app import (
    User, StudentProfile, StudentPortfolio, StudentCertificate,
    StudentInternshipExperience, Organization, Internship, Application
)
from werkzeug.security import generate_password_hash
from datetime import date, datetime

def seed():
    with app.app_context():
        db.create_all()

        # ── 1. ORGANIZATIONS ────────────────────────────────────────────────
        orgs_data = [
            dict(email='hr@technova.io',      password='org123', name='TechNova Solutions',
                 company='TechNova Solutions',  gst='27AABCT1332L1ZG', domain='technova.io',
                 linkedin='https://linkedin.com/company/technova', industry='Software',
                 location='Bangalore', desc='Full-stack product company building SaaS tools for SMEs.'),
            dict(email='careers@datamind.ai',  password='org123', name='DataMind Analytics',
                 company='DataMind Analytics',  gst='27AABCD5566M1ZH', domain='datamind.ai',
                 linkedin='https://linkedin.com/company/datamind', industry='Data & AI',
                 location='Hyderabad', desc='AI-first analytics firm delivering predictive intelligence.'),
            dict(email='jobs@cloudedge.com',   password='org123', name='CloudEdge Systems',
                 company='CloudEdge Systems',   gst='07AABCE1234N1ZI', domain='cloudedge.com',
                 linkedin='https://linkedin.com/company/cloudedge', industry='Cloud Computing',
                 location='Mumbai', desc='Cloud-native infrastructure and DevOps consulting.'),
            dict(email='studio@designhub.in',  password='org123', name='DesignHub Studio',
                 company='DesignHub Studio',    gst='29AABCD9988P1ZJ', domain='designhub.in',
                 linkedin='https://linkedin.com/company/designhub', industry='Design',
                 location='Pune', desc='Award-winning UX/UI design studio for mobile and web.'),
            dict(email='recruit@securenet.co', password='org123', name='SecureNet Technologies',
                 company='SecureNet Technologies', gst='06AABCS3344Q1ZK', domain='securenet.co',
                 linkedin='https://linkedin.com/company/securenet', industry='Cybersecurity',
                 location='Chennai', desc='Cybersecurity solutions for enterprise and government.'),
            dict(email='team@innostartup.in',  password='org123', name='InnoStartup Labs',
                 company='InnoStartup Labs',    gst='19AABCI7755R1ZL', domain='innostartup.in',
                 linkedin='https://linkedin.com/company/innostartup', industry='Startup',
                 location='Delhi', desc='Early-stage startup incubator specializing in EdTech and FinTech.'),
        ]

        org_objects = {}
        for o in orgs_data:
            user = User.query.filter_by(email=o['email']).first()
            if not user:
                user = User(email=o['email'], name=o['name'],
                            password=generate_password_hash(o['password']), role='organization')
                db.session.add(user)
                db.session.flush()
                org = Organization(
                    user_id=user.id, company_name=o['company'], gst_number=o['gst'],
                    domain_email=o['domain'], linkedin_profile=o['linkedin'],
                    industry=o['industry'], location=o['location'], description=o['desc'],
                    is_verified=True, verification_status='approved',
                )
                db.session.add(org)
                db.session.flush()
                print(f'  ✅ Org: {o["company"]}')
            else:
                org = Organization.query.filter_by(user_id=user.id).first()
                print(f'  ⏭️  Org exists: {o["company"]}')
            org_objects[o['company']] = org

        db.session.commit()

        # ── 2. INTERNSHIPS ────────────────────────────────────────────────
        internships_data = [
            # TechNova
            dict(org='TechNova Solutions', title='Full Stack Web Development Intern',
                 skills='React, Node.js, JavaScript, HTML, CSS, REST API, Git',
                 capacity=5, location='Bangalore', duration='3 months', stipend='15000'),
            dict(org='TechNova Solutions', title='Backend Engineer Intern',
                 skills='Python, Flask, PostgreSQL, REST API, Docker, Git',
                 capacity=4, location='Bangalore', duration='6 months', stipend='18000'),
            dict(org='TechNova Solutions', title='Mobile App Development Intern',
                 skills='React Native, JavaScript, Firebase, REST API, Git',
                 capacity=3, location='Remote', duration='3 months', stipend='12000'),
            # DataMind
            dict(org='DataMind Analytics', title='AI / Data Science Intern',
                 skills='Python, Machine Learning, Pandas, NumPy, Scikit-learn, SQL',
                 capacity=4, location='Hyderabad', duration='6 months', stipend='20000'),
            dict(org='DataMind Analytics', title='Data Analyst Intern',
                 skills='SQL, Python, Tableau, Excel, Statistics, Data Visualization',
                 capacity=5, location='Hyderabad', duration='3 months', stipend='14000'),
            dict(org='DataMind Analytics', title='Machine Learning Research Intern',
                 skills='Python, TensorFlow, PyTorch, Deep Learning, NLP, Computer Vision',
                 capacity=2, location='Remote', duration='6 months', stipend='22000'),
            # CloudEdge
            dict(org='CloudEdge Systems', title='Cloud Infrastructure Intern',
                 skills='AWS, Azure, Docker, Kubernetes, Linux, Terraform, Python',
                 capacity=4, location='Mumbai', duration='6 months', stipend='18000'),
            dict(org='CloudEdge Systems', title='DevOps Engineer Intern',
                 skills='CI/CD, Jenkins, Git, Docker, Python, Linux, Bash',
                 capacity=3, location='Mumbai', duration='3 months', stipend='16000'),
            # DesignHub
            dict(org='DesignHub Studio', title='UI/UX Design Intern',
                 skills='Figma, Adobe XD, User Research, Prototyping, HTML, CSS',
                 capacity=5, location='Pune', duration='3 months', stipend='12000'),
            dict(org='DesignHub Studio', title='Graphic Design Intern',
                 skills='Adobe Illustrator, Photoshop, Figma, Typography, Branding',
                 capacity=3, location='Remote', duration='3 months', stipend='10000'),
            # SecureNet
            dict(org='SecureNet Technologies', title='Cybersecurity Analyst Intern',
                 skills='Network Security, Python, Linux, Penetration Testing, SIEM, Firewalls',
                 capacity=3, location='Chennai', duration='6 months', stipend='18000'),
            dict(org='SecureNet Technologies', title='Ethical Hacking Intern',
                 skills='Python, Kali Linux, OWASP, Burp Suite, Network Security, CTF',
                 capacity=2, location='Chennai', duration='3 months', stipend='15000'),
            # InnoStartup
            dict(org='InnoStartup Labs', title='Product Management Intern',
                 skills='Product Roadmap, Agile, Scrum, User Stories, Market Research, SQL',
                 capacity=3, location='Delhi', duration='3 months', stipend='13000'),
            dict(org='InnoStartup Labs', title='Growth Marketing Intern',
                 skills='Digital Marketing, SEO, Content Writing, Analytics, Social Media',
                 capacity=4, location='Delhi', duration='3 months', stipend='11000'),
            dict(org='InnoStartup Labs', title='Business Development Intern',
                 skills='Sales, Communication, CRM, Excel, Market Research, Presentation',
                 capacity=5, location='Remote', duration='3 months', stipend='10000'),
        ]

        for i in internships_data:
            org = org_objects.get(i['org'])
            if not org:
                continue
            existing = Internship.query.filter_by(
                organization_id=org.id, title=i['title']).first()
            if not existing:
                intern = Internship(
                    organization_id=org.id, title=i['title'],
                    skills_required=i['skills'], capacity=i['capacity'],
                    location=i['location'], duration=i['duration'],
                    stipend=i['stipend'], status='approved',
                )
                db.session.add(intern)
                print(f'  ✅ Internship: {i["title"]}')
            else:
                print(f'  ⏭️  Internship exists: {i["title"]}')

        db.session.commit()

        # ── 3. STUDENTS ────────────────────────────────────────────────────
        students_data = [
            dict(email='alice@student.com',   name='Alice Sharma',   location='Bangalore',
                 skills='Python, Machine Learning, SQL, Data Analysis, NumPy, Pandas'),
            dict(email='bob@student.com',     name='Bob Patel',      location='Hyderabad',
                 skills='React, JavaScript, HTML, CSS, Node.js, Git, REST API'),
            dict(email='carol@student.com',   name='Carol Nair',     location='Bangalore',
                 skills='Python, TensorFlow, Deep Learning, Computer Vision, OpenCV'),
            dict(email='david@student.com',   name='David Rao',      location='Mumbai',
                 skills='AWS, Docker, Linux, Python, Kubernetes, CI/CD, Terraform'),
            dict(email='emma@student.com',    name='Emma Joshi',     location='Pune',
                 skills='Figma, Adobe XD, UI/UX Design, Prototyping, User Research, CSS'),
            dict(email='frank@student.com',   name='Frank Mehta',    location='Chennai',
                 skills='Cybersecurity, Python, Linux, Network Security, Penetration Testing'),
            dict(email='grace@student.com',   name='Grace Krishnan', location='Delhi',
                 skills='Java, Spring Boot, SQL, REST API, Git, Microservices, Docker'),
            dict(email='henry@student.com',   name='Henry Das',      location='Hyderabad',
                 skills='Python, Flask, Django, PostgreSQL, REST API, Redis, Docker'),
            dict(email='irene@student.com',   name='Irene Verma',    location='Bangalore',
                 skills='React Native, JavaScript, Firebase, Git, REST API, Redux'),
            dict(email='james@student.com',   name='James Pillai',   location='Chennai',
                 skills='Data Analysis, Python, SQL, Tableau, Excel, Statistics, Power BI'),
        ]

        student_user_objs = {}
        for s in students_data:
            user = User.query.filter_by(email=s['email']).first()
            if not user:
                user = User(email=s['email'], name=s['name'],
                            password=generate_password_hash('student123'), role='student')
                db.session.add(user)
                db.session.flush()
                profile = StudentProfile(user_id=user.id, skills=s['skills'], location=s['location'])
                db.session.add(profile)
                db.session.flush()
                print(f'  ✅ Student: {s["name"]} ({s["location"]})')
            else:
                profile = StudentProfile.query.filter_by(user_id=user.id).first()
                if profile and not profile.location:
                    profile.location = s['location']
                print(f'  ⏭️  Student exists: {s["name"]}')
            student_user_objs[s['email']] = (user, profile if 'profile' in dir() or True else
                StudentProfile.query.filter_by(user_id=user.id).first())

        db.session.commit()

        # Re-fetch profiles cleanly
        student_profiles = {}
        for email, (user, _) in student_user_objs.items():
            p = StudentProfile.query.filter_by(user_id=user.id).first()
            student_profiles[email] = (user, p)

        # ── 4. CERTIFICATES ────────────────────────────────────────────────
        certs_data = [
            ('alice@student.com',  'AWS Certified Cloud Practitioner', 'Amazon Web Services',
             date(2023, 6, 15), date(2026, 6, 15)),
            ('alice@student.com',  'Google Data Analytics Certificate', 'Google',
             date(2023, 9, 20), None),
            ('bob@student.com',    'Meta Front-End Developer Certificate', 'Meta',
             date(2023, 7, 10), None),
            ('carol@student.com',  'TensorFlow Developer Certificate', 'Google',
             date(2023, 11, 5), date(2026, 11, 5)),
            ('david@student.com',  'AWS Solutions Architect – Associate', 'Amazon Web Services',
             date(2023, 8, 22), date(2026, 8, 22)),
            ('david@student.com',  'Certified Kubernetes Administrator (CKA)', 'CNCF',
             date(2024, 1, 10), date(2027, 1, 10)),
            ('emma@student.com',   'Google UX Design Certificate', 'Google',
             date(2023, 5, 30), None),
            ('frank@student.com',  'CompTIA Security+', 'CompTIA',
             date(2023, 7, 18), date(2026, 7, 18)),
            ('frank@student.com',  'Certified Ethical Hacker (CEH)', 'EC-Council',
             date(2024, 2, 14), date(2027, 2, 14)),
            ('grace@student.com',  'Oracle Java SE Programmer', 'Oracle',
             date(2023, 10, 5), date(2026, 10, 5)),
            ('henry@student.com',  'Django REST Framework Certification', 'Udemy',
             date(2023, 12, 12), None),
            ('irene@student.com',  'React Native Specialist', 'Coursera',
             date(2024, 1, 20), None),
            ('james@student.com',  'Tableau Desktop Specialist', 'Tableau',
             date(2023, 9, 8), date(2026, 9, 8)),
            ('james@student.com',  'Microsoft Power BI Data Analyst', 'Microsoft',
             date(2024, 3, 1), date(2027, 3, 1)),
            ('bob@student.com',    'JavaScript Algorithms & Data Structures', 'freeCodeCamp',
             date(2023, 6, 25), None),
            ('carol@student.com',  'Deep Learning Specialization', 'Coursera / DeepLearning.AI',
             date(2023, 8, 15), None),
        ]

        for email, cert_name, issuer, issue_dt, expiry_dt in certs_data:
            user, _ = student_profiles.get(email, (None, None))
            if not user:
                continue
            existing = StudentCertificate.query.filter_by(
                user_id=user.id, certificate_name=cert_name).first()
            if not existing:
                c = StudentCertificate(user_id=user.id, certificate_name=cert_name,
                    issuing_organization=issuer, issue_date=issue_dt, expiry_date=expiry_dt)
                db.session.add(c)
                print(f'  ✅ Cert: {cert_name} → {email}')
            else:
                print(f'  ⏭️  Cert exists: {cert_name}')

        db.session.commit()

        # ── 5. EXPERIENCES ────────────────────────────────────────────────
        experiences_data = [
            ('alice@student.com',  'InfoSys BPM', 'Data Science Intern',
             date(2023, 5, 1), date(2023, 8, 31), 'Bangalore', '12000',
             'Python, SQL, Data Visualization', 'Built sales dashboards and ML models for churn prediction.'),
            ('bob@student.com',    'Wipro Digital', 'Frontend Intern',
             date(2023, 6, 1), date(2023, 9, 30), 'Hyderabad', '10000',
             'React, CSS, JavaScript', 'Developed responsive UI components for client web portals.'),
            ('carol@student.com',  'NVIDIA AI Labs', 'ML Research Intern',
             date(2023, 7, 1), date(2023, 12, 31), 'Bangalore', '25000',
             'Python, PyTorch, Computer Vision', 'Researched object detection models for autonomous drones.'),
            ('david@student.com',  'HCL Cloud Services', 'Cloud Operations Intern',
             date(2023, 5, 15), date(2023, 9, 15), 'Mumbai', '15000',
             'AWS, Linux, Docker', 'Managed cloud infrastructure and automated deployment pipelines.'),
            ('frank@student.com',  'Qualys', 'Security Analyst Intern',
             date(2023, 6, 1), date(2023, 11, 30), 'Chennai', '14000',
             'Penetration Testing, Python, SIEM', 'Conducted vulnerability assessments and security audits.'),
            ('emma@student.com',   'Zomato', 'UX Design Intern',
             date(2023, 3, 1), date(2023, 6, 30), 'Pune', '11000',
             'Figma, User Research, Prototyping', 'Redesigned the restaurant partner onboarding flow.'),
        ]

        for email, company, role, start, end, loc, stipend, skills, desc in experiences_data:
            user, _ = student_profiles.get(email, (None, None))
            if not user:
                continue
            existing = StudentInternshipExperience.query.filter_by(
                user_id=user.id, company_name=company).first()
            if not existing:
                e = StudentInternshipExperience(
                    user_id=user.id, company_name=company, role=role,
                    start_date=start, end_date=end, location=loc,
                    stipend=stipend, skills_used=skills, work_description=desc,
                )
                db.session.add(e)
                print(f'  ✅ Experience: {role} @ {company} → {email}')
            else:
                print(f'  ⏭️  Experience exists: {role} @ {company}')

        db.session.commit()

        # ── 6. APPLICATIONS ────────────────────────────────────────────────
        all_internships = Internship.query.filter_by(status='approved').all()
        intern_map = {i.title: i for i in all_internships}

        apps_data = [
            ('alice@student.com',  'AI / Data Science Intern',                'approved'),
            ('bob@student.com',    'Full Stack Web Development Intern',         'pending'),
            ('carol@student.com',  'Machine Learning Research Intern',          'approved'),
            ('david@student.com',  'DevOps Engineer Intern',                    'pending'),
            ('emma@student.com',   'UI/UX Design Intern',                       'approved'),
            ('frank@student.com',  'Cybersecurity Analyst Intern',              'pending'),
            ('grace@student.com',  'Backend Engineer Intern',                   'pending'),
            ('henry@student.com',  'Backend Engineer Intern',                   'approved'),
            ('irene@student.com',  'Mobile App Development Intern',             'pending'),
            ('james@student.com',  'Data Analyst Intern',                       'approved'),
        ]

        for email, intern_title, status in apps_data:
            user, profile = student_profiles.get(email, (None, None))
            intern = intern_map.get(intern_title)
            if not user or not profile or not intern:
                continue
            existing = Application.query.filter_by(
                student_id=profile.id, internship_id=intern.id).first()
            if not existing:
                a = Application(student_id=profile.id, internship_id=intern.id, status=status)
                db.session.add(a)
                print(f'  ✅ Application: {email} → {intern_title} [{status}]')
            else:
                print(f'  ⏭️  Application exists: {email} → {intern_title}')

        db.session.commit()

        # ── SUMMARY ────────────────────────────────────────────────────────
        print('\n' + '='*52)
        print(f'  Users:        {User.query.count()}')
        print(f'  Organizations:{Organization.query.count()}')
        print(f'  Internships:  {Internship.query.count()}')
        print(f'  Students:     {StudentProfile.query.count()}')
        print(f'  Certificates: {StudentCertificate.query.count()}')
        print(f'  Experiences:  {StudentInternshipExperience.query.count()}')
        print(f'  Applications: {Application.query.count()}')
        print('='*52)
        print('  Seed complete!')


if __name__ == '__main__':
    seed()
