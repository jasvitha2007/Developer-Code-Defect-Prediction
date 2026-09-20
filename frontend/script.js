const fileInput =
    document.getElementById("fileInput");

const fileName =
    document.getElementById("fileName");

const analyzeBtn =
    document.getElementById("analyzeBtn");

const status =
    document.getElementById("status");

const resultSection =
    document.getElementById("resultSection");

const prediction =
    document.getElementById("prediction");

const probability =
    document.getElementById("probability");

const risk =
    document.getElementById("risk");

const probabilityBar =
    document.getElementById("probabilityBar");

const predictionIcon =
    document.querySelector(".prediction-icon");

const analyzedFile =
    document.getElementById("analyzedFile");


const metricLoc =
    document.getElementById("metricLoc");

const metricComplexity =
    document.getElementById("metricComplexity");

const metricVolume =
    document.getElementById("metricVolume");

const metricBranches =
    document.getElementById("metricBranches");

const metricOperators =
    document.getElementById("metricOperators");

const metricOperands =
    document.getElementById("metricOperands");


const resetBtn =
    document.getElementById("resetBtn");


const shapFactors =
    document.getElementById("shapFactors");


// ==========================================
// Friendly names for SHAP features
// ==========================================

const featureNames = {

    "loc": "Lines of Code",

    "v(g)": "Cyclomatic Complexity",

    "ev(g)": "Essential Complexity",

    "iv(g)": "Design Complexity",

    "n": "Program Length",

    "v": "Halstead Volume",

    "l": "Program Level",

    "d": "Difficulty",

    "i": "Intelligence",

    "e": "Effort",

    "b": "Estimated Bugs",

    "t": "Development Time",

    "lOCode": "Code Lines",

    "lOComment": "Comment Lines",

    "lOBlank": "Blank Lines",

    "locCodeAndComment": "Code + Comment Lines",

    "uniq_Op": "Unique Operators",

    "uniq_Opnd": "Unique Operands",

    "total_Op": "Total Operators",

    "total_Opnd": "Total Operands",

    "branchCount": "Branch Count"
};


// ==========================================
// Update prediction/risk styling
// ==========================================

function updateResultStyle(riskLevel) {

    risk.classList.remove(
        "risk-low",
        "risk-medium",
        "risk-high"
    );

    predictionIcon.classList.remove(
        "prediction-low",
        "prediction-medium",
        "prediction-high"
    );


    if (riskLevel === "Low") {

        risk.classList.add("risk-low");

        predictionIcon.classList.add(
            "prediction-low"
        );

        predictionIcon.textContent = "✓";

    }

    else if (riskLevel === "Medium") {

        risk.classList.add("risk-medium");

        predictionIcon.classList.add(
            "prediction-medium"
        );

        predictionIcon.textContent = "⚠";

    }

    else {

        risk.classList.add("risk-high");

        predictionIcon.classList.add(
            "prediction-high"
        );

        predictionIcon.textContent = "!";
    }
}


// ==========================================
// Display SHAP factors
// ==========================================

function displayShapFactors(factors) {

    shapFactors.innerHTML = "";


    if (!factors || factors.length === 0) {

        shapFactors.innerHTML = `
            <div class="metric-item">
                <span>Explanation</span>
                <strong>Not available</strong>
            </div>
        `;

        return;
    }


    factors.forEach(function (factor) {

        const item =
            document.createElement("div");

        item.className =
            "metric-item";


        const featureName =
            featureNames[factor.feature]
            || factor.feature;


        const direction =
            factor.direction === "increases"
                ? "↑ Increases risk"
                : "↓ Decreases risk";


        item.innerHTML = `

            <span>
                ${featureName}
            </span>

            <strong class="${
                factor.direction === "increases"
                    ? "factor-increase"
                    : "factor-decrease"
            }">
                ${direction}
            </strong>

        `;


        shapFactors.appendChild(item);

    });
}


// ==========================================
// File selection
// ==========================================

fileInput.addEventListener(
    "change",
    function () {

        if (fileInput.files.length > 0) {

            const file =
                fileInput.files[0];

            fileName.textContent =
                file.name;

            status.textContent = "";

        }

        else {

            fileName.textContent =
                "No file selected";
        }
    }
);


// ==========================================
// Analyze code
// ==========================================

analyzeBtn.addEventListener(
    "click",
    async function () {

        if (fileInput.files.length === 0) {

            status.textContent =
                "Please select a Python file first.";

            return;
        }


        const file =
            fileInput.files[0];


        if (
            !file.name
                .toLowerCase()
                .endsWith(".py")
        ) {

            status.textContent =
                "Please upload a .py Python file.";

            return;
        }


        analyzedFile.textContent =
            "File: " + file.name;


        const formData =
            new FormData();


        formData.append(
            "file",
            file
        );


        status.textContent =
            "Analyzing source code...";


        analyzeBtn.disabled = true;


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/predict",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Prediction failed."
                );
            }


            // ==================================
            // Prediction
            // ==================================

            prediction.textContent =
                data.prediction;


            // ==================================
            // Probability
            // ==================================

            probability.textContent =
                Number(
                    data.defect_probability
                ).toFixed(2) + "%";


            probabilityBar.style.width =
                data.defect_probability + "%";


            // ==================================
            // Risk
            // ==================================

            risk.textContent =
                data.risk_level;


            updateResultStyle(
                data.risk_level
            );


            // ==================================
            // SHAP explanation
            // ==================================

            displayShapFactors(
                data.top_factors
            );


            // ==================================
            // Code analysis metrics
            // ==================================

            metricLoc.textContent =
                data.metrics.loc;


            metricComplexity.textContent =
                data.metrics["v(g)"];


            metricVolume.textContent =
                Number(
                    data.metrics.v
                ).toFixed(2);


            metricBranches.textContent =
                data.metrics.branchCount;


            metricOperators.textContent =
                data.metrics.total_Op;


            metricOperands.textContent =
                data.metrics.total_Opnd;


            // ==================================
            // Show results
            // ==================================

            resultSection.classList.remove(
                "hidden"
            );


            status.textContent =
                "Analysis completed successfully.";


            resultSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }


        catch (error) {

            status.textContent =
                "Error: " + error.message;

        }


        finally {

            analyzeBtn.disabled = false;
        }

    }
);


// ==========================================
// Reset
// ==========================================

resetBtn.addEventListener(
    "click",
    function () {

        fileInput.value = "";


        fileName.textContent =
            "No file selected";


        status.textContent = "";


        prediction.textContent =
            "-";


        probability.textContent =
            "-";


        risk.textContent =
            "-";


        probabilityBar.style.width =
            "0%";


        predictionIcon.textContent =
            "⚠";


        risk.classList.remove(
            "risk-low",
            "risk-medium",
            "risk-high"
        );


        predictionIcon.classList.remove(
            "prediction-low",
            "prediction-medium",
            "prediction-high"
        );


        analyzedFile.textContent =
            "File: -";


        shapFactors.innerHTML =
            "";


        metricLoc.textContent =
            "-";


        metricComplexity.textContent =
            "-";


        metricVolume.textContent =
            "-";


        metricBranches.textContent =
            "-";


        metricOperators.textContent =
            "-";


        metricOperands.textContent =
            "-";


        resultSection.classList.add(
            "hidden"
        );


        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);