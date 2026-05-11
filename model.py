import pandas as pd
import numpy as np
import pickle, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

MODEL_PATH = 'model/loan_model.pkl'
DATASET_PATH = 'dataset/loan_data.csv'

def preprocess(data: dict) -> np.ndarray:
    emp_map = {'Salaried': 3, 'Business': 2, 'Self Employed': 1, 'Unemployed': 0}
    edu_map = {'Graduate': 1, 'Not Graduate': 0}
    prop_map = {'Urban': 2, 'Semiurban': 1, 'Rural': 0}
    married_map = {'Yes': 1, 'No': 0}

    income = float(data.get('income', 0))
    coincome = float(data.get('coincome', 0))
    lamt = float(data.get('lamt', 0))
    lterm = float(data.get('lterm', 360))
    cibil = float(data.get('cibil', 0))
    ch = float(data.get('ch', 0))
    emi = float(data.get('emi', 0))
    assets = float(data.get('assets', 0))
    exp = float(data.get('exp', 0))
    age = float(data.get('age', 30))
    dep = float(data.get('dep', 0))

    total_income = income + coincome
    monthly_emi = (lamt / lterm) + emi if lterm > 0 else 0
    emi_ratio = monthly_emi / total_income if total_income > 0 else 1
    lti_ratio = lamt / (total_income * 12) if total_income > 0 else 999
    asset_ratio = assets / lamt if lamt > 0 else 0

    features = [
        cibil / 900,
        ch,
        emi_ratio,
        lti_ratio,
        emp_map.get(data.get('emp', ''), 0) / 3,
        edu_map.get(data.get('edu', ''), 0),
        asset_ratio,
        exp / 30,
        age / 70,
        dep / 3,
        married_map.get(data.get('married', 'No'), 0),
        prop_map.get(data.get('prop', ''), 0) / 2,
    ]
    return np.array(features).reshape(1, -1)

def predict(data: dict) -> dict:
    if not os.path.exists(MODEL_PATH):
        train_model()

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    X = preprocess(data)
    prob = model.predict_proba(X)[0]
    approved = int(prob[1] >= 0.5)
    score = round(float(prob[1]) * 100, 1)

    importances = model.feature_importances_
    feat_names = ['CIBIL Score','Credit History','EMI Ratio','LTI Ratio',
                  'Employment','Education','Assets','Experience','Age','Dependents','Married','Property']
    feat_importance = {
        feat_names[i]: round(float(importances[i]) * 100, 1)
        for i in range(len(feat_names))
    }

    return {
        'approved': approved,
        'probability': score,
        'label': 'Approved' if approved else 'Rejected',
        'feature_importance': feat_importance,
        'applicant': data.get('name', 'Applicant')
    }

def train_model() -> float:
    """Train on real dataset or generate synthetic training data."""
    os.makedirs('model', exist_ok=True)

    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        # Encode categoricals
        le = LabelEncoder()
        for col in df.select_dtypes(include='object').columns:
            if col != 'Loan_Status':
                df[col] = le.fit_transform(df[col].astype(str))
        df['Loan_Status'] = (df['Loan_Status'] == 'Y').astype(int)
        df.dropna(inplace=True)
        X = df.drop('Loan_Status', axis=1)
        y = df['Loan_Status']
    else:
        # Synthetic training data (12 features)
        np.random.seed(42)
        n = 2000
        cibil = np.random.uniform(0.3, 1.0, n)
        ch = np.random.binomial(1, 0.8, n)
        emi_r = np.random.uniform(0.1, 0.8, n)
        lti = np.random.uniform(0.5, 10, n)
        emp = np.random.choice([0,1,2,3], n) / 3
        edu = np.random.binomial(1, 0.65, n)
        assets = np.random.uniform(0, 3, n)
        exp = np.random.uniform(0, 1, n)
        age = np.random.uniform(0.25, 0.8, n)
        dep = np.random.choice([0,1,2,3], n) / 3
        married = np.random.binomial(1, 0.6, n)
        prop = np.random.choice([0,1,2], n) / 2

        X = np.column_stack([cibil,ch,emi_r,lti,emp,edu,assets,exp,age,dep,married,prop])
        score = (cibil*0.35 + ch*0.20 + (1-emi_r)*0.20 + (1/(lti+0.1))*0.1 +
                 emp*0.05 + edu*0.03 + assets*0.04 + exp*0.03)
        y = (score > np.percentile(score, 40)).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    print(f"Model trained. Accuracy: {acc*100:.2f}%")
    return round(acc * 100, 2)

if __name__ == '__main__':
    acc = train_model()
    print(f"Accuracy: {acc}%")