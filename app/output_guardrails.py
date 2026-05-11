# Blocked output patterns
BLOCKED_OUTPUTS = [
    "hate",
    "kill",
    "terrorist",
    "hack bank",
    "steal password"
]


def validate_output(ai_output: str):

    # Empty response check
    if not ai_output.strip():

        return {
            "safe": False,
            "reason": "Empty AI response"
        }

    # Long response check
    if len(ai_output) > 3000:

        return {
            "safe": False,
            "reason": "Response too long"
        }

    # Toxic / unsafe keyword detection
    text = ai_output.lower()

    for pattern in BLOCKED_OUTPUTS:

        if pattern in text:

            return {
                "safe": False,
                "reason": f"Unsafe output detected: {pattern}"
            }

    # Safe response
    return {
        "safe": True,
        "reason": "Output validated"
    }