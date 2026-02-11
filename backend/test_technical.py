from rounds.technical import select_questions, evaluate_answers

# Simulated resume skills (from resume parser)
resume_skills = ['python', 'data structures']

# Step 1: Select questions
questions = select_questions(resume_skills)

# Step 2: Simulated user answers
user_answers = {
    1: "A list is a mutable and ordered collection in Python",
    2: "Tuple is immutable",
    3: "Stack follows LIFO and supports push and pop operations",
    4: "List is mutable while tuple is immutable"
}

# Step 3: Evaluate
result = evaluate_answers(questions, user_answers)

print(result)
