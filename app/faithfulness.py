# --------------------------------
# Faithfulness Evaluation
# --------------------------------

def evaluate_faithfulness(
    answer,
    sources,
    threshold=0.20
):

    # Convert answer into keywords
    answer_words = set(
        answer.lower().split()
    )


    highest_score = 0


    # Compare against chunks
    for source in sources:

        chunk = source["chunk"]

        chunk_words = set(
            chunk.lower().split()
        )


        # Count matching words
        common_words = (
            answer_words.intersection(
                chunk_words
            )
        )


        # Calculate overlap score
        score = (
            len(common_words)
            / len(answer_words)
        )


        if score > highest_score:

            highest_score = score


    # Hallucination detection
    hallucination = (
        highest_score < threshold
    )


    return {

        "faithfulness_score":
            round(highest_score, 2),

        "hallucination_detected":
            hallucination
    }