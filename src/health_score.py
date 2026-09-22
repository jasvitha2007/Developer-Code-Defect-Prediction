def calculate_health_score(
    metrics,
    code_analysis,
    defect_probability
):

    score = 100.0

    loc = float(
        metrics.get("loc", 0)
    )

    complexity = float(
        metrics.get("v(g)", 0)
    )

    difficulty = float(
        metrics.get("d", 0)
    )

    branches = float(
        metrics.get("branchCount", 0)
    )

    comments = float(
        metrics.get("lOComment", 0)
    )

    # File size penalty
    if loc > 500:
        score -= 20
    elif loc > 250:
        score -= 10
    elif loc > 150:
        score -= 5

    # Complexity penalty
    if complexity > 15:
        score -= 25
    elif complexity > 10:
        score -= 15
    elif complexity > 8:
        score -= 8

    # Difficulty penalty
    if difficulty > 30:
        score -= 15
    elif difficulty > 15:
        score -= 8

    # Branch penalty
    if branches > 15:
        score -= 15
    elif branches > 8:
        score -= 8

    # Documentation
    if loc > 100 and comments < 5:
        score -= 5

    # ML risk contribution
    if defect_probability >= 70:
        score -= 15
    elif defect_probability >= 30:
        score -= 8
    elif defect_probability >= 20:
        score -= 3

    score = max(
        0,
        min(
            100,
            round(score)
        )
    )

    if score >= 80:
        label = "Excellent"

    elif score >= 65:
        label = "Good"

    elif score >= 50:
        label = "Needs Attention"

    else:
        label = "Poor"

    return {
        "score": score,
        "label": label
    }