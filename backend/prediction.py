import os
import joblib
import pandas as pd


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "final_xgboost_model.pkl"
)


# Load trained XGBoost model
model = joblib.load(MODEL_PATH)


# Exact feature order used during training
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


def predict_defect(metrics):
    """
    Predict software defect probability from extracted metrics.
    """

    input_data = pd.DataFrame(
        [[metrics[feature] for feature in FEATURES]],
        columns=FEATURES
    )

    probability = model.predict_proba(input_data)[0][1]

    if probability < 0.30:
        risk = "Low"
    elif probability < 0.70:
        risk = "Medium"
    else:
        risk = "High"

    prediction = (
        "Defect Predicted"
        if probability >= 0.20
        else "No Defect Predicted"
    )

    return {
        "prediction": prediction,
        "defect_probability": round(float(probability) * 100, 2),
        "risk_level": risk
    }