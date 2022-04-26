from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_recommended_jobs(job_description, skill):
    """
    To get similarity between jobs required skills 
    and user's resume skills using cosine similarity
    """
    vectorizer = TfidfVectorizer()
    desc_vector = vectorizer.fit_transform(job_description)
    skill_vecor = vectorizer.transform(skill)
    similarity = cosine_similarity(desc_vector,skill_vecor)
    return similarity


def match_location(organization, candidate):
    """
    To get similarity between location of user profile  
    and organizaiton profile using cosine similarity
    """
    vectorizer = TfidfVectorizer()
    org_vector = vectorizer.fit_transform(organization)
    candidate_vecor = vectorizer.transform(candidate)
    similarity = cosine_similarity(org_vector,candidate_vecor)
    return similarity