import joblib

from app.config.config import settings


def compute_embedding(text: str) -> list[float]:
    model_file = settings.RECOMMENDATION_MODEL_FILE
    tfidf = joblib.load(model_file)
    embedding = tfidf.transform([text]).toarray()[0]
    return embedding
