import os
import json
import importlib.util
from datetime import datetime

import streamlit as st


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SRC_DIR = os.path.join(
    BASE_DIR,
    "src"
)

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AI Software Defect Predictor",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# MODULE LOADER
# ============================================================

def load_module(
    name,
    path
):

    spec = importlib.util.spec_from_file_location(
        name,
        path
    )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


prediction = load_module(
    "prediction",
    os.path.join(
        SRC_DIR,
        "prediction.py"
    )
)

extractor = load_module(
    "metric_extractor",
    os.path.join(
        BACKEND_DIR,
        "metric_extractor.py"
    )
)

analyzer = load_module(
    "code_analyzer",
    os.path.join(
        BACKEND_DIR,
        "code_analyzer.py"
    )
)

recommendation_engine = load_module(
    "recommendations",
    os.path.join(
        SRC_DIR,
        "recommendations.py"
    )
)

health_engine = load_module(
    "health_score",
    os.path.join(
        SRC_DIR,
        "health_score.py"
    )
)


# ============================================================
# FUNCTIONS
# ============================================================

predict_defect = (
    prediction.predict_defect
)

extract_metrics = (
    extractor.extract_metrics
)

analyze_code = (
    analyzer.analyze_code
)

generate_recommendations = (
    recommendation_engine.generate_recommendations
)

calculate_health_score = (
    health_engine.calculate_health_score
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {

    "result": None,

    "metrics": None,

    "analysis": None,

    "recommendations": [],

    "health": None,

    "filename": None,

    "code": None,

    "history": []
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Defect AI")

    st.caption(
        "Explainable Software Quality Platform"
    )

    st.divider()

    st.subheader("🧠 Pipeline")

    st.write(
        "📂 Source Code"
    )

    st.write(
        "↓"
    )

    st.write(
        "⚙️ Metric Extraction"
    )

    st.write(
        "↓"
    )

    st.write(
        "🤖 XGBoost"
    )

    st.write(
        "↓"
    )

    st.write(
        "🔎 SHAP Explanation"
    )

    st.write(
        "↓"
    )

    st.write(
        "📊 Quality Dashboard"
    )

    st.divider()

    st.subheader("🎯 Risk Levels")

    st.success(
        "🟢 Low — < 30%"
    )

    st.warning(
        "🟠 Medium — 30–69%"
    )

    st.error(
        "🔴 High — ≥ 70%"
    )

    st.divider()

    st.subheader("⚙️ Stack")

    st.write(
        "Python"
    )

    st.write(
        "XGBoost"
    )

    st.write(
        "SHAP"
    )

    st.write(
        "Radon"
    )

    st.write(
        "Python AST"
    )

    st.write(
        "Streamlit"
    )

    st.divider()

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        for key in defaults:

            st.session_state[key] = (
                defaults[key]
            )

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 AI Software Defect Predictor"
)

st.write(
    "Analyze Python source code, estimate defect risk, "
    "identify code-quality hotspots, and understand "
    "why the machine-learning model made its prediction."
)

st.divider()


# ============================================================
# DEMO MODE
# ============================================================

st.header(
    "📂 Analyze Source Code"
)

demo_col, upload_col = st.columns(
    [1, 2]
)

with demo_col:

    demo_files = {

        "Simple example":
            "tests/simple.py",

        "Moderate example":
            "tests/moderate.py",

        "Complex example":
            "tests/complex_code.py"
    }

    demo_choice = st.selectbox(
        "🎮 Demo Mode",
        [
            "None"
        ] + list(
            demo_files.keys()
        )
    )

with upload_col:

    uploaded_file = st.file_uploader(
        "Upload Python (.py)",
        type=["py"]
    )


# ============================================================
# GET CODE
# ============================================================

code = None
filename = None

if demo_choice != "None":

    demo_path = os.path.join(
        BASE_DIR,
        demo_files[demo_choice]
    )

    if os.path.exists(
        demo_path
    ):

        with open(
            demo_path,
            "r",
            encoding="utf-8"
        ) as file:

            code = file.read()

        filename = os.path.basename(
            demo_path
        )

if uploaded_file is not None:

    code = uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )

    filename = uploaded_file.name


# ============================================================
# ANALYZE
# ============================================================

if code is not None:

    st.info(
        f"Selected file: **{filename}**"
    )

    if st.button(
        "🚀 Analyze Code",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Running complete code analysis..."
            ):

                metrics = extract_metrics(
                    code
                )

                result = predict_defect(
                    metrics
                )

                analysis = analyze_code(
                    code
                )

                recommendations = (
                    generate_recommendations(
                        metrics,
                        analysis
                    )
                )

                health = calculate_health_score(
                    metrics,
                    analysis,
                    result[
                        "defect_probability"
                    ]
                )

            st.session_state.result = result

            st.session_state.metrics = metrics

            st.session_state.analysis = analysis

            st.session_state.recommendations = (
                recommendations
            )

            st.session_state.health = health

            st.session_state.filename = filename

            st.session_state.code = code

            # ------------------------------------------------
            # History
            # ------------------------------------------------

            st.session_state.history.insert(
                0,
                {
                    "file": filename,
                    "probability":
                        result[
                            "defect_probability"
                        ],
                    "risk":
                        result[
                            "risk_level"
                        ],
                    "health":
                        health["score"]
                }
            )

            st.session_state.history = (
                st.session_state.history[:10]
            )

            st.success(
                "Analysis completed."
            )

        except SyntaxError:

            st.error(
                "❌ Invalid Python syntax."
            )

        except Exception as error:

            st.error(
                "❌ Analysis failed."
            )

            with st.expander(
                "Technical details"
            ):

                st.exception(
                    error
                )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.result

metrics = st.session_state.metrics

analysis = st.session_state.analysis

recommendations = (
    st.session_state.recommendations
)

health = st.session_state.health


if result is not None:

    st.divider()

    # ========================================================
    # HEALTH + PREDICTION
    # ========================================================

    st.header(
        "🎯 Code Health Dashboard"
    )

    health_col, prediction_col, probability_col, risk_col = (
        st.columns(4)
    )

    with health_col:

        st.metric(
            "🏆 Code Health",
            f'{health["score"]}/100'
        )

    with prediction_col:

        st.metric(
            "Prediction",
            result["prediction"]
        )

    with probability_col:

        st.metric(
            "Defect Probability",
            f'{result["defect_probability"]:.2f}%'
        )

    with risk_col:

        st.metric(
            "Risk Level",
            result["risk_level"]
        )


    st.progress(
        health["score"] / 100
    )

    st.caption(
        f"Overall code-health classification: "
        f"**{health['label']}**"
    )


    # ========================================================
    # RISK
    # ========================================================

    st.subheader(
        "📊 Defect Risk"
    )

    probability = (
        result["defect_probability"]
    )

    st.progress(
        min(
            probability / 100,
            1
        )
    )

    if result["risk_level"] == "Low":

        st.success(
            f"🟢 Estimated defect probability: "
            f"{probability:.2f}%"
        )

    elif result["risk_level"] == "Medium":

        st.warning(
            f"🟠 Estimated defect probability: "
            f"{probability:.2f}%"
        )

    else:

        st.error(
            f"🔴 Estimated defect probability: "
            f"{probability:.2f}%"
        )


    # ========================================================
    # SHAP + CODE HOTSPOTS
    # ========================================================

    left, right = st.columns(2)


    with left:

        st.subheader(
            "🔎 Why this prediction?"
        )

        factors = result.get(
            "top_factors",
            []
        )

        names = {

            "loc":
                "Lines of Code",

            "v(g)":
                "Cyclomatic Complexity",

            "ev(g)":
                "Essential Complexity",

            "iv(g)":
                "Design Complexity",

            "n":
                "Program Length",

            "v":
                "Halstead Volume",

            "l":
                "Halstead Level",

            "d":
                "Halstead Difficulty",

            "i":
                "Halstead Intelligence",

            "e":
                "Halstead Effort",

            "b":
                "Estimated Bugs",

            "t":
                "Programming Time",

            "lOCode":
                "Lines of Code",

            "lOComment":
                "Comment Lines",

            "lOBlank":
                "Blank Lines",

            "locCodeAndComment":
                "Code + Comment Lines",

            "uniq_Op":
                "Unique Operators",

            "uniq_Opnd":
                "Unique Operands",

            "total_Op":
                "Total Operators",

            "total_Opnd":
                "Total Operands",

            "branchCount":
                "Branch Count"
        }

        for factor in factors:

            name = names.get(
                factor["feature"],
                factor["feature"]
            )

            value = factor["value"]

            shap_value = factor[
                "shap_value"
            ]

            if shap_value > 0:

                st.error(
                    f"**↑ {name}**  \n"
                    f"Value: `{value}`  \n"
                    f"Model contribution: "
                    f"`+{abs(shap_value):.4f}`"
                )

            else:

                st.success(
                    f"**↓ {name}**  \n"
                    f"Value: `{value}`  \n"
                    f"Model contribution: "
                    f"`-{abs(shap_value):.4f}`"
                )


    with right:

        st.subheader(
            "🔥 Code Hotspots"
        )

        functions = analysis.get(
            "functions_detail",
            []
        )

        if functions:

            hotspots = sorted(
                functions,
                key=lambda x: (
                    x["complexity"],
                    x["lines"]
                ),
                reverse=True
            )

            for item in hotspots[:5]:

                if item["complexity"] >= 10:

                    st.error(
                        f"🔴 **{item['name']}()** — "
                        f"Complexity {item['complexity']} | "
                        f"{item['lines']} lines"
                    )

                elif item["complexity"] >= 6:

                    st.warning(
                        f"🟠 **{item['name']}()** — "
                        f"Complexity {item['complexity']} | "
                        f"{item['lines']} lines"
                    )

                else:

                    st.info(
                        f"🟢 **{item['name']}()** — "
                        f"Complexity {item['complexity']} | "
                        f"{item['lines']} lines"
                    )

        else:

            st.info(
                "No functions detected."
            )


    # ========================================================
    # CODE QUALITY
    # ========================================================

    st.divider()

    st.header(
        "🧠 Code Quality"
    )

    q1, q2, q3, q4, q5, q6 = st.columns(6)

    with q1:
        st.metric(
            "Functions",
            analysis["functions"]
        )

    with q2:
        st.metric(
            "Classes",
            analysis["classes"]
        )

    with q3:
        st.metric(
            "Loops",
            analysis["loops"]
        )

    with q4:
        st.metric(
            "Conditions",
            analysis["conditions"]
        )

    with q5:
        st.metric(
            "Max Complexity",
            analysis["max_complexity"]
        )

    with q6:
        st.metric(
            "Imports",
            analysis["imports"]
        )


    # ========================================================
    # KEY METRICS
    # ========================================================

    st.subheader(
        "📈 Key Software Metrics"
    )

    key_metrics = [

        ("LOC", "loc"),

        ("Cyclomatic Complexity", "v(g)"),

        ("Branches", "branchCount"),

        ("Operators", "uniq_Op"),

        ("Operands", "uniq_Opnd"),

        ("Halstead Volume", "v"),

        ("Difficulty", "d"),

        ("Comments", "lOComment")
    ]

    metric_cols = st.columns(4)

    for index, (
        label,
        key
    ) in enumerate(
        key_metrics
    ):

        with metric_cols[
            index % 4
        ]:

            st.metric(
                label,
                f'{float(metrics.get(key, 0)):.2f}'
            )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header(
        "💡 Refactoring & Testing Suggestions"
    )

    for item in recommendations:

        severity = item[
            "severity"
        ]

        message = (
            f"**{item['title']}**  \n"
            f"{item['message']}"
        )

        if severity == "High":

            st.error(message)

        elif severity == "Medium":

            st.warning(message)

        else:

            st.info(message)


    # ========================================================
    # SECURITY
    # ========================================================

    security_signals = analysis.get(
        "security_signals",
        []
    )

    st.subheader(
        "🛡️ Security Signals"
    )

    if security_signals:

        for signal in security_signals:

            st.warning(
                f"Potential security signal: "
                f"`{signal['name']}` "
                f"around line {signal['line']}"
            )

    else:

        st.success(
            "No configured security signals detected."
        )


    # ========================================================
    # SOURCE
    # ========================================================

    st.divider()

    st.header(
        "💻 Source Code"
    )

    with st.expander(
        f"View {st.session_state.filename}"
    ):

        st.code(
            st.session_state.code,
            language="python"
        )


    # ========================================================
    # ALL METRICS
    # ========================================================

    with st.expander(
        "📋 View all extracted metrics"
    ):

        st.json(
            metrics
        )


    # ========================================================
    # HISTORY
    # ========================================================

    if st.session_state.history:

        st.divider()

        st.header(
            "🕘 Analysis History"
        )

        for item in st.session_state.history:

            st.write(
                f"**{item['file']}** — "
                f"Risk: {item['risk']} | "
                f"Probability: {item['probability']:.2f}% | "
                f"Health: {item['health']}/100"
            )


    # ========================================================
    # HTML REPORT
    # ========================================================

    st.divider()

    st.header(
        "📥 Export Report"
    )

    report = {

        "file":
            st.session_state.filename,

        "analysis_time":
            datetime.now().isoformat(),

        "prediction":
            result,

        "health":
            health,

        "metrics":
            metrics,

        "code_analysis":
            analysis,

        "recommendations":
            recommendations
    }

    json_report = json.dumps(
        report,
        indent=4,
        default=str
    )

    html_report = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Software Defect Analysis</title>
</head>

<body>

<h1>AI Software Defect Analysis</h1>

<h2>File</h2>
<p>{st.session_state.filename}</p>

<h2>Code Health</h2>
<h1>{health["score"]}/100</h1>
<p>{health["label"]}</p>

<h2>Prediction</h2>
<p>{result["prediction"]}</p>

<h2>Defect Probability</h2>
<p>{result["defect_probability"]:.2f}%</p>

<h2>Risk Level</h2>
<p>{result["risk_level"]}</p>

<h2>Top Risk Factors</h2>
<ul>
"""

    for factor in result.get(
        "top_factors",
        []
    ):

        html_report += (
            f"<li>{factor['feature']} — "
            f"{factor['value']} — "
            f"SHAP {factor['shap_value']}</li>"
        )

    html_report += """
</ul>

<h2>Recommendations</h2>
<ul>
"""

    for recommendation in recommendations:

        html_report += (
            f"<li><b>{recommendation['title']}</b>: "
            f"{recommendation['message']}</li>"
        )

    html_report += """
</ul>

</body>
</html>
"""

    report_col1, report_col2 = st.columns(2)

    with report_col1:

        st.download_button(
            "📄 Download JSON",
            json_report,
            "defect_analysis.json",
            "application/json",
            use_container_width=True
        )

    with report_col2:

        st.download_button(
            "🌐 Download HTML Report",
            html_report,
            "defect_analysis.html",
            "text/html",
            use_container_width=True
        )


    # ========================================================
    # INTERPRETATION
    # ========================================================

    st.divider()

    st.header(
        "ℹ️ Interpretation"
    )

    st.write(
        "The model estimates defect risk from software "
        "engineering metrics extracted automatically "
        "from the uploaded Python source code."
    )

    st.write(
        "SHAP values describe how individual metrics "
        "influenced this particular model prediction."
    )

    st.write(
        "Static-analysis signals are indicators for review, "
        "not proof of a security vulnerability or defect."
    )


else:

    st.info(
        "👆 Upload a Python file or choose Demo Mode "
        "to begin."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Software Defect Predictor • "
    "XGBoost + SHAP + Radon + Python AST"
)