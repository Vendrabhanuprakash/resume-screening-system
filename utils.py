import re
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_path):

    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        text += page.extract_text()

    return text


def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text


def calculate_similarity(resume_text, jd_text):

    texts = [resume_text, jd_text]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return round(similarity[0][0] * 100, 2)


def skill_analysis(resume_text, jd_text):

    resume_words = set(resume_text.split())

    jd_words = set(jd_text.split())

    matching_skills = list(
        resume_words.intersection(jd_words)
    )

    missing_skills = list(
        jd_words.difference(resume_words)
    )

    return matching_skills, missing_skills