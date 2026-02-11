import json

def load_coding_questions():
    with open("questions/coding_questions.json", "r") as file:
        return json.load(file)


def evaluate_code(user_code, function_name, test_cases):
    results = []

    try:
        exec(user_code, globals())
        func = globals()[function_name]

        for case in test_cases:
            output = func(case["input"])
            results.append(output == case["output"])

        score = sum(results) / len(results) * 100

        return {
            "passed": sum(results),
            "total": len(results),
            "score": score
        }

    except Exception as e:
        return {
            "error": str(e),
            "score": 0
        }
