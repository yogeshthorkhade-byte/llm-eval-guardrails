import json
import time
import csv
import os

from datetime import datetime

from app.chatbot import ask_chatbot


# --------------------------------
# Evaluation Thresholds
# --------------------------------

MIN_ACCURACY = 80
MAX_HALLUCINATION_RATE = 5
MAX_LATENCY = 3


# --------------------------------
# Create Reports Folder
# --------------------------------

os.makedirs("reports", exist_ok=True)


# --------------------------------
# CSV Report File
# --------------------------------

report_file = "reports/evaluation_report.csv"


# --------------------------------
# Create CSV Headers
# --------------------------------

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


# --------------------------------
# Load Golden Dataset
# --------------------------------

with open("datasets/golden_dataset.json", "r") as file:

    dataset = json.load(file)


# --------------------------------
# Metrics
# --------------------------------

total_questions = len(dataset)

correct_answers = 0

hallucination_count = 0

total_latency = 0


print("\nSTARTING EVALUATION\n")


# --------------------------------
# Evaluation Loop
# --------------------------------

for item in dataset:

    question = item["question"]

    expected_answer = item["expected_answer"]

    print(f"Question: {question}")


    # --------------------------------
    # Start Timer
    # --------------------------------

    start_time = time.time()


    # --------------------------------
    # Ask Chatbot
    # --------------------------------

    ai_answer = ask_chatbot(question)


    # --------------------------------
    # End Timer
    # --------------------------------

    end_time = time.time()

    latency = end_time - start_time

    total_latency += latency


    print(f"AI Answer: {ai_answer}")

    print(f"Expected: {expected_answer}")


    # --------------------------------
    # Improved Semantic Matching
    # --------------------------------

    expected_words = expected_answer.lower().split()

    matched_words = 0


    for word in expected_words:

        if word in ai_answer.lower():

            matched_words += 1


    similarity = matched_words / len(expected_words)


    print(f"Similarity Score: {similarity:.2f}")


    # --------------------------------
    # Correctness Check
    # --------------------------------

    if similarity >= 0.5:

        result = "CORRECT"

        correct_answers += 1

    else:

        result = "INCORRECT"


    print(f"Result: {result}")


    # --------------------------------
    # Hallucination Detection
    # --------------------------------

    hallucination_detected = False


    if similarity < 0.3:

        hallucination_detected = True

        hallucination_count += 1


    print(f"Hallucination Detected: {hallucination_detected}")


    # --------------------------------
    # Latency
    # --------------------------------

    print(f"Latency: {latency:.2f} seconds")


    # --------------------------------
    # Save Results to CSV
    # --------------------------------

    with open(report_file, mode="a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now(),
            question,
            expected_answer,
            ai_answer,
            round(similarity, 2),
            result,
            hallucination_detected,
            round(latency, 2)
        ])


    print("\n-----------------------------------\n")


# --------------------------------
# Final Metrics
# --------------------------------

accuracy = (correct_answers / total_questions) * 100

hallucination_rate = (
    hallucination_count / total_questions
) * 100

average_latency = total_latency / total_questions


print("\nEVALUATION COMPLETE")

print(f"Total Questions: {total_questions}")

print(f"Correct Answers: {correct_answers}")

print(f"Accuracy: {accuracy:.2f}%")

print(f"Hallucination Rate: {hallucination_rate:.2f}%")

print(f"Average Latency: {average_latency:.2f} seconds")


# --------------------------------
# CI/CD Threshold Validation
# --------------------------------

pipeline_failed = False


# Accuracy Check
if accuracy < MIN_ACCURACY:

    print("\nCI/CD FAILURE: Accuracy below threshold")

    pipeline_failed = True


# Hallucination Check
if hallucination_rate > MAX_HALLUCINATION_RATE:

    print("\nCI/CD FAILURE: Hallucination rate too high")

    pipeline_failed = True


# Latency Check
if average_latency > MAX_LATENCY:

    print("\nCI/CD FAILURE: Latency too high")

    pipeline_failed = True


# --------------------------------
# Fail Pipeline Intentionally
# --------------------------------

if pipeline_failed:

    raise Exception(
        "CI/CD quality thresholds failed"
    )


print("\nCI/CD PASSED")