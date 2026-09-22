def generate_recommendations(
    metrics,
    code_analysis
):

    recommendations = []

    loc = float(
        metrics.get("loc", 0)
    )

    complexity = float(
        metrics.get("v(g)", 0)
    )

    branches = float(
        metrics.get("branchCount", 0)
    )

    difficulty = float(
        metrics.get("d", 0)
    )

    comments = float(
        metrics.get("lOComment", 0)
    )

    # --------------------------------------------------------
    # File size
    # --------------------------------------------------------

    if loc > 500:

        recommendations.append(
            {
                "severity": "High",
                "title": "Large source file",
                "message":
                    "Consider splitting this file into smaller "
                    "modules with focused responsibilities."
            }
        )

    elif loc > 250:

        recommendations.append(
            {
                "severity": "Medium",
                "title": "Large source file",
                "message":
                    "Consider separating related functionality "
                    "into smaller modules."
            }
        )

    # --------------------------------------------------------
    # Complexity
    # --------------------------------------------------------

    if complexity > 15:

        recommendations.append(
            {
                "severity": "High",
                "title": "High cyclomatic complexity",
                "message":
                    "There are many independent execution paths. "
                    "Break complex logic into smaller functions."
            }
        )

    elif complexity > 8:

        recommendations.append(
            {
                "severity": "Medium",
                "title": "Elevated cyclomatic complexity",
                "message":
                    "Simplify conditional logic and consider "
                    "extracting complex operations."
            }
        )

    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    if branches > 15:

        recommendations.append(
            {
                "severity": "High",
                "title": "High branch count",
                "message":
                    "Review nested decision logic and consider "
                    "extracting conditional behaviour."
            }
        )

    # --------------------------------------------------------
    # Halstead
    # --------------------------------------------------------

    if difficulty > 30:

        recommendations.append(
            {
                "severity": "High",
                "title": "High Halstead difficulty",
                "message":
                    "Simplify complicated expressions and "
                    "break large operations into smaller units."
            }
        )

    elif difficulty > 15:

        recommendations.append(
            {
                "severity": "Medium",
                "title": "Elevated Halstead difficulty",
                "message":
                    "Some expressions may be difficult to understand. "
                    "Consider simplifying them."
            }
        )

    # --------------------------------------------------------
    # Comments
    # --------------------------------------------------------

    if loc > 100 and comments < 5:

        recommendations.append(
            {
                "severity": "Medium",
                "title": "Limited documentation",
                "message":
                    "Consider adding comments around complex "
                    "logic and important design decisions."
            }
        )

    # --------------------------------------------------------
    # Complex function
    # --------------------------------------------------------

    max_complexity = code_analysis.get(
        "max_complexity",
        0
    )

    if max_complexity > 10:

        name = code_analysis.get(
            "most_complex_function",
            "unknown"
        )

        recommendations.append(
            {
                "severity": "High",
                "title": "Complex function detected",
                "message":
                    f"`{name}()` has high estimated complexity. "
                    "Consider splitting it into smaller functions."
            }
        )

    # --------------------------------------------------------
    # Deep nesting
    # --------------------------------------------------------

    if code_analysis.get(
        "max_ast_depth",
        0
    ) > 15:

        recommendations.append(
            {
                "severity": "Medium",
                "title": "Deep nesting detected",
                "message":
                    "Consider using early returns and helper "
                    "functions to reduce nesting."
            }
        )

    # --------------------------------------------------------
    # TODO / FIXME
    # --------------------------------------------------------

    todo_count = code_analysis.get(
        "todo_count",
        0
    )

    if todo_count > 0:

        recommendations.append(
            {
                "severity": "Low",
                "title": "Pending TODO/FIXME items",
                "message":
                    f"{todo_count} TODO/FIXME marker(s) were detected. "
                    "Review them before considering the code complete."
            }
        )

    # --------------------------------------------------------
    # Security
    # --------------------------------------------------------

    security_signals = code_analysis.get(
        "security_signals",
        []
    )

    for signal in security_signals:

        recommendations.append(
            {
                "severity": "High",
                "title":
                    f"Security signal: {signal['name']}",
                "message":
                    f"Potentially sensitive operation detected "
                    f"around line {signal['line']}. "
                    "Review this operation carefully."
            }
        )

    # --------------------------------------------------------
    # Default
    # --------------------------------------------------------

    if not recommendations:

        recommendations.append(
            {
                "severity": "Info",
                "title": "No major issues detected",
                "message":
                    "The configured static analysis rules did not "
                    "identify major concerns."
            }
        )

    return recommendations