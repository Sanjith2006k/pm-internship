from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_student(student_skills, internships):
    student_vec = model.encode([student_skills])
    
    scores = []
    for internship in internships:
        internship_vec = model.encode([internship.skills_required])
        score = cosine_similarity(student_vec, internship_vec)[0][0]
        scores.append((internship, score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores