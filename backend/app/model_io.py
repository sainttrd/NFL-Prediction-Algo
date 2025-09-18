import os, joblib

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), 'model_artifacts')
MODEL_PATH = os.path.join(ARTIFACT_DIR, 'model.pkl')
VERSION_PATH = os.path.join(ARTIFACT_DIR, 'version.txt')

os.makedirs(ARTIFACT_DIR, exist_ok=True)

def save_model(model, version: str):
    joblib.dump(model, MODEL_PATH)
    with open(VERSION_PATH, 'w') as f:
        f.write(version)

def load_model():
    from sklearn.linear_model import LogisticRegression
    if not os.path.exists(MODEL_PATH):
        # fallback baseline
        m = LogisticRegression()
        return m, 'baseline-dev'
    model = joblib.load(MODEL_PATH)
    version = 'unknown'
    if os.path.exists(VERSION_PATH):
        version = open(VERSION_PATH).read().strip()
    return model, version
