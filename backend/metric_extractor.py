import ast
import math

from radon.raw import analyze
from radon.complexity import cc_visit
from radon.metrics import h_visit


def extract_metrics(code):

    raw = analyze(code)

    complexity_results = cc_visit(code)

    if complexity_results:
        cyclomatic_complexity = sum(
            item.complexity
            for item in complexity_results
        )
    else:
        cyclomatic_complexity = 1

    halstead = h_visit(code)

    total_h = halstead.total

    uniq_op = total_h.h1
    uniq_opnd = total_h.h2

    total_op = total_h.N1
    total_opnd = total_h.N2

    n = total_h.length
    volume = total_h.volume
    difficulty = total_h.difficulty
    effort = total_h.effort
    time = total_h.time
    bugs = total_h.bugs

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

    branch_count = cyclomatic_complexity

    loc = raw.loc
    loc_code = raw.lloc
    loc_comment = raw.sloc
    loc_blank = raw.blank
    loc_code_comment = raw.single_comments

    return {
        "loc": loc,
        "v(g)": cyclomatic_complexity,
        "ev(g)": cyclomatic_complexity,
        "iv(g)": cyclomatic_complexity,
        "n": n,
        "v": volume,
        "l": level,
        "d": difficulty,
        "i": intelligence,
        "e": effort,
        "b": bugs,
        "t": time,
        "lOCode": loc_code,
        "lOComment": loc_comment,
        "lOBlank": loc_blank,
        "locCodeAndComment": loc_code_comment,
        "uniq_Op": uniq_op,
        "uniq_Opnd": uniq_opnd,
        "total_Op": total_op,
        "total_Opnd": total_opnd,
        "branchCount": branch_count
    }