# AI Software Defect Predictor

An ML-based software defect prediction system that analyzes Python source code, extracts software engineering metrics, and predicts the probability and risk of software defects using XGBoost.

## Project Overview

Software defects can increase maintenance cost and reduce software reliability. This project uses machine learning to identify software modules that may be more likely to contain defects.

The system automatically:

1. Accepts a Python source-code file
2. Extracts software engineering metrics
3. Processes the extracted metrics
4. Uses an XGBoost classification model
5. Predicts defect probability
6. Assigns a risk level
7. Provides SHAP-based explanations for the prediction

## Key Features

- Automatic Python source-code analysis
- Software metric extraction using Radon
- Machine learning based defect prediction
- XGBoost classification
- Class imbalance analysis
- Hyperparameter tuning
- Probability-based prediction
- Risk-level classification
- SHAP explainability
- FastAPI backend
- Simple web-based frontend

## Dataset

The project uses the **NASA JM1 software defect dataset** obtained from Kaggle.

Dataset source:

https://www.kaggle.com/datasets/semustafacevik/software-defect-prediction

The dataset contains software engineering metrics such as:

- Lines of Code
- Cyclomatic Complexity
- Halstead Volume
- Difficulty
- Effort
- Operators
- Operands
- Branch Count
- Comment and blank-line metrics

The target variable is:

- `0` → No defect
- `1` → Defect

## Machine Learning Pipeline

NASA JM1 Dataset
        ↓
Data Cleaning
        ↓
Duplicate Removal
        ↓
Missing Value Handling
        ↓
Exploratory Data Analysis
        ↓
Feature Analysis
        ↓
Train/Test Split
        ↓
Feature Scaling
        ↓
Class Imbalance Handling
        ↓
Model Training
        ↓
Model Comparison
        ↓
Hyperparameter Tuning
        ↓
Final XGBoost Model
        ↓
SHAP Explainability
        ↓
Source Code Prediction

## Models Compared

The project evaluates multiple machine learning algorithms:

Logistic Regression
Random Forest
Gradient Boosting
XGBoost
Support Vector Machine

The models were evaluated using:

Accuracy
Precision
Recall
F1 Score
ROC-AUC

Because the dataset is imbalanced, recall, F1-score and ROC-AUC were considered alongside accuracy.

## Final Model

The project uses XGBoost as the final prediction model.

The baseline XGBoost model achieved a test ROC-AUC of approximately:

0.722

The model achieved:

Accuracy: 0.787
Precision: 0.610
Recall: 0.159
F1 Score: 0.252
ROC-AUC: 0.722

A separate threshold analysis was also performed to study the trade-off between precision and recall.

## Explainable AI

SHAP (SHapley Additive exPlanations) is used to understand which software metrics contribute most strongly to individual model predictions.

Important model-attribution features included metrics such as:

Lines of Code (loc)
Blank Lines (lOBlank)
Difficulty (d)
Intelligence (i)
Total Operands (total_Opnd)
Code Lines (lOCode)
Unique Operators (uniq_Op)

SHAP explanations are used to show whether a feature's contribution moves the model prediction toward higher or lower defect probability.
                Python Source Code
                       |
                       ▼
                FastAPI Backend
                       │
                       ▼
               Metric Extraction
                   (Radon)
                       │
                       ▼
              XGBoost ML Model
                       │
              ┌────────┴────────┐
              ▼                 ▼
       Defect Probability    SHAP Analysis
              │                 │
              └────────┬────────┘
                       ▼
                 Risk Level
                       │
                       ▼
                 Web Frontend

## Technology Stack

### Programming Language
- Python
- JavaScript
- HTML
- CSS

### Machine Learning
- Scikit-learn
- XGBoost
- SHAP
- Imbalanced-learn

### Data Processing
- Pandas
- NumPy

### Software Analysis
- Radon
- Python AST

### Backend
- FastAPI
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript

### Development Tools
- Jupyter Notebook
- VS Code
- Git
- GitHub

## Prediction Workflow
The user uploads a Python source-code file.
    Python File
        ↓
    Metric Extraction
        ↓
    21 Software Metrics
        ↓
    XGBoost Prediction
        ↓
    Defect Probability
        ↓
    Risk Level
        ↓
    SHAP Risk Factors

The application displays:
- Prediction
- Defect probability
- Risk level
- Top risk factors
- Selected software metric

## Risk Levels

The application uses project-defined probability thresholds:
Probability < 30%       → Low Risk
30% – 69.99%            → Medium Risk
Probability ≥ 70%       → High Risk
These thresholds are application-specific and are not universal software-quality standards.

## Future Improvements
- Support additional programming languages
- Use larger software defect datasets
- Add repository-level analysis
- Add code churn and historical development metrics
- Improve model calibration
- Perform external validation on additional datasets
- Add automated CI/CD integration
- Deploy the application to a cloud platform

## Disclaimer

The source-code metric extraction and the JM1-trained model operate on different data-generation environments, so predictions should be treated as experimental rather than production-grade software-quality assessments.

## Author
Jasvitha Reddy Mandepudi
