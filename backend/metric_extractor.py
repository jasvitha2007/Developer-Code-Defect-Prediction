import ast
import math
from radon.raw import analyze
from radon.complexity import cc_visit
from radon.metrics import h_visit


def extract_metrics(code: str):
    """
    Extract software metrics from Python source code.

    Returns the 21 features expected by the trained XGBoost model.
    """

    # -----------------------------------
    # 1. Basic source-code metrics
    # -----------------------------------

    raw_metrics = analyze(code)

    loc = raw_metrics.loc
    loc_code = raw_metrics.sloc
    loc_comment = raw_metrics.comments
    loc_blank = raw_metrics.blank

    # Lines containing both code and comments
    loc_code_and_comment = max(
        0,
        loc_code + loc_comment - loc
    )

    # -----------------------------------
    # 2. Cyclomatic complexity
    # -----------------------------------

    complexity_blocks = cc_visit(code)

    if complexity_blocks:
        total_complexity = sum(
            block.complexity for block in complexity_blocks
        )

        max_complexity = max(
            block.complexity for block in complexity_blocks
        )
    else:
        total_complexity = 1
        max_complexity = 1

    # Approximate JM1 complexity-related metrics
    v_g = total_complexity
    ev_g = max_complexity
    iv_g = max_complexity

    branch_count = max(0, total_complexity - 1)

    # -----------------------------------
    # 3. Halstead metrics
    # -----------------------------------

    try:
        halstead = h_visit(code)

        total_h = halstead.total

        # Basic Halstead metrics
        uniq_op = total_h.h1
        uniq_opnd = total_h.h2
        total_op = total_h.N1
        total_opnd = total_h.N2

        # Total number of operators and operands
        n = total_h.length

        # Halstead metrics
        volume = total_h.volume
        difficulty = total_h.difficulty
        effort = total_h.effort

        # Radon already provides time and bugs
        time = total_h.time
        bugs = total_h.bugs

        # Derived intelligence and level
        intelligence = (
            volume / difficulty
            if difficulty > 0
            else 0
        )

        level = (
            1 / difficulty
            if difficulty > 0
            else 0
        )

    except Exception as error:
        print("Halstead metric extraction error:", error)

        uniq_op = 0
        uniq_opnd = 0
        total_op = 0
        total_opnd = 0
        n = 0
        volume = 0
        difficulty = 0
        effort = 0
        intelligence = 0
        level = 0
        bugs = 0
        time = 0

    # -----------------------------------
    # 4. Derived metrics
    # -----------------------------------

    

    # -----------------------------------
    # 5. Return exact model features
    # -----------------------------------

    metrics = {
        "loc": float(loc),
        "v(g)": float(v_g),
        "ev(g)": float(ev_g),
        "iv(g)": float(iv_g),
        "n": float(n),
        "v": float(volume),
        "l": float(level),
        "d": float(difficulty),
        "i": float(intelligence),
        "e": float(effort),
        "b": float(bugs),
        "t": float(time),
        "lOCode": float(loc_code),
        "lOComment": float(loc_comment),
        "lOBlank": float(loc_blank),
        "locCodeAndComment": float(loc_code_and_comment),
        "uniq_Op": float(uniq_op),
        "uniq_Opnd": float(uniq_opnd),
        "total_Op": float(total_op),
        "total_Opnd": float(total_opnd),
        "branchCount": float(branch_count),
    }

    return metrics