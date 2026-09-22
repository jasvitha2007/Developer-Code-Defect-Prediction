import os
import joblib
import numpy as np
import shap

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "data",
    "final_xgboost_model.pkl"
)

model = joblib.load(MODEL_PATH)

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


# Create SHAP explainer once
explainer = shap.TreeExplainer(model)


def predict_defect(metrics):

    # -----------------------------
    # Prepare model input
    # -----------------------------

    values = [
        float(metrics[feature])
        for feature in FEATURES
    ]

    input_data = np.array(
        [values],
        dtype=np.float32
    )


    # -----------------------------
    # Model prediction
    # -----------------------------

    probability = float(
        model.predict_proba(
            input_data
        )[0][1]
    )


    # -----------------------------
    # Prediction threshold
    # -----------------------------

    if probability >= 0.20:
        prediction = "Defect Predicted"
    else:
        prediction = "No Defect Predicted"


    # -----------------------------
    # Risk level
    # -----------------------------

    if probability < 0.30:
        risk_level = "Low"

    elif probability < 0.70:
        risk_level = "Medium"

    else:
        risk_level = "High"


    # -----------------------------
    # SHAP explanation
    # -----------------------------

    shap_values = explainer.shap_values(
        input_data
    )


    # XGBoost binary classification
    # normally returns shape:
    # (1, number_of_features)

    shap_values = np.asarray(
        shap_values
    )


    if shap_values.ndim == 3:
        shap_values = shap_values[0, :, 1]

    elif shap_values.ndim == 2:
        shap_values = shap_values[0]

    else:
        shap_values = shap_values.flatten()


    # -----------------------------
    # Create factor list
    # -----------------------------

    factors = []

    for feature, value, shap_value in zip(
        FEATURES,
        values,
        shap_values
    ):

        factors.append(
            {
                "feature": feature,
                "value": round(
                    float(value),
                    2
                ),
                "shap_value": round(
                    float(shap_value),
                    4
                )
            }
        )


    # Strongest factors first
    factors.sort(
        key=lambda item: abs(
            item["shap_value"]
        ),
        reverse=True
    )


    # Only show top 5
    top_factors = factors[:5]


    # -----------------------------
    # Final result
    # -----------------------------

    return {
        "prediction": prediction,

        "defect_probability": round(
            probability * 100,
            2
        ),

        "risk_level": risk_level,

        "top_factors": top_factors
    }