import ast


def calculate_function_complexity(function):

    complexity = 1

    for node in ast.walk(function):

        if isinstance(
            node,
            (
                ast.If,
                ast.For,
                ast.AsyncFor,
                ast.While,
                ast.Try,
                ast.With,
                ast.AsyncWith,
                ast.IfExp
            )
        ):
            complexity += 1

        elif isinstance(node, ast.BoolOp):

            complexity += max(
                len(node.values) - 1,
                0
            )

    return complexity


def analyze_code(code):

    tree = ast.parse(code)

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef
            )
        )
    ]

    classes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]

    loops = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.For,
                ast.AsyncFor,
                ast.While
            )
        )
    ]

    conditions = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.If,
                ast.IfExp
            )
        )
    ]

    imports = [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.Import,
                ast.ImportFrom
            )
        )
    ]

    function_data = []

    for function in functions:

        complexity = calculate_function_complexity(
            function
        )

        end_line = getattr(
            function,
            "end_lineno",
            function.lineno
        )

        lines = (
            end_line
            - function.lineno
            + 1
        )

        parameters = len(
            function.args.args
        )

        function_data.append(
            {
                "name": function.name,
                "line": function.lineno,
                "end_line": end_line,
                "lines": lines,
                "complexity": complexity,
                "parameters": parameters
            }
        )

    if function_data:

        complexity_values = [
            item["complexity"]
            for item in function_data
        ]

        max_complexity = max(
            complexity_values
        )

        average_complexity = (
            sum(complexity_values)
            / len(complexity_values)
        )

        most_complex = max(
            function_data,
            key=lambda item: item["complexity"]
        )

    else:

        max_complexity = 1
        average_complexity = 1

        most_complex = {
            "name": "None",
            "line": 0,
            "end_line": 0,
            "lines": 0,
            "complexity": 1,
            "parameters": 0
        }

    # --------------------------------------------------------
    # AST depth
    # --------------------------------------------------------

    max_depth = 0

    def calculate_depth(node, depth=0):

        nonlocal max_depth

        max_depth = max(
            max_depth,
            depth
        )

        for child in ast.iter_child_nodes(node):

            calculate_depth(
                child,
                depth + 1
            )

    calculate_depth(tree)

    # --------------------------------------------------------
    # TODO / FIXME
    # --------------------------------------------------------

    todo_count = 0

    for line in code.splitlines():

        upper_line = line.upper()

        if "TODO" in upper_line:
            todo_count += 1

        if "FIXME" in upper_line:
            todo_count += 1

    # --------------------------------------------------------
    # Security signals
    # --------------------------------------------------------

    security_signals = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                function_name = node.func.id

                if function_name in {
                    "eval",
                    "exec",
                    "compile"
                }:

                    security_signals.append(
                        {
                            "type": "Potentially unsafe function",
                            "name": function_name,
                            "line": node.lineno
                        }
                    )

            elif isinstance(
                node.func,
                ast.Attribute
            ):

                if node.func.attr == "system":

                    security_signals.append(
                        {
                            "type": "Shell execution signal",
                            "name": "os.system",
                            "line": node.lineno
                        }
                    )

    # --------------------------------------------------------
    # Nested function count
    # --------------------------------------------------------

    nested_functions = 0

    for function in functions:

        for node in ast.walk(function):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            ) and node is not function:

                nested_functions += 1

    return {

        "functions": len(functions),

        "classes": len(classes),

        "loops": len(loops),

        "conditions": len(conditions),

        "imports": len(imports),

        "max_complexity": max_complexity,

        "average_complexity": round(
            average_complexity,
            2
        ),

        "most_complex_function":
            most_complex["name"],

        "most_complexity":
            most_complex["complexity"],

        "max_ast_depth":
            max_depth,

        "todo_count":
            todo_count,

        "nested_functions":
            nested_functions,

        "functions_detail":
            function_data,

        "security_signals":
            security_signals
    }