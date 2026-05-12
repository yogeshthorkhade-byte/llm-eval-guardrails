import re

from app.policy_loader import load_policy


policy = load_policy()


BLOCKED_PATTERNS = policy[
    "blocked_input_patterns"
]


def validate_input(user_input: str):

    text = user_input.lower()


    # --------------------------------
    # Prompt Injection Detection
    # --------------------------------

    for pattern in BLOCKED_PATTERNS:

        if pattern in text:

            return {
                "safe": False,
                "reason": (
                    f"Blocked pattern detected: "
                    f"{pattern}"
                )
            }


    # --------------------------------
    # Credit Card Detection
    # --------------------------------

    credit_card_pattern = (
        r"\\b(?:\\d[ -]*?){13,16}\\b"
    )

    if re.search(
        credit_card_pattern,
        user_input
    ):

        return {
            "safe": False,
            "reason": (
                "Possible credit card detected"
            )
        }


    # --------------------------------
    # Safe Input
    # --------------------------------

    return {
        "safe": True,
        "reason": "Input validated"
    }