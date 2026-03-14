import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

# ─── CAREER PATH DATA ─────────────────────────────────────────────────────────
CAREER_PATHS = {
    'Data Scientist': {
        'skills': ['python', 'machine learning', 'statistics', 'data analysis', 'pandas', 'numpy', 'scikit-learn', 'sql', 'visualization'],
        'description': 'Analyze complex datasets to identify patterns and build predictive models.',
        'internships': ['Data Analyst Intern', 'ML Research Intern', 'AI/Data Science Intern'],
        'salary_range': '₹8-25 LPA',
        'icon': '📊',
    },
    'AI / ML Engineer': {
        'skills': ['python', 'tensorflow', 'pytorch', 'deep learning', 'nlp', 'computer vision', 'machine learning', 'neural networks'],
        'description': 'Design, train, and deploy intelligent AI/ML systems at scale.',
        'internships': ['Machine Learning Intern', 'AI Research Intern', 'Deep Learning Intern'],
        'salary_range': '₹10-30 LPA',
        'icon': '🤖',
    },
    'Full Stack Developer': {
        'skills': ['javascript', 'react', 'node.js', 'html', 'css', 'sql', 'rest api', 'git', 'python', 'flask'],
        'description': 'Build complete web applications from frontend to backend.',
        'internships': ['Web Development Intern', 'Frontend Intern', 'Backend Intern'],
        'salary_range': '₹6-20 LPA',
        'icon': '💻',
    },
    'Cybersecurity Analyst': {
        'skills': ['networking', 'security', 'linux', 'penetration testing', 'cryptography', 'ethical hacking', 'firewalls'],
        'description': 'Protect systems and data from cyber threats and vulnerabilities.',
        'internships': ['Security Analyst Intern', 'SOC Intern', 'Ethical Hacking Intern'],
        'salary_range': '₹7-22 LPA',
        'icon': '🔐',
    },
    'Cloud / DevOps Engineer': {
        'skills': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'devops', 'linux', 'terraform', 'ci/cd'],
        'description': 'Design, build, and manage scalable cloud infrastructure.',
        'internships': ['Cloud Intern', 'DevOps Intern', 'Infrastructure Intern'],
        'salary_range': '₹8-25 LPA',
        'icon': '☁️',
    },
    'Business / Data Analyst': {
        'skills': ['data analysis', 'excel', 'sql', 'power bi', 'tableau', 'communication', 'problem solving', 'ms office'],
        'description': 'Bridge business problems and technical solutions through data-driven insights.',
        'internships': ['Business Analyst Intern', 'Data Analyst Intern', 'Product Analyst Intern'],
        'salary_range': '₹6-18 LPA',
        'icon': '📈',
    },
    'Product Manager': {
        'skills': ['product management', 'agile', 'scrum', 'communication', 'analytics', 'strategy', 'user research'],
        'description': 'Lead product vision and strategy from concept to launch.',
        'internships': ['Product Intern', 'PM Intern', 'Product Strategy Intern'],
        'salary_range': '₹10-25 LPA',
        'icon': '🎯',
    },
    'UI / UX Designer': {
        'skills': ['figma', 'sketch', 'adobe xd', 'user research', 'prototyping', 'wireframing', 'css', 'design thinking'],
        'description': 'Create intuitive and visually impressive user experiences.',
        'internships': ['UI/UX Intern', 'Design Intern', 'Product Design Intern'],
        'salary_range': '₹5-18 LPA',
        'icon': '🎨',
    },
}

# ─── INTERVIEW QUESTION BANK ──────────────────────────────────────────────────
INTERVIEW_QUESTIONS = {
    'python': [
        {'q': 'Explain the difference between a list and a tuple in Python.', 'keywords': ['mutable', 'immutable', 'list', 'tuple', 'change'], 'difficulty': 'Easy'},
        {'q': 'What is a Python decorator? Give an example use case.', 'keywords': ['function', 'wrapper', 'modify', 'behavior', '@'], 'difficulty': 'Medium'},
        {'q': 'Explain the concept of generators and when you would use them.', 'keywords': ['yield', 'iterator', 'memory', 'lazy', 'sequence'], 'difficulty': 'Medium'},
    ],
    'machine learning': [
        {'q': 'Explain the difference between supervised and unsupervised learning.', 'keywords': ['labeled', 'unlabeled', 'training', 'prediction', 'clustering'], 'difficulty': 'Easy'},
        {'q': 'What is overfitting and how do you prevent it?', 'keywords': ['training', 'test', 'regularization', 'dropout', 'cross-validation', 'generalize'], 'difficulty': 'Medium'},
        {'q': 'Explain gradient descent and its variants (SGD, Adam).', 'keywords': ['gradient', 'learning rate', 'optimization', 'batch', 'stochastic', 'minimize'], 'difficulty': 'Hard'},
    ],
    'data structures': [
        {'q': 'What is the time complexity of common operations in a Hash Map?', 'keywords': ['O(1)', 'average', 'collision', 'hash', 'lookup', 'constant'], 'difficulty': 'Medium'},
        {'q': 'Explain the difference between BFS and DFS graph traversal.', 'keywords': ['breadth', 'depth', 'queue', 'stack', 'level', 'path'], 'difficulty': 'Easy'},
    ],
    'web development': [
        {'q': 'What is the difference between REST and GraphQL APIs?', 'keywords': ['endpoint', 'query', 'flexible', 'over-fetching', 'schema', 'request'], 'difficulty': 'Medium'},
        {'q': 'Explain how HTTPS works and why it is important for security.', 'keywords': ['ssl', 'tls', 'encryption', 'certificate', 'secure', 'handshake'], 'difficulty': 'Medium'},
    ],
    'sql': [
        {'q': 'What is the difference between INNER JOIN and LEFT JOIN in SQL?', 'keywords': ['inner', 'left', 'matching', 'null', 'rows', 'join'], 'difficulty': 'Easy'},
    ],
    'general': [
        {'q': 'Describe a challenging technical problem you solved and your approach to it.', 'keywords': ['problem', 'solution', 'approach', 'learned', 'result'], 'difficulty': 'Easy'},
        {'q': 'Where do you see yourself in 5 years in the technology field?', 'keywords': ['growth', 'skills', 'career', 'goal', 'technology'], 'difficulty': 'Easy'},
        {'q': 'Explain a project you worked on from start to finish.', 'keywords': ['built', 'designed', 'implemented', 'tested', 'project'], 'difficulty': 'Easy'},
    ],
}

# ─── COMPANY CULTURE TYPES ────────────────────────────────────────────────────
CULTURE_TYPES = {
    'Innovative Startup': {
        'traits': {'risk_taking': 5, 'teamwork': 4, 'structure': 2, 'creativity': 5, 'pace': 5},
        'description': 'Fast-paced, creative environment with high ownership and impact.',
        'examples': ['Early-stage startups', 'Product companies', 'R&D labs'],
        'icon': '🚀',
    },
    'Corporate Enterprise': {
        'traits': {'risk_taking': 2, 'teamwork': 3, 'structure': 5, 'creativity': 2, 'pace': 3},
        'description': 'Structured environment with clear processes, stability, and career ladders.',
        'examples': ['TCS', 'Infosys', 'Wipro', 'Large MNCs'],
        'icon': '🏢',
    },
    'Scale-up Company': {
        'traits': {'risk_taking': 3, 'teamwork': 5, 'structure': 3, 'creativity': 4, 'pace': 4},
        'description': 'Growing company balancing innovation with process.',
        'examples': ['Series B/C startups', 'Mid-stage tech companies'],
        'icon': '📈',
    },
    'Government / PSU': {
        'traits': {'risk_taking': 1, 'teamwork': 3, 'structure': 5, 'creativity': 2, 'pace': 2},
        'description': 'Stable, structured environment with job security and social impact.',
        'examples': ['ISRO', 'DRDO', 'Government tech departments'],
        'icon': '🏛️',
    },
    'Research Lab': {
        'traits': {'risk_taking': 4, 'teamwork': 3, 'structure': 3, 'creativity': 5, 'pace': 2},
        'description': 'Deep technical exploration with academic-industry collaboration.',
        'examples': ['IIT labs', 'Google Research', 'Microsoft Research India'],
        'icon': '🔬',
    },
}

# ─── TRUSTED CERTIFICATE ISSUERS ──────────────────────────────────────────────
TRUSTED_ISSUERS = [
    'coursera', 'udemy', 'google', 'microsoft', 'amazon', 'ibm', 'meta',
    'nptel', 'swayam', 'infosys springboard', 'edx', 'linkedin learning',
    'cisco', 'red hat', 'oracle', 'aws', 'iit', 'nit', 'bits', 'mit',
    'stanford', 'harvard', 'upgrad', 'great learning', 'simplilearn',
    'internshala', 'nasscom', 'nism', 'sebi', 'ncfm', 'apssdc', 'adobe',
]

# ─── INSTITUTION KNOWLEDGE BASE ───────────────────────────────────────────────
INSTITUTION_REGISTRY = {
    'aws': {
        'name': 'Amazon Web Services (AWS)',
        'type': 'Cloud Technology Provider',
        'description': 'AWS is the world\'s most comprehensive cloud platform, trusted by millions of customers. AWS certifications are globally recognized credentials for cloud expertise.',
        'cert_types': ['Cloud Practitioner', 'Solutions Architect', 'Developer', 'SysOps Admin', 'Machine Learning Specialty', 'Security Specialty'],
        'verify_url': 'https://www.credly.com/org/amazon-web-services',
        'verification_note': 'Verify via Credly badge link on the certificate or at aws.amazon.com/certification/certification-prep/testing/.',
    },
    'amazon': {
        'name': 'Amazon Web Services (AWS)',
        'type': 'Cloud Technology Provider',
        'description': 'AWS is the world\'s most comprehensive cloud platform, trusted by millions of customers. AWS certifications are globally recognized credentials for cloud expertise.',
        'cert_types': ['Cloud Practitioner', 'Solutions Architect', 'Developer', 'SysOps Admin', 'Machine Learning Specialty'],
        'verify_url': 'https://www.credly.com/org/amazon-web-services',
        'verification_note': 'Verify via Credly badge or at aws.amazon.com/certification.',
    },
    'google': {
        'name': 'Google',
        'type': 'Technology Corporation',
        'description': 'Google offers industry-recognized certifications in cloud (GCP), data analytics, UX design, IT support, and project management — typically via Coursera or Credly.',
        'cert_types': ['Google Cloud Associate', 'Professional Cloud Architect', 'Data Analytics', 'IT Support', 'UX Design', 'TensorFlow Developer'],
        'verify_url': 'https://www.credly.com/org/google',
        'verification_note': 'Verify Google Cloud certifications at cloud.google.com/certification. Career Certificates are verified via Credly or the Coursera certificate URL.',
    },
    'microsoft': {
        'name': 'Microsoft',
        'type': 'Technology Corporation',
        'description': 'Microsoft certifications validate skills across Azure cloud, Office 365, AI, data engineering, and developer technologies. Certs are role-based and globally recognized.',
        'cert_types': ['AZ-900 Azure Fundamentals', 'AZ-204 Azure Developer', 'AZ-104 Azure Admin', 'DP-900 Data Fundamentals', 'AI-900 AI Fundamentals', 'PL-300 Power BI'],
        'verify_url': 'https://learn.microsoft.com/en-us/certifications/verify/',
        'verification_note': 'Verify using the certificate URL or Microsoft Transcript ID at learn.microsoft.com/en-us/certifications/verify/.',
    },
    'coursera': {
        'name': 'Coursera',
        'type': 'Online Learning Platform',
        'description': 'Coursera is a global online learning platform partnered with 300+ leading universities and companies including Google, IBM, Meta, and Stanford. Certificates are issued on completion of verified courses.',
        'cert_types': ['Course Certificate', 'Specialization Certificate', 'Professional Certificate', 'MasterTrack', 'Degree'],
        'verify_url': 'https://www.coursera.org/verify/',
        'verification_note': 'Verify using the certificate URL or 18-digit certificate ID at coursera.org/verify/<ID>.',
    },
    'udemy': {
        'name': 'Udemy',
        'type': 'Online Learning Marketplace',
        'description': 'Udemy is the world\'s largest online learning marketplace with 210,000+ courses by independent instructors, covering technology, business, and design.',
        'cert_types': ['Course Completion Certificate'],
        'verify_url': 'https://www.udemy.com/certificate/',
        'verification_note': 'Verify using the UC-XXXXX certificate URL printed on the certificate at udemy.com/certificate/<ID>.',
    },
    'ibm': {
        'name': 'IBM',
        'type': 'Technology & Consulting Corporation',
        'description': 'IBM offers professional certifications and digital badges in AI, Cloud, Data Science, Blockchain, and Cybersecurity — primarily through Coursera and Credly.',
        'cert_types': ['IBM Data Science Professional', 'IBM AI Engineering', 'IBM Full Stack Developer', 'IBM Cloud Computing'],
        'verify_url': 'https://www.credly.com/org/ibm',
        'verification_note': 'Verify IBM badges via Credly at credly.com/org/ibm. IBM professional certs are also verifiable via Coursera certificate ID.',
    },
    'meta': {
        'name': 'Meta (Facebook)',
        'type': 'Technology Corporation',
        'description': 'Meta\'s professional certificate programs cover front-end/back-end development, marketing analytics, database engineering, and AR/VR — issued through Coursera.',
        'cert_types': ['Front-End Developer', 'Back-End Developer', 'Marketing Analytics', 'Database Engineer', 'iOS Developer', 'Android Developer'],
        'verify_url': 'https://www.coursera.org/verify/',
        'verification_note': 'Meta certificates are issued via Coursera. Verify using the Coursera certificate URL or ID at coursera.org/verify.',
    },
    'nptel': {
        'name': 'NPTEL (IIT/IISc — MHRD)',
        'type': 'Government Education Initiative (India)',
        'description': 'NPTEL is a joint initiative by IITs and IISc funded by the Ministry of Education, India. It offers free online courses in engineering, science, and humanities with proctored exams.',
        'cert_types': ['Elite Certificate', 'Elite + Silver', 'Elite + Gold', 'Topper Certificate'],
        'verify_url': 'https://nptel.ac.in/noc/E_Certificate/verify.php',
        'verification_note': 'Verify using Roll Number or Certificate ID at nptel.ac.in/noc/E_Certificate/verify.php.',
    },
    'swayam': {
        'name': 'SWAYAM (Government of India)',
        'type': 'Government MOOC Platform (India)',
        'description': 'SWAYAM is the Government of India\'s MOOC platform for school to post-graduate level education, taught by national faculty from IITs, IIMs, and central universities.',
        'cert_types': ['Course Completion', 'Credit Transfer Eligible'],
        'verify_url': 'https://swayam.gov.in/',
        'verification_note': 'Certificates are issued after proctored exam. Verify via SWAYAM portal with enrollment ID.',
    },
    'cisco': {
        'name': 'Cisco',
        'type': 'Networking Technology Corporation',
        'description': 'Cisco certifications (CCNA, CCNP, CCIE) are the global industry standard for networking and cybersecurity professionals, recognized by thousands of employers worldwide.',
        'cert_types': ['CCNA (Routing & Switching)', 'CCNP Enterprise', 'CCIE', 'CyberOps Associate', 'DevNet Associate', 'Security+'],
        'verify_url': 'https://certifications.cisco.com/app/index#!ce-status',
        'verification_note': 'Verify by entering candidate name or certification ID at certifications.cisco.com.',
    },
    'red hat': {
        'name': 'Red Hat',
        'type': 'Open Source Technology Company (IBM subsidiary)',
        'description': 'Red Hat certifications are performance-based exams validating real-world skills in Linux, OpenShift, Ansible, and DevOps. Highly respected by enterprise employers.',
        'cert_types': ['RHCSA (System Administrator)', 'RHCE (Certified Engineer)', 'OpenShift Administrator', 'Ansible Automation'],
        'verify_url': 'https://rhtapps.redhat.com/verify',
        'verification_note': 'Verify by entering certification number at rhtapps.redhat.com/verify.',
    },
    'oracle': {
        'name': 'Oracle Corporation',
        'type': 'Database & Cloud Technology Corporation',
        'description': 'Oracle certifications are industry standards for Java, database (DBA), cloud infrastructure, and middleware — recognized globally in enterprise IT environments.',
        'cert_types': ['Oracle Cloud Infrastructure', 'Java SE Programmer', 'Oracle DBA', 'MySQL Developer'],
        'verify_url': 'https://catalog-education.oracle.com/pls/apex/f?p=1010:26',
        'verification_note': 'Verify using Oracle Certification Number at catalog-education.oracle.com.',
    },
    'linkedin learning': {
        'name': 'LinkedIn Learning',
        'type': 'Professional Online Learning Platform (Microsoft)',
        'description': 'LinkedIn Learning (formerly Lynda.com) is Microsoft\'s professional skill development platform. Certificates are linked directly to LinkedIn profiles.',
        'cert_types': ['Course Certificate', 'Learning Path Certificate'],
        'verify_url': 'https://www.linkedin.com/in/',
        'verification_note': 'Certificates appear on the student\'s LinkedIn profile under Licenses & Certifications. Request the LinkedIn profile URL for verification.',
    },
    'infosys springboard': {
        'name': 'Infosys Springboard',
        'type': 'Corporate Training Platform (Infosys)',
        'description': 'Infosys Springboard is Infosys\'s free upskilling platform offering industry-relevant courses in programming, AI, digital skills, and foundational tech.',
        'cert_types': ['Technology Fundamentals', 'Programming Basics', 'Digital Skills', 'Industry Modules'],
        'verify_url': 'https://infyspringboard.onwingspan.com/',
        'verification_note': 'Verify using certificate ID at Infosys Springboard portal or contact certifications@infosys.com.',
    },
    'internshala': {
        'name': 'Internshala',
        'type': 'Indian Internship & Training Platform',
        'description': 'India\'s leading student internship platform, also offering certified online training programs in programming, design, marketing, and soft skills.',
        'cert_types': ['Training Certificate', 'Industrial Training', 'Internship Certificate'],
        'verify_url': 'https://trainings.internshala.com/verify-certificate/',
        'verification_note': 'Verify training certificates at trainings.internshala.com/verify-certificate/ using the certificate number.',
    },
    'edx': {
        'name': 'edX (2U)',
        'type': 'Online Learning Platform',
        'description': 'edX was founded by MIT and Harvard and now partners with 160+ top universities and companies. Offers MicroMasters, Professional Certificates, and full degrees.',
        'cert_types': ['Verified Certificate', 'Professional Certificate', 'MicroMasters', 'XSeries', 'MicroBachelors'],
        'verify_url': 'https://courses.edx.org/certificates/',
        'verification_note': 'Verify using the certificate URL printed on the document at courses.edx.org/certificates/<ID>.',
    },
    'simplilearn': {
        'name': 'Simplilearn',
        'type': 'Professional Skilling & Bootcamp Platform',
        'description': 'Simplilearn is a global professional certificate and bootcamp provider partnered with universities like Caltech, Purdue, and IITs for upskilling in tech and business.',
        'cert_types': ['SkillUp Certificate', 'Professional Certificate', 'Masters Program', 'University-partnered Post Graduate Program'],
        'verify_url': 'https://certificates.simplilearn.com/',
        'verification_note': 'Verify at certificates.simplilearn.com using the certificate ID printed on the document.',
    },
    'great learning': {
        'name': 'Great Learning',
        'type': 'Online Professional Education Platform',
        'description': 'Great Learning offers university-partnered programs (Stanford, UT Austin, MIT) and standalone certs in AI, data science, cloud, and management.',
        'cert_types': ['Program Certificate', 'PGP Certificate', 'GL Academy Completion Certificate'],
        'verify_url': 'https://www.mygreatlearning.com/certificate',
        'verification_note': 'Verify at mygreatlearning.com/certificate using the certificate ID or QR code on the document.',
    },
    'upgrad': {
        'name': 'upGrad',
        'type': 'Online Higher Education Platform (India)',
        'description': 'upGrad is India\'s largest online higher education platform, partnered with top universities offering degrees, PGPs, and short programs in tech, management, and law.',
        'cert_types': ['PG Diploma', 'Executive PGP', 'Professional Certificate Program', 'Degree Program'],
        'verify_url': 'https://www.upgrad.com/certificate-verification/',
        'verification_note': 'Verify at upgrad.com/certificate-verification using certificate ID or registered email.',
    },
    'nasscom': {
        'name': 'NASSCOM',
        'type': 'IT Industry Association (India)',
        'description': 'NASSCOM is the apex body of the Indian IT industry. Its FutureSkills Prime program certifies skills in emerging technologies for industry readiness.',
        'cert_types': ['FutureSkills Prime', 'Industry Badging', 'Sector Skill Certification'],
        'verify_url': 'https://futureskills.nasscom.in/',
        'verification_note': 'Verify via the NASSCOM FutureSkills Prime portal at futureskills.nasscom.in.',
    },
    'iit': {
        'name': 'Indian Institute of Technology (IIT)',
        'type': 'Premier Government Technical University (India)',
        'description': 'IITs are India\'s most prestigious engineering institutions. Online certs primarily come via NPTEL/Swayam (IIT faculty-taught). On-campus programs are highly competitive.',
        'cert_types': ['NPTEL Certified Course', 'MOOC Completion', 'Professional Development Program'],
        'verify_url': 'https://nptel.ac.in',
        'verification_note': 'IIT-issued NPTEL certificates: verify at nptel.ac.in. For on-campus programs, contact the respective IIT directly.',
    },
}

# Text patterns found in certificate files → INSTITUTION_REGISTRY key
_ISSUER_TEXT_PATTERNS = [
    ('amazon web services', 'aws'),
    ('aws certified', 'aws'),
    ('aws training', 'aws'),
    ('microsoft certified', 'microsoft'),
    ('microsoft azure', 'microsoft'),
    ('microsoft corporation', 'microsoft'),
    ('google cloud', 'google'),
    ('google career certificates', 'google'),
    ('google llc', 'google'),
    ('cisco certified', 'cisco'),
    ('cisco systems', 'cisco'),
    ('red hat certified', 'red hat'),
    ('red hat, inc', 'red hat'),
    ('ibm professional', 'ibm'),
    ('ibm corporation', 'ibm'),
    ('meta platforms', 'meta'),
    ('meta certified', 'meta'),
    ('oracle certified', 'oracle'),
    ('oracle corporation', 'oracle'),
    ('coursera', 'coursera'),
    ('udemy', 'udemy'),
    ('edx', 'edx'),
    ('nptel', 'nptel'),
    ('swayam', 'swayam'),
    ('infosys springboard', 'infosys springboard'),
    ('linkedin learning', 'linkedin learning'),
    ('internshala', 'internshala'),
    ('nasscom', 'nasscom'),
    ('simplilearn', 'simplilearn'),
    ('great learning', 'great learning'),
    ('upgrad', 'upgrad'),
    ('iit ', 'iit'),
]

# ─── COURSE RECOMMENDATIONS ───────────────────────────────────────────────────
COURSE_MAP = {
    'python': ['Python for Beginners – Coursera (Free)', 'Automate the Boring Stuff – Free Book'],
    'tensorflow': ['TensorFlow Developer Certificate – Google', 'Deep Learning Specialization – Coursera'],
    'machine learning': ['ML Specialization – Andrew Ng (Coursera)', 'FastAI Practical Deep Learning – Free'],
    'statistics': ['Statistics with Python – Coursera', 'Khan Academy Statistics – Free'],
    'sql': ['SQL for Data Science – Udemy', 'Mode Analytics SQL Tutorial – Free'],
    'react': ['React – The Complete Guide – Udemy', 'Official React Docs'],
    'docker': ['Docker Mastery – Udemy', 'Play with Docker – Free'],
    'aws': ['AWS Cloud Practitioner Free Training', 'A Cloud Guru: AWS Associate'],
    'javascript': ['JavaScript.info – Free', 'The Odin Project – Free Curriculum'],
    'data analysis': ['Data Analysis with Python – freeCodeCamp', 'Pandas Official Tutorial'],
    'deep learning': ['Deep Learning Specialization – Coursera', 'Fast.ai – Free Course'],
    'nlp': ['NLP Specialization – Coursera', 'Hugging Face Course – Free'],
    'linux': ['Linux Basics – edX (Free)', 'The Linux Command Line – Free Book'],
    'networking': ['Computer Networking – Coursera (Google)', 'Cisco NetAcad – Free'],
    'figma': ['UI/UX Design Bootcamp – Udemy', 'Figma Official Tutorials – Free'],
    'git': ['Git & GitHub Crash Course – freeCodeCamp', 'Pro Git Book – Free'],
    'kubernetes': ['Kubernetes for Beginners – KodeKloud', 'CNCF Training – Free'],
    'tableau': ['Tableau Desktop Specialist – Udemy', 'Tableau Public Free Training'],
}


def parse_skills(skills_text):
    """Parse comma/newline/semicolon separated skills into a cleaned list."""
    if not skills_text:
        return []
    parts = re.split(r'[,;\n]+', skills_text.lower())
    return [p.strip() for p in parts if p.strip()]


def match_student(student_skills, internships):
    """Original skill matcher – ranks internships by cosine similarity."""
    if not student_skills or not student_skills.strip():
        return [(i, 0.0) for i in internships]
    student_vec = model.encode([student_skills])
    scores = []
    for internship in internships:
        req = internship.skills_required or ''
        if not req.strip():
            scores.append((internship, 0.0))
            continue
        internship_vec = model.encode([req])
        score = float(cosine_similarity(student_vec, internship_vec)[0][0])
        scores.append((internship, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


# ─── 1. CAREER PATH PREDICTOR ─────────────────────────────────────────────────
def predict_career_paths(student_skills_text):
    """
    Predicts top career paths using sentence embeddings + cosine similarity
    against defined career skill profiles. Returns top 3 paths.
    """
    if not student_skills_text or not student_skills_text.strip():
        return []
    student_vec = model.encode([student_skills_text])
    student_skills_list = parse_skills(student_skills_text)
    results = []
    for career, data in CAREER_PATHS.items():
        career_skills_text = ', '.join(data['skills'])
        career_vec = model.encode([career_skills_text])
        score = float(cosine_similarity(student_vec, career_vec)[0][0])
        career_skills_list = data['skills']
        matching = [s for s in career_skills_list if any(s in st or st in s for st in student_skills_list)]
        missing = [s for s in career_skills_list if not any(s in st or st in s for st in student_skills_list)]
        results.append({
            'career': career,
            'score': round(score * 100, 1),
            'icon': data['icon'],
            'description': data['description'],
            'matching_skills': matching[:5],
            'missing_skills': missing[:5],
            'recommended_internships': data['internships'],
            'salary_range': data['salary_range'],
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:3]


# ─── 2. SKILL GAP ANALYZER ────────────────────────────────────────────────────
def analyze_skill_gap(student_skills_text, internship_skills_text):
    """
    Compares student skills vs internship required skills.
    Returns matched skills, missing skills, semantic score, courses, readiness.
    """
    student_skills = parse_skills(student_skills_text)
    required_skills = parse_skills(internship_skills_text)
    matched = []
    missing = []
    for skill in required_skills:
        found = any(skill in st or st in skill for st in student_skills)
        if found:
            matched.append(skill)
        else:
            missing.append(skill)
    score = 0.0
    if student_skills_text and internship_skills_text:
        s_vec = model.encode([student_skills_text])
        i_vec = model.encode([internship_skills_text])
        score = float(cosine_similarity(s_vec, i_vec)[0][0])
    match_pct = round((len(matched) / len(required_skills) * 100) if required_skills else 0, 1)
    courses = []
    for skill in missing:
        for key, recs in COURSE_MAP.items():
            if key in skill or skill in key:
                for rec in recs:
                    if rec not in courses:
                        courses.append(rec)
    return {
        'matched_skills': matched,
        'missing_skills': missing,
        'match_percentage': match_pct,
        'semantic_score': round(score * 100, 1),
        'recommended_courses': courses[:6],
        'readiness_level': 'High' if match_pct >= 70 else 'Medium' if match_pct >= 40 else 'Low',
        'readiness_color': 'success' if match_pct >= 70 else 'warning' if match_pct >= 40 else 'danger',
    }


# ─── 3. SUCCESS PREDICTOR ─────────────────────────────────────────────────────
def predict_success_probability(student_skills, internship_skills, certificates_count=0, experience_count=0):
    """
    Predicts internship success probability using a weighted scoring formula.
    Returns probability, breakdown, and verdict.
    """
    skill_score = 0.0
    if student_skills and internship_skills:
        s_vec = model.encode([student_skills])
        i_vec = model.encode([internship_skills])
        skill_score = float(cosine_similarity(s_vec, i_vec)[0][0])
    cert_score = min(certificates_count * 0.05, 0.20)
    exp_score = min(experience_count * 0.05, 0.15)
    profile_score = 0.15
    total = (skill_score * 0.50) + cert_score + exp_score + profile_score
    probability = round(min(total * 100, 97), 1)
    reasons = []
    if skill_score >= 0.7:
        reasons.append({'icon': '✅', 'text': 'Strong skill alignment with internship requirements', 'positive': True})
    elif skill_score >= 0.4:
        reasons.append({'icon': '⚠️', 'text': 'Moderate skill match – consider upskilling missing areas', 'positive': False})
    else:
        reasons.append({'icon': '❌', 'text': 'Low skill match – significant skill gaps detected', 'positive': False})
    if certificates_count >= 2:
        reasons.append({'icon': '✅', 'text': f'{certificates_count} verified certificates strengthen your profile', 'positive': True})
    elif certificates_count == 1:
        reasons.append({'icon': '⚠️', 'text': '1 certificate found – more certifications will boost your score', 'positive': False})
    else:
        reasons.append({'icon': '❌', 'text': 'No certificates – add relevant certifications to improve ranking', 'positive': False})
    if experience_count >= 1:
        reasons.append({'icon': '✅', 'text': f'{experience_count} prior internship experience(s) detected', 'positive': True})
    else:
        reasons.append({'icon': '⚠️', 'text': 'No prior internship experience – projects and courses help', 'positive': False})
    verdict_map = [
        (75, 'Excellent', 'success'),
        (55, 'Good', 'info'),
        (35, 'Fair', 'warning'),
        (0, 'Needs Improvement', 'danger'),
    ]
    verdict, verdict_color = next(
        (v, c) for threshold, v, c in verdict_map if probability >= threshold
    )
    return {
        'probability': probability,
        'skill_score': round(skill_score * 100, 1),
        'cert_score': round(cert_score * 100, 1),
        'exp_score': round(exp_score * 100, 1),
        'reasons': reasons,
        'verdict': verdict,
        'verdict_color': verdict_color,
    }


# ─── 4. RECOMMENDATION ENGINE ─────────────────────────────────────────────────
def recommend_internships(student_skills, all_internships, top_n=5):
    """Content-based recommendation engine using semantic similarity."""
    if not all_internships:
        return []
    scored = match_student(student_skills, all_internships)
    recommendations = []
    for internship, score in scored[:top_n]:
        gap = analyze_skill_gap(student_skills, internship.skills_required or '')
        recommendations.append({
            'internship': internship,
            'score': round(score * 100, 1),
            'matched_skills': gap['matched_skills'][:4],
            'missing_skills': gap['missing_skills'][:3],
            'readiness': gap['readiness_level'],
            'readiness_color': gap['readiness_color'],
        })
    return recommendations


# ─── 5. ALLOCATION OPTIMIZER ──────────────────────────────────────────────────
def optimize_allocation(students_data, internships):
    """
    Greedy stable-matching allocation optimizer.
    students_data: list of dicts {'id', 'name', 'skills', 'cert_count', 'exp_count'}
    Returns: list of allocation detail dicts and unallocated student IDs.
    """
    if not students_data or not internships:
        return [], []
    score_matrix = {}
    for student in students_data:
        sid = student['id']
        skills = student.get('skills', '')
        score_matrix[sid] = {}
        for internship in internships:
            req = internship.skills_required or ''
            if skills and req:
                s_vec = model.encode([skills])
                i_vec = model.encode([req])
                score = float(cosine_similarity(s_vec, i_vec)[0][0])
            else:
                score = 0.0
            bonus = min(student.get('cert_count', 0) * 0.02, 0.10)
            bonus += min(student.get('exp_count', 0) * 0.02, 0.08)
            score_matrix[sid][internship.id] = min(score + bonus, 1.0)

    capacity_used = {i.id: 0 for i in internships}
    capacity_limit = {i.id: (i.capacity or 1) for i in internships}

    def best_score(s_id):
        return max(score_matrix[s_id].values()) if score_matrix[s_id] else 0

    sorted_students = sorted(students_data, key=lambda s: best_score(s['id']), reverse=True)
    allocation_details = []
    unallocated = []
    for student in sorted_students:
        sid = student['id']
        ranked = sorted(internships, key=lambda i: score_matrix[sid].get(i.id, 0), reverse=True)
        allocated = False
        for internship in ranked:
            if capacity_used[internship.id] < capacity_limit[internship.id]:
                capacity_used[internship.id] += 1
                allocation_details.append({
                    'student_name': student['name'],
                    'student_id': sid,
                    'internship_title': internship.title,
                    'internship_id': internship.id,
                    'score': round(score_matrix[sid][internship.id] * 100, 1),
                })
                allocated = True
                break
        if not allocated:
            unallocated.append(student['name'])
    return allocation_details, unallocated


# ─── 6. PERSONALITY CULTURE MATCH ─────────────────────────────────────────────
def match_personality_culture(quiz_answers):
    """
    Matches student personality quiz answers to company culture types.
    quiz_answers: dict {risk_taking, teamwork, structure, creativity, pace} (1-5 each)
    """
    results = []
    for culture, data in CULTURE_TYPES.items():
        traits = data['traits']
        distance = sum((quiz_answers.get(k, 3) - traits[k]) ** 2 for k in traits) ** 0.5
        max_distance = (4 ** 2 * len(traits)) ** 0.5
        similarity = round((1 - distance / max_distance) * 100, 1)
        results.append({
            'culture': culture,
            'score': similarity,
            'icon': data['icon'],
            'description': data['description'],
            'examples': data['examples'],
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


# ─── 7. INTERVIEW SIMULATOR ───────────────────────────────────────────────────
def get_interview_question(skills_text, asked_ids=None):
    """Returns a relevant interview question based on student skills."""
    if asked_ids is None:
        asked_ids = []
    student_skills = parse_skills(skills_text)
    candidates = []
    for topic, questions in INTERVIEW_QUESTIONS.items():
        topic_relevant = any(topic in skill or skill in topic for skill in student_skills)
        for q in questions:
            q_id = abs(hash(q['q'])) % (10 ** 9)
            if q_id not in asked_ids:
                relevance = 2 if topic_relevant else 1
                candidates.append({**q, 'topic': topic, 'id': q_id, 'relevance': relevance})
    if not candidates:
        for q in INTERVIEW_QUESTIONS['general']:
            q_id = abs(hash(q['q'])) % (10 ** 9)
            if q_id not in asked_ids:
                candidates.append({**q, 'topic': 'general', 'id': q_id, 'relevance': 1})
    if not candidates:
        return None
    candidates.sort(key=lambda x: x['relevance'], reverse=True)
    return candidates[0]


def evaluate_interview_answer(question_text, student_answer, keywords):
    """
    Evaluates a student answer using keyword matching + semantic similarity.
    Returns score (0-10), feedback, pass/fail.
    """
    if not student_answer or len(student_answer.strip()) < 10:
        return {'score': 0, 'feedback': 'Answer is too short. Please provide a detailed response.', 'good': False}
    answer_lower = student_answer.lower()
    keyword_hits = sum(1 for kw in keywords if kw.lower() in answer_lower)
    keyword_score = (keyword_hits / len(keywords)) * 5 if keywords else 0
    q_vec = model.encode([question_text])
    a_vec = model.encode([student_answer])
    semantic_score = float(cosine_similarity(q_vec, a_vec)[0][0]) * 5
    total_score = round(min(keyword_score + semantic_score, 10), 1)
    missed_keywords = [k for k in keywords if k not in answer_lower]
    if total_score >= 8:
        feedback = 'Excellent answer! You demonstrated strong understanding of the concept.'
    elif total_score >= 6:
        feedback = f'Good answer! Consider also mentioning: {", ".join(missed_keywords[:3])}.'
    elif total_score >= 4:
        feedback = f'Decent attempt. Key concepts to improve: {", ".join(missed_keywords[:4])}.'
    else:
        feedback = f'Needs improvement. Focus on these key concepts: {", ".join(keywords[:4])}.'
    return {'score': total_score, 'feedback': feedback, 'good': total_score >= 6}


# ─── 8. GAMIFIED AI SCORE CALCULATOR ─────────────────────────────────────────
def calculate_ai_score(skills_text, certificates_count, experience_count, applications_count):
    """Calculates a gamified AI score for the student leaderboard."""
    skills = parse_skills(skills_text)
    skill_score = min(len(skills) * 20, 300)
    cert_score = min(certificates_count * 50, 250)
    exp_score = min(experience_count * 80, 250)
    activity_score = min(applications_count * 20, 200)
    total = skill_score + cert_score + exp_score + activity_score
    if total >= 700:
        level, level_color = 'Platinum', '#8b5cf6'
    elif total >= 450:
        level, level_color = 'Gold', '#f59e0b'
    elif total >= 250:
        level, level_color = 'Silver', '#6b7280'
    else:
        level, level_color = 'Bronze', '#b45309'
    return {
        'total': total,
        'skill_score': skill_score,
        'cert_score': cert_score,
        'exp_score': exp_score,
        'activity_score': activity_score,
        'level': level,
        'level_color': level_color,
        'skill_count': len(skills),
    }


# ─── 9. CERTIFICATE FRAUD DETECTOR ───────────────────────────────────────────

# Keywords that appear in real certificates
_CERT_KEYWORDS = [
    'certificate', 'certification', 'certify', 'certifies', 'certifying',
    'awarded', 'award', 'achievement', 'accomplish',
    'completion', 'completed', 'successfully', 'successfully completed',
    'hereby', 'this is to certify', 'presented to', 'is hereby awarded',
    'diploma', 'credential', 'authorized', 'in recognition',
    'has demonstrated', 'has successfully', 'is qualified',
]

# Issuer → domain tags for cross-check
_ISSUER_DOMAINS = {
    'cisco': ['networking', 'network', 'ccna', 'ccnp', 'cybersecurity', 'security'],
    'red hat': ['linux', 'rhcsa', 'rhce', 'openshift', 'ansible', 'devops'],
    'aws': ['cloud', 'amazon', 'aws', 's3', 'ec2', 'lambda', 'devops'],
    'amazon': ['cloud', 'aws', 'ecommerce', 'python', 'java', 'data'],
    'microsoft': ['azure', 'office', 'windows', 'dotnet', '.net', 'power bi', 'teams', 'excel'],
    'google': ['cloud', 'gcp', 'analytics', 'data', 'python', 'tensorflow', 'android', 'flutter'],
    'oracle': ['java', 'sql', 'database', 'mysql', 'cloud'],
    'ibm': ['data science', 'watson', 'cloud', 'python', 'ai', 'machine learning'],
    'coursera': [],  # accepts all topics
    'udemy': [],
    'edx': [],
    'nptel': [],
    'swayam': [],
    'linkedin learning': [],
    'infosys springboard': [],
    'internshala': [],
}


def _detect_issuer_from_text(text):
    """Scan extracted certificate text for known institution name patterns."""
    text_lower = text.lower()
    for pattern, key in _ISSUER_TEXT_PATTERNS:
        if pattern in text_lower:
            return key
    return None


def _get_institution_key(issuer_str):
    """Return the INSTITUTION_REGISTRY key matching a given issuer string, or None."""
    if not issuer_str:
        return None
    issuer_lower = issuer_str.lower()
    for key in sorted(INSTITUTION_REGISTRY.keys(), key=len, reverse=True):
        if key in issuer_lower:
            return key
    return None


def _check_cert_issuer_match(cert_name, issuing_org):
    """Detect if certificate topic is inconsistent with the issuing organization."""
    org_lower = (issuing_org or '').lower()
    cert_lower = (cert_name or '').lower()
    for issuer_key, domains in _ISSUER_DOMAINS.items():
        if issuer_key in org_lower and domains:
            if not any(d in cert_lower for d in domains):
                return False  # mismatch
    return True  # consistent or unknown issuer


def _analyze_cert_pdf(filepath, cert_name, issuing_org):
    """Extract text from PDF and verify it looks like a real certificate."""
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            raw_text = ' '.join(page.extract_text() or '' for page in pdf.pages).strip()
        text = raw_text.lower()

        if not text:
            return {
                'score_delta': -20,
                'detected_issuer': None,
                'flags': [{'type': 'warning', 'msg': 'PDF has no extractable text (image-based scan) – manual review needed'}],
            }

        flags = []
        score_delta = 0

        # --- Detect institution from text ---
        detected_issuer = _detect_issuer_from_text(text)

        # --- Keyword check ---
        hits = [kw for kw in _CERT_KEYWORDS if kw in text]
        if len(hits) >= 3:
            flags.append({'type': 'success', 'msg': f'File content verified: {len(hits)} certificate authenticity signals found in document'})
            score_delta += 15
        elif len(hits) >= 1:
            flags.append({'type': 'warning', 'msg': f'Only {len(hits)} certificate keyword(s) found – document may not be a formal certificate'})
            score_delta -= 10
        else:
            flags.append({'type': 'danger', 'msg': 'No certificate keywords found in file – this does not appear to be a certificate document'})
            score_delta -= 35

        # --- Certificate name check ---
        meaningful = [w for w in (cert_name or '').lower().split() if len(w) > 3]
        if meaningful:
            matched = sum(1 for w in meaningful if w in text)
            ratio = matched / len(meaningful)
            if ratio >= 0.6:
                flags.append({'type': 'success', 'msg': 'Certificate title confirmed in document text'})
                score_delta += 10
            elif ratio >= 0.3:
                flags.append({'type': 'warning', 'msg': 'Certificate title only partially matches document content'})
            else:
                flags.append({'type': 'danger', 'msg': 'Certificate title not found in document – possible metadata mismatch'})
                score_delta -= 15

        # --- Issuer check ---
        issuer_words = [w for w in (issuing_org or '').lower().split() if len(w) > 2]
        if issuer_words:
            issuer_hits = sum(1 for w in issuer_words if w in text)
            if issuer_hits / len(issuer_words) >= 0.5:
                flags.append({'type': 'success', 'msg': 'Issuing organization name confirmed in document'})
                score_delta += 5
            else:
                flags.append({'type': 'warning', 'msg': 'Issuing organization not clearly found in document – possible mismatch'})
                score_delta -= 10

        return {'score_delta': score_delta, 'flags': flags, 'detected_issuer': detected_issuer}

    except Exception as e:
        return {
            'score_delta': 0,
            'detected_issuer': None,
            'flags': [{'type': 'warning', 'msg': f'Could not read PDF: {str(e)[:80]}'}],
        }


def _analyze_cert_image(filepath, cert_name, issuing_org):
    """Analyze certificate image dimensions and color profile for authenticity."""
    try:
        from PIL import Image
        img = Image.open(filepath)
        width, height = img.size
        flags = []
        score_delta = 0

        # Too small = suspicious
        if width < 200 or height < 200:
            flags.append({'type': 'danger', 'msg': f'Image resolution ({width}×{height}px) is too low to be a real certificate'})
            score_delta -= 35
            return {'score_delta': score_delta, 'flags': flags, 'detected_issuer': None}

        # Aspect ratio: real certificates are A4 (1.41), letter (1.29), or landscape versions thereof
        ratio = max(width, height) / min(width, height)
        if 1.15 <= ratio <= 1.65:
            flags.append({'type': 'success', 'msg': f'Image dimensions ({width}×{height}px) match standard A4/letter certificate format'})
            score_delta += 8
        elif ratio > 2.2:
            flags.append({'type': 'danger', 'msg': f'Unusual image ratio ({ratio:.1f}:1) – standard certificates are not this shape'})
            score_delta -= 20
        else:
            flags.append({'type': 'warning', 'msg': 'Image dimensions are non-standard – check if this is the full certificate'})
            score_delta -= 5

        # Color analysis: certificates have predominantly light/white backgrounds
        rgb = img.convert('RGB').resize((120, 120))
        pixels = list(rgb.getdata())
        light = sum(1 for r, g, b in pixels if r > 200 and g > 200 and b > 200)
        light_pct = light / len(pixels)

        if light_pct >= 0.45:
            flags.append({'type': 'success', 'msg': f'Background analysis: {int(light_pct*100)}% light tones – consistent with a document/certificate'})
            score_delta += 7
        elif light_pct >= 0.20:
            flags.append({'type': 'warning', 'msg': f'Background analysis: only {int(light_pct*100)}% light tones – may not be a standard certificate'})
            score_delta -= 20
        else:
            flags.append({'type': 'danger', 'msg': f'Background analysis: {int(light_pct*100)}% light tones – image looks like a photo, not a certificate document'})
            score_delta -= 45

        # Note: issuer cannot be detected from images without OCR
        flags.append({'type': 'warning', 'msg': 'Issuer cannot be auto-detected from image files – upload as PDF for full institution verification'})

        return {'score_delta': score_delta, 'flags': flags, 'detected_issuer': None}

    except Exception as e:
        return {
            'score_delta': 0,
            'detected_issuer': None,
            'flags': [{'type': 'warning', 'msg': f'Could not analyze image: {str(e)[:80]}'}],
        }


def _check_certificate_file(file_path, cert_name, issuing_org):
    """Dispatch file to appropriate analyzer. Returns score_delta, flags, and detected_issuer."""
    import os
    if not os.path.exists(file_path):
        return {'score_delta': -5, 'detected_issuer': None, 'flags': [{'type': 'warning', 'msg': 'Certificate file unavailable for deep scan'}]}

    size = os.path.getsize(file_path)
    if size < 1000:
        return {
            'score_delta': -30,
            'detected_issuer': None,
            'flags': [{'type': 'danger', 'msg': 'Certificate file is under 1 KB – too small to be a real certificate'}],
        }

    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return _analyze_cert_pdf(file_path, cert_name, issuing_org)
    elif ext in ('.png', '.jpg', '.jpeg', '.webp', '.bmp'):
        return _analyze_cert_image(file_path, cert_name, issuing_org)
    else:
        return {
            'score_delta': -5,
            'detected_issuer': None,
            'flags': [{'type': 'warning', 'msg': f'File format ({ext or "unknown"}) cannot be deep-scanned – manual review needed'}],
        }


def verify_certificate(cert_name, issuing_org, issue_date, expiry_date=None, file_path=None):
    """
    AI certificate authenticity engine.
    Checks: trusted issuer · issuer-domain fit · suspicious name · date validity ·
            file content (PDF text extraction or image analysis) · institution detection.
    Returns: verification status, trust score, flags, institution_info, detected_issuer.
    """
    from datetime import date, datetime
    flags = []
    trust_score = 100

    # Look up institution info from the claimed issuer
    institution_info = INSTITUTION_REGISTRY.get(_get_institution_key(issuing_org))

    # 1. Trusted issuer registry
    issuer_lower = (issuing_org or '').lower()
    is_trusted = any(t in issuer_lower for t in TRUSTED_ISSUERS)
    if not is_trusted:
        flags.append({'type': 'warning', 'msg': 'Issuing organization not in trusted registry – verify manually'})
        trust_score -= 20

    # 2. Issuer ↔ certificate-topic consistency
    if not _check_cert_issuer_match(cert_name, issuing_org):
        flags.append({'type': 'warning', 'msg': 'Certificate topic seems unusual for this issuer – verify authenticity'})
        trust_score -= 15

    # 3. Suspicious keywords in certificate name
    suspicious_words = ['fake', 'dummy', 'test', 'sample', 'template']
    if any(sw in (cert_name or '').lower() for sw in suspicious_words):
        flags.append({'type': 'danger', 'msg': 'Certificate name contains suspicious keywords'})
        trust_score -= 40

    # 4. Date validation
    today = date.today()
    if issue_date:
        if isinstance(issue_date, str):
            try:
                issue_date = datetime.strptime(issue_date, '%Y-%m-%d').date()
            except Exception:
                issue_date = None
        if issue_date and issue_date > today:
            flags.append({'type': 'danger', 'msg': 'Issue date is in the future – possible fraud'})
            trust_score -= 50
        if issue_date and issue_date.year < 2000:
            flags.append({'type': 'warning', 'msg': 'Very old certificate – consider renewing'})
            trust_score -= 10
    if expiry_date:
        if isinstance(expiry_date, str):
            try:
                expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
            except Exception:
                expiry_date = None
        if expiry_date and expiry_date < today:
            flags.append({'type': 'warning', 'msg': 'Certificate has expired'})
            trust_score -= 15

    # 5. Deep file analysis + institution detection
    detected_issuer = None
    issuer_match = None

    if file_path:
        file_result = _check_certificate_file(file_path, cert_name, issuing_org)
        trust_score += file_result['score_delta']
        flags.extend(file_result['flags'])
        detected_issuer = file_result.get('detected_issuer')

        if detected_issuer:
            claimed_key = _get_institution_key(issuing_org)
            detected_name = INSTITUTION_REGISTRY[detected_issuer]['name']
            if claimed_key == detected_issuer:
                issuer_match = True
                flags.append({'type': 'success', 'msg': f'Institution confirmed: "{detected_name}" detected in document – matches claimed issuer'})
                trust_score += 10
            elif claimed_key is None:
                issuer_match = False
                flags.append({'type': 'warning', 'msg': f'Document references "{detected_name}" but claimed issuer "{issuing_org}" is unknown – consider updating'})
                trust_score -= 10
            else:
                issuer_match = False
                claimed_name = INSTITUTION_REGISTRY.get(claimed_key, {}).get('name', issuing_org)
                flags.append({'type': 'danger', 'msg': f'Issuer mismatch: document contains "{detected_name}" but claimed issuer is "{claimed_name}"'})
                trust_score -= 35
    else:
        flags.append({'type': 'warning', 'msg': 'No certificate file uploaded – upload the PDF for institution detection and deep AI scan'})
        trust_score -= 15

    trust_score = max(0, min(100, trust_score))

    # If no issues found at all, add a clean bill of health
    if not any(f['type'] in ('warning', 'danger') for f in flags):
        flags.insert(0, {'type': 'success', 'msg': 'All checks passed – certificate appears authentic'})

    if trust_score >= 80:
        status, status_color = 'Verified', 'success'
    elif trust_score >= 50:
        status, status_color = 'Suspicious', 'warning'
    else:
        status, status_color = 'Flagged', 'danger'

    return {
        'status': status,
        'status_color': status_color,
        'trust_score': trust_score,
        'flags': flags,
        'is_trusted_issuer': is_trusted,
        'institution_info': institution_info,
        'detected_issuer': detected_issuer,
        'issuer_match': issuer_match,
    }


# ─── 10. AI RESUME SCANNER ────────────────────────────────────────────────────

# Comprehensive skill keyword dictionary grouped by domain
SKILL_KEYWORDS = [
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'ruby', 'go', 'rust',
    'kotlin', 'swift', 'php', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell',
    'dart', 'elixir', 'haskell', 'julia', 'lua', 'groovy', 'objective-c',
    # Web Frontend
    'html', 'css', 'react', 'angular', 'vue', 'next.js', 'nuxt.js', 'svelte', 'bootstrap',
    'tailwind', 'sass', 'scss', 'jquery', 'webpack', 'vite', 'graphql', 'redux', 'mobx',
    # Web Backend
    'node.js', 'express', 'django', 'flask', 'fastapi', 'spring boot', 'laravel', 'rails',
    'asp.net', 'nestjs', 'rest api', 'soap', 'grpc',
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'sqlite', 'redis', 'cassandra', 'dynamodb',
    'firebase', 'oracle', 'elasticsearch', 'neo4j', 'supabase',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'terraform', 'ansible',
    'jenkins', 'github actions', 'gitlab ci', 'circleci', 'helm', 'prometheus', 'grafana',
    'devops', 'ci/cd', 'linux', 'nginx', 'apache', 'serverless',
    # AI / ML / Data
    'machine learning', 'deep learning', 'neural networks', 'nlp', 'computer vision',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
    'seaborn', 'opencv', 'hugging face', 'langchain', 'llm', 'generative ai', 'data analysis',
    'data science', 'statistics', 'regression', 'classification', 'clustering', 'reinforcement learning',
    'transformers', 'bert', 'gpt', 'xgboost', 'lightgbm',
    # Mobile
    'android', 'ios', 'react native', 'flutter', 'xamarin',
    # Version Control & Tools
    'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'trello', 'figma',
    'adobe xd', 'sketch', 'postman', 'swagger', 'vscode',
    # Security
    'cybersecurity', 'pen testing', 'ethical hacking', 'owasp', 'cryptography', 'networking',
    'firewalls', 'ssl', 'oauth', 'jwt', 'siem', 'nmap', 'wireshark',
    # Data Visualization & BI
    'tableau', 'power bi', 'excel', 'google analytics', 'looker', 'metabase', 'qlik',
    # Soft / Business
    'agile', 'scrum', 'product management', 'leadership', 'communication', 'problem solving',
    'ui/ux', 'user research', 'design thinking', 'ms office', 'word', 'powerpoint',
    # Emerging / Other
    'blockchain', 'solidity', 'web3', 'unity', 'unreal engine', 'arkit', 'arcore',
    'iot', 'raspberry pi', 'arduino', 'ros', 'autocad', 'solidworks',
]

# Regex patterns for detecting portfolio / social profile links
_URL_LINKEDIN = re.compile(
    r'(https?://)?(www\.)?linkedin\.com/in/[\w\-]+/?', re.IGNORECASE
)
_URL_GITHUB = re.compile(
    r'(https?://)?(www\.)?github\.com/[\w\-]+/?', re.IGNORECASE
)
_URL_PORTFOLIO = re.compile(
    r'https?://(?!linkedin|github)[\w\-]+\.[\w\.\-/]+', re.IGNORECASE
)


def _extract_text_from_pdf(path):
    """Extract plain text from a PDF file using pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return '\n'.join(text_parts)
    except Exception:
        return ''


def _extract_text_from_docx(path):
    """Extract plain text from a DOCX file using python-docx."""
    try:
        from docx import Document
        doc = Document(path)
        return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ''


def _detect_skills_from_text(text):
    """Match SKILL_KEYWORDS against resume text (case-insensitive, word-boundary aware)."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        # Use word-boundary-style matching to avoid false positives (e.g. 'c' in 'each')
        escaped = re.escape(skill)
        pattern = r'(?<![a-z0-9])' + escaped + r'(?![a-z0-9])'
        if re.search(pattern, text_lower):
            found.append(skill)
    # Capitalise for nice display
    return [s.title() if len(s) <= 3 else s.capitalize() for s in found]


def _detect_links_from_text(text):
    """Extract LinkedIn, GitHub, and other portfolio URLs from resume text."""
    linkedin = None
    github = None
    portfolio = None

    m = _URL_LINKEDIN.search(text)
    if m:
        raw = m.group(0)
        if not raw.startswith('http'):
            raw = 'https://' + raw
        linkedin = raw.rstrip('/')

    m = _URL_GITHUB.search(text)
    if m:
        raw = m.group(0)
        if not raw.startswith('http'):
            raw = 'https://' + raw
        github = raw.rstrip('/')

    # First non-linkedin/github URL as portfolio
    for m in _URL_PORTFOLIO.finditer(text):
        url = m.group(0)
        if 'linkedin' not in url.lower() and 'github' not in url.lower():
            portfolio = url
            break

    return {'linkedin': linkedin, 'github': github, 'portfolio': portfolio}


def extract_resume_data(absolute_file_path):
    """
    AI resume scanner: extracts text from a PDF or DOCX, then detects
    skills using NLP keyword matching and portfolio links using regex.

    Returns:
        {
          'skills': [...],
          'linkedin_url': str | None,
          'github_url': str | None,
          'portfolio_url': str | None,
          'text_preview': str,
          'success': bool,
          'error': str | None,
        }
    """
    import os
    ext = os.path.splitext(absolute_file_path)[1].lower()

    if ext == '.pdf':
        text = _extract_text_from_pdf(absolute_file_path)
    elif ext in ('.docx',):
        text = _extract_text_from_docx(absolute_file_path)
    else:
        return {
            'skills': [], 'linkedin_url': None, 'github_url': None,
            'portfolio_url': None, 'text_preview': '',
            'success': False, 'error': 'Unsupported file type. Upload PDF or DOCX for AI scan.',
        }

    if not text.strip():
        return {
            'skills': [], 'linkedin_url': None, 'github_url': None,
            'portfolio_url': None, 'text_preview': '',
            'success': False, 'error': 'Could not extract text from file. Ensure it is not a scanned image PDF.',
        }

    skills = _detect_skills_from_text(text)
    links = _detect_links_from_text(text)
    preview = ' '.join(text.split())[:300]  # first 300 chars for display

    return {
        'skills': skills,
        'linkedin_url': links['linkedin'],
        'github_url': links['github'],
        'portfolio_url': links['portfolio'],
        'text_preview': preview,
        'success': True,
        'error': None,
    }

