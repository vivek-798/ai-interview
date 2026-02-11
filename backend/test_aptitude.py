from rounds.aptitude import evaluate_aptitude

user_answers={
    1:"5 days",
    2:"32",
    3:"10 m/s"
}

result = evaluate_aptitude(user_answers)
print(result)