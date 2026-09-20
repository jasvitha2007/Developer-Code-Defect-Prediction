from metric_extractor import extract_metrics
from prediction import predict_defect


code = """
def calculate_total(a, b):
    if a > b:
        return a + b
    else:
        return a - b
"""


# Step 1: Extract metrics from source code
metrics = extract_metrics(code)

print("Extracted metrics:")
print(metrics)
print()


# Step 2: Predict defect
result = predict_defect(metrics)

print("Prediction Result:")
print(result)