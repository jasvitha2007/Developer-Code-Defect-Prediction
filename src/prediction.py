import os
import joblib
import numpy as np


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
# Prediction
# --------------------------------------------------

def predict_defect(metrics):

    values = [
        float(metrics[feature])
        for feature in FEATURES
    ]

    input_data = np.array(
        [values],
        dtype=np.float32
    )

    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    if probability >= 0.20:
        prediction = "Defect Predicted"
    else:
        prediction = "No Defect Predicted"

    if probability < 0.30:
        risk_level = "Low"
    elif probability < 0.70:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "prediction": prediction,
        "defect_probability": round(probability * 100, 2),
        "risk_level": risk_level,
        "top_factors": []
    }

