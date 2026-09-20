import os
import joblib
import pandas as pd


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "data",
    "final_xgboost_model.pkl"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# Feature order used during model training
# --------------------------------------------------

FEATURES = [
    "loc",
    "v(g)",
    "ev(g)",
    "iv(g)",
    "n",
    "v",
    "l",
    "d",
    "i",
    "e",
    "b",
    "t",
    "lOCode",
    "lOComment",
    "lOBlank",
    "locCodeAndComment",
    "uniq_Op",
    "uniq_Opnd",
    "total_Op",
    "total_Opnd",
    "branchCount"
]


# --------------------------------------------------
# Prediction function
# --------------------------------------------------

def predict_defect(metrics):

    # Create dataframe in the exact feature order
    input_data = pd.DataFrame(
        [[metrics[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    # Get probability of defect
    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    # Project threshold
    if probability >= 0.20:
        prediction = "Defect Predicted"
    else:
        prediction = "No Defect Predicted"

    # Risk level
    if probability < 0.30:
        risk_level = "Low"
    elif probability < 0.70:
        risk_level = "Medium"
    else:
        risk_level = "High"

    # SHAP temporarily disabled for Vercel deployment
    top_factors = []

    return {
        "prediction": prediction,
        "defect_probability": round(probability * 100, 2),
        "risk_level": risk_level,
        "top_factors": top_factors
    }

