# 🤖 AI Software Defect Predictor & Risk Analyzer

An explainable machine-learning system that analyzes Python source code, extracts software engineering metrics, predicts defect risk using XGBoost, and explains individual predictions using SHAP.

The platform combines machine learning, static code analysis, software metrics, explainable AI, code-quality scoring, hotspot detection, security signals, and an interactive Streamlit dashboard.

---

## 🚀 Project Overview

Software defects are often associated with measurable characteristics of source code such as:

- Lines of Code
- Cyclomatic Complexity
- Branch Count
- Halstead Volume
- Halstead Difficulty
- Operators and Operands
- Code structure and nesting

This project automatically extracts these characteristics from Python source code and uses a trained XGBoost classification model to estimate defect risk.

Instead of providing only a prediction, the system also explains why the model produced that prediction and provides actionable code-quality recommendations.

---

## ✨ Key Features

### 🤖 Machine Learning

- XGBoost-based software defect prediction
- Defect probability estimation
- Custom prediction threshold
- Risk classification
- Accuracy, precision, recall, F1-score and ROC-AUC evaluation
- Confusion matrix analysis
- Threshold analysis

### 🔎 Explainable AI

- SHAP-based model explanations
- Top contributing software metrics
- Positive and negative feature contributions
- Per-prediction explanations
- Human-readable model interpretation

### 🧠 Static Code Analysis

- Python AST analysis
- Function detection
- Class detection
- Loop detection
- Conditional detection
- Import analysis
- AST depth analysis
- Function-level complexity analysis
- Code hotspot detection

### 🏆 Code Health Score

The system calculates an independent Code Health Score from 0–100 using software-quality indicators including:

- Source-code size
- Cyclomatic complexity
- Branch count
- Halstead difficulty
- Documentation
- ML-estimated defect risk

### 💡 Automated Recommendations

The system detects potential code-quality concerns such as:

- Large source files
- High complexity
- Excessive branching
- Difficult expressions
- Deep nesting
- Limited documentation
- Complex functions
- TODO/FIXME markers

### 🛡️ Security Signals

The analyzer checks for potentially risky operations such as:

- `eval()`
- `exec()`
- `compile()`
- Shell execution patterns

These are reported as security signals requiring review and are not automatically classified as vulnerabilities.

### 🔥 Function-Level Hotspots

The system identifies functions with elevated complexity and reports:

- Function name
- Starting line
- Ending line
- Number of lines
- Complexity
- Number of parameters

### 🎮 Demo Mode

Built-in examples are provided for:

- Simple code
- Moderate-complexity code
- Complex code

### 📊 Interactive Dashboard

The Streamlit application provides:

- Prediction summary
- Defect probability
- Risk level
- Code Health Score
- SHAP explanation
- Code hotspots
- Software metrics
- Refactoring recommendations
- Security signals
- Source-code viewer
- Analysis history

### 📥 Report Export

Analysis results can be exported as:

- JSON
- HTML

---

## 🏗️ System Architecture

```text
                    Python Source Code
                           │
                           ▼
                  ┌──────────────────┐
                  │   Python Parser  │
                  │      AST         │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      Static Analysis              Metric Extraction
             │                           │
             │                           ▼
             │                    Software Metrics
             │                           │
             │                           ▼
             │                    XGBoost Model
             │                           │
             │                           ▼
             │                    Defect Probability
             │                           │
             │                           ▼
             │                         SHAP
             │                           │
             └──────────────┬────────────┘
                            ▼
                  Explainable Dashboard
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       Code Health      Risk Analysis   Recommendations
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     JSON / HTML Report
🔬 Machine Learning Pipeline
Dataset
   ↓
Data Cleaning
   ↓
Duplicate Detection
   ↓
Missing Value Handling
   ↓
Feature Analysis
   ↓
Train / Test Split
   ↓
XGBoost Training
   ↓
Model Evaluation
   ↓
Threshold Analysis
   ↓
Final Model
   ↓
SHAP Explainability
   ↓
Deployment
📊 Dataset

The project uses the Software Defect Prediction dataset from Kaggle:

semustafacevik/software-defect-prediction

The dataset contains software engineering metrics and a binary defect label.

Main Features
Feature	Description
loc	Lines of code
v(g)	Cyclomatic complexity
ev(g)	Essential complexity
iv(g)	Design complexity
n	Program length
v	Halstead volume
l	Halstead level
d	Halstead difficulty
i	Halstead intelligence
e	Halstead effort
b	Estimated bugs
t	Programming time
lOCode	Lines of code
lOComment	Comment lines
lOBlank	Blank lines
uniq_Op	Unique operators
uniq_Opnd	Unique operands
total_Op	Total operators
total_Opnd	Total operands
branchCount	Number of branches

## 🧹 Data Preparation

The dataset was processed using:

Duplicate record detection
Duplicate removal
Numeric conversion
Missing-value handling
Target-label inspection
Class-distribution analysis
Feature correlation analysis
Train/test splitting

After preprocessing, the modeling dataset contained approximately 8.9K records.

The positive defect class represented approximately 22.5% of the cleaned dataset.

## 🤖 Machine Learning Model

The primary model is:

XGBoost Classifier

XGBoost was selected because it is well suited for structured tabular data and can capture nonlinear relationships between software metrics and defect labels.

## Evaluation Metrics

The model was evaluated using:

Accuracy
Precision
Recall
F1-score
ROC-AUC
Confusion matrix
Threshold analysis

The final baseline XGBoost model achieved approximately:

ROC-AUC: 0.72

on the held-out test set.

## 🎯 Prediction Threshold

The application uses a defect-prediction threshold of:

20%

Probability >= 20%
        ↓
Defect Predicted

Probability < 20%
        ↓
No Defect Predicted

The prediction threshold is separate from the risk-classification thresholds.

⚠️ Risk Classification
Defect Probability	Risk Level
< 30%	🟢 Low
30% – <70%	🟠 Medium
≥ 70%	🔴 High

These are project-defined risk bands and should not be interpreted as calibrated real-world failure probabilities.

🔎 Explainable AI with SHAP

The project uses SHAP to explain individual predictions.

Instead of displaying only a probability, the system identifies which software metrics contributed most strongly to that prediction.

Example:

↑ Lines of Code
↑ Halstead Difficulty
↓ Comment Lines
↑ Branch Count
↑ Total Operands

Each factor includes:

Feature name
Feature value
SHAP contribution
Direction of contribution

This provides transparency into the model's decision-making process.

🏆 Code Health Score

The application calculates an independent Code Health Score from 0–100.

The score considers:

Source-code size
Cyclomatic complexity
Branch count
Halstead difficulty
Documentation
ML-estimated defect risk
Health Categories
Score	Classification
80–100	Excellent
65–79	Good
50–64	Needs Attention
0–49	Poor

The Code Health Score is a project-specific quality indicator and is separate from the ML defect probability.

🔥 Function-Level Hotspots

The application analyzes individual functions and identifies potential hotspots.

For every detected function, the system can report:

Function name
Starting line
Ending line
Number of lines
Estimated complexity
Number of parameters

Example:

🔴 process_data()
   Complexity: 12
   Lines: 48

🟠 calculate_score()
   Complexity: 8
   Lines: 29

This helps developers identify areas that may require additional testing or refactoring.

🛡️ Security Signals

The static analyzer checks for selected potentially risky operations.

Examples:

eval(...)
exec(...)
compile(...)
os.system(...)

These detections are reported as security signals.

A security signal does not automatically mean that a vulnerability exists. The surrounding code and intended usage should be reviewed.

💡 Automated Recommendations

The system generates recommendations based on detected code characteristics.

Large Source File

Consider splitting the file into smaller modules with focused responsibilities.

High Complexity

Break complex logic into smaller functions and simplify conditional paths.

Deep Nesting

Consider using early returns and helper functions to reduce nesting.

Limited Documentation

Consider documenting complex logic and important design decisions.

Complex Function

Split highly complex functions into smaller units that are easier to test and maintain.

👩‍💻 Author
Jasvitha Reddy Mandepudi

CSE – Artificial Intelligence & Machine Learning

Areas of Interest
Machine Learning
Artificial Intelligence
Data Science
Software Engineering
Explainable AI

⭐ Project Highlight

End-to-end Explainable AI system for software defect prediction combining XGBoost, SHAP, software engineering metrics, Python AST analysis, code-health scoring, hotspot detection, security signals, and automated recommendations.

📌 Keywords

Machine Learning XGBoost SHAP Explainable AI Software Defect Prediction Static Code Analysis Python AST Software Metrics Code Quality Risk Analysis Streamlit Python Software Engineering
