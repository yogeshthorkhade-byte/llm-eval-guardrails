import json
import time
import csv
from datetime import datetime
from app.chatbot import ask_chatbot


# Load dataset
with open("datasets/golden_dataset.json", "r") as file:
    dataset = json.load(file)


# Metrics
total_questions = len(dataset)
correct_answers = 0
hallucination_count = 0
# CSV report file
report_file = "reports/evaluation_report.csv"


# Create CSV headers
with open(report_file, mode="w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "question",
        "expected_answer",
        "ai_answer",
        "similarity_score",
        "result",
        "hallucination_detected",
        "latency_seconds"
    ])

print("\nSTARTING EVALUATION\n")


# Loop through dataset
for item in dataset:

    question = item["question"]
    expected_answer = item["expected_answer"]
    forbidden_words = item["forbidden_words"]

    print(f"\nQuestion: {question}")

    # Start latency timer
    start_time = time.time()

    # Ask chatbot
    ai_answer = ask_chatbot(question)

    # End latency timer
    end_time = time.time()

    latency = end_time - start_time

    # Print answers
    print(f"AI Answer: {ai_answer}")
    print(f"Expected: {expected_answer}")

    # -----------------------------
    # Semantic Similarity Evaluation
    # -----------------------------

    expected_words = expected_answer.lower().split()

    match_count = 0

    for word in expected_words:

        if word in ai_answer.lower():
            match_count += 1

    similarity = match_count / len(expected_words)

    print(f"Similarity Score: {similarity:.2f}")

    if similarity >= 0.5:
        print("Result: CORRECT")
        correct_answers += 1
    else:
        print("Result: INCORRECT")

    # -----------------------------
    # Hallucination Detection
    # -----------------------------

    hallucination_detected = False

    for forbidden in forbidden_words:

        if forbidden.lower() in ai_answer.lower():

            hallucination_detected = True

    if hallucination_detected:
        print("Hallucination Detected: YES")
        hallucination_count += 1
    else:
        print("Hallucination Detected: NO")

    # -----------------------------
    # Latency
    # -----------------------------

    print(f"Latency: {latency:.2f} seconds")
    # Save evaluation result to CSV
with open(report_file, mode="a", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow([
        datetime.now(),
        question,
        expected_answer,
        ai_answer,
        similarity,
        "CORRECT" if similarity >= 0.5 else "INCORRECT",
        hallucination_detected,
        round(latency, 2)
    ])


# -----------------------------
# Final Metrics
# -----------------------------

accuracy = (correct_answers / total_questions) * 100

hallucination_rate = (
    hallucination_count / total_questions
) * 100

print("\nEVALUATION COMPLETE")
print(f"Total Questions: {total_questions}")
print(f"Correct Answers: {correct_answers}")
print(f"Accuracy: {accuracy:.2f}%")
print(f"Hallucination Rate: {hallucination_rate:.2f}%")