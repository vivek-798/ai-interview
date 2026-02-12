import json
import traceback


def load_coding_questions():
    with open("questions/coding_questions.json", "r") as f:
        return json.load(f)


def conduct_coding_round():
    questions = load_coding_questions()

    print("\n=== Coding Round ===")

    q = questions[0]  # For now, pick first question
    print("\nProblem:")
    print(q["question"])
    print("\nWrite your function below. Type 'END' on new line to finish.\n")

    user_code_lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        user_code_lines.append(line)

    user_code = "\n".join(user_code_lines)

    return evaluate_code(user_code, q)

# rounds/coding.py

def evaluate_code(user_code, function_name, test_cases):

    exec_globals = {}

    try:
        # Execute user code
        exec(user_code, exec_globals)

        if function_name not in exec_globals:
            return {
                "passed": 0,
                "total": len(test_cases),
                "score": 0,
                "error": f"Function '{function_name}' not defined"
            }

        func = exec_globals[function_name]

        passed = 0

        for test in test_cases:
            input_val = test["input"]
            expected_output = test["output"]

            try:
                result = func(input_val)

                if result == expected_output:
                    passed += 1

            except Exception:
                continue

        score = (passed / len(test_cases)) * 100

        return {
            "passed": passed,
            "total": len(test_cases),
            "score": round(score, 2)
        }

    except Exception as e:
        return {
            "passed": 0,
            "total": len(test_cases),
            "score": 0,
            "error": str(e)
        }
