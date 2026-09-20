import os
import joblib
import pandas as pd
import numpy as np
import shap


# ==========================================
# Load model
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "final_xgboost_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ==========================================
# Model features
# ==========================================

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


# ==========================================
# SHAP explainer
# ==========================================

explainer = shap.TreeExplainer(model)


# ==========================================
# Prediction function
# ==========================================

def predict_defect(metrics):

    # Create model input

    input_data = pd.DataFrame(
        [[metrics[feature] for feature in FEATURES]],
        columns=FEATURES
    )


    # ==========================================
    # Predict probability
    # ==========================================

    probability = model.predict_proba(
        input_data
    )[0][1]


    # ==========================================
    # Risk level
    # ==========================================

    if probability < 0.30:

        risk = "Low"

    elif probability < 0.70:

        risk = "Medium"

    else:

        risk = "High"


    # ==========================================
    # Prediction threshold
    # ==========================================

    if probability >= 0.20:

        prediction = "Defect Predicted"

    else:

        prediction = "No Defect Predicted"


    # ==========================================
    # SHAP values
    # ==========================================

    shap_values = explainer.shap_values(
        input_data
    )


    # Convert to NumPy array

    shap_values = np.asarray(
        shap_values
    )


    # Handle possible XGBoost SHAP output shape

    if shap_values.ndim == 3:

        shap_values = shap_values[:, :, 1]


    shap_values = shap_values.reshape(-1)


    # ==========================================
    # Find top 5 factors
    # ==========================================

    absolute_values = np.abs(
        shap_values
    )


    top_indices = np.argsort(
        absolute_values
    )[::-1][:5]


    top_factors = []


    for index in top_indices:

        feature = FEATURES[index]

        feature_value = float(
            input_data.iloc[0][feature]
        )

        shap_value = float(
            shap_values[index]
        )


        if shap_value > 0:

            direction = "increases"

        else:

            direction = "decreases"


        top_factors.append({

            "feature": feature,

            "value": round(
                feature_value,
                2
            ),

            "impact": round(
                abs(shap_value),
                4
            ),

            "direction": direction

        })


    # ==========================================
    # Return result
    # ==========================================

    return {

        "prediction": prediction,

        "defect_probability": round(
            float(probability) * 100,
            2
        ),

        "risk_level": risk,

        "top_factors": top_factors

    }