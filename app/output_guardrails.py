from app.policy_loader import load_policy


policy = load_policy()


BLOCKED_OUTPUTS = policy[
    "blocked_output_patterns"
]

MAX_RESPONSE_LENGTH = policy[
    "max_response_length"
]


def validate_output(ai_output: str):

    # --------------------------------
    # Empty Response
    # --------------------------------

    if not ai_output.strip():

        return {
            "safe": False,
            "reason": "Empty AI response"
        }


    # --------------------------------
    # Response Length Check
    # --------------------------------

    if len(ai_output) > MAX_RESPONSE_LENGTH:

        return {
            "safe": False,
            "reason": "Response too long"
        }


    # --------------------------------
    # Unsafe Output Detection
    # --------------------------------

    text = ai_output.lower()

    for pattern in BLOCKED_OUTPUTS:

        if pattern in text:

            return {
                "safe": False,
                "reason": (
                    f"Unsafe output detected: "
                    f"{pattern}"
                )
            }


    # --------------------------------
    # Safe Output
    # --------------------------------

    return {
        "safe": True,
        "reason": "Output validated"
    }