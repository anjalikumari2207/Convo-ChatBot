def detect_tone(message: str) -> str:
    """
    Detect user's emotional tone based on keywords.
    Returns one of: empathetic, friendly, neutral
    """

    message_lower = message.lower()

    sad_keywords = ["sad", "low", "tired", "upset", "depressed", "not okay"]
    happy_keywords = ["haha", "lol", "fun", "excited", "great", "awesome"]

    for word in sad_keywords:
        if word in message_lower:
            return "empathetic"

    for word in happy_keywords:
        if word in message_lower:
            return "friendly"

    return "neutral"
