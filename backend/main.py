import sys
import os

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# ==========================================
# Project paths
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)


# Add src to Python path

if SRC_DIR not in sys.path:

    sys.path.insert(
        0,
        SRC_DIR
    )


# ==========================================
# Imports
# ==========================================

from .metric_extractor import extract_metrics
from prediction import predict_defect


# ==========================================
# FastAPI application
# ==========================================

app = FastAPI(
    title="AI Software Defect Predictor",
    description="ML-based software defect prediction using XGBoost",
    version="1.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================
# Manual prediction model
# ==========================================

class ManualMetrics(BaseModel):

    loc: float
    v_g: float
    ev_g: float
    iv_g: float
    n: float
    v: float
    l: float
    d: float
    i: float
    e: float
    b: float
    t: float
    lOCode: float
    lOComment: float
    lOBlank: float
    locCodeAndComment: float
    uniq_Op: float
    uniq_Opnd: float
    total_Op: float
    total_Opnd: float
    branchCount: float


# ==========================================
# Root endpoint
# ==========================================

@app.get("/")
def root():
    frontend_path = os.path.join(BASE_DIR, "frontend", "index.html")
    return FileResponse(frontend_path)


# ==========================================
# Python source-code prediction
# ==========================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    # Check file extension

    if not file.filename.lower().endswith(".py"):

        raise HTTPException(
            status_code=400,
            detail="Please upload a Python (.py) source code file."
        )


    # Read uploaded file

    content = await file.read()


    # Decode source code

    try:

        code = content.decode("utf-8")

    except UnicodeDecodeError:

        raise HTTPException(
            status_code=400,
            detail="Unable to read the uploaded file."
        )


    # ==========================================
    # Extract metrics
    # ==========================================

    try:

        metrics = extract_metrics(code)

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unable to analyze source code: {str(error)}"
            )
        )


    # ==========================================
    # ML prediction + SHAP
    # ==========================================

    try:

        result = predict_defect(metrics)

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Prediction failed: {str(error)}"
            )
        )


    # ==========================================
    # API response
    # ==========================================

    return {

        "filename": file.filename,

        "prediction": result["prediction"],

        "defect_probability":
            result["defect_probability"],

        "risk_level":
            result["risk_level"],

        "top_factors":
            result["top_factors"],

        "metrics": metrics
    }


# ==========================================
# Manual prediction endpoint
# ==========================================

@app.post("/predict-manual")
def predict_manual(
    metrics: ManualMetrics
):

    metric_data = {

        "loc": metrics.loc,

        "v(g)": metrics.v_g,

        "ev(g)": metrics.ev_g,

        "iv(g)": metrics.iv_g,

        "n": metrics.n,

        "v": metrics.v,

        "l": metrics.l,

        "d": metrics.d,

        "i": metrics.i,

        "e": metrics.e,

        "b": metrics.b,

        "t": metrics.t,

        "lOCode": metrics.lOCode,

        "lOComment": metrics.lOComment,

        "lOBlank": metrics.lOBlank,

        "locCodeAndComment":
            metrics.locCodeAndComment,

        "uniq_Op": metrics.uniq_Op,

        "uniq_Opnd": metrics.uniq_Opnd,

        "total_Op": metrics.total_Op,

        "total_Opnd": metrics.total_Opnd,

        "branchCount": metrics.branchCount
    }


    return predict_defect(metric_data)