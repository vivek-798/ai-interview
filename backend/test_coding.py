from rounds.coding import evaluate_code

user_code = """
def reverse_string(s):
    return s[::-1]
"""

test_cases = [
    {"input": "hello", "output": "olleh"},
    {"input": "python", "output": "nohtyp"}
]

result = evaluate_code(user_code, "reverse_string", test_cases)
print(result)
