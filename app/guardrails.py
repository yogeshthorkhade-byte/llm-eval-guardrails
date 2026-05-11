import re


# Blocked prompt patterns
BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "bypass safety",
    "reveal secrets",
    "pretend you are unrestricted",
    "hack the system"
]


def validate_input(user_input: str):

    # Lowercase for matching
    text = user_input.lower()

    # Check prompt injections
    for pattern in BLOCKED_PATTERNS:

        if pattern in text:

            return {
                "safe": False,
                "reason": f"Blocked pattern detected: {pattern}"
            }

    # Credit card detection
    credit_card_pattern = r"\b(?:\d[ -]*?){13,16}\b"

    if re.search(credit_card_pattern, user_input):

        return {
            "safe": False,
            "reason": "Possible credit card detected"
        }

    # Safe input
    return {
        "safe": True,
        "reason": "Input validated"
    }